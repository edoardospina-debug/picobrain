#!/usr/bin/env python3
"""
Employee Migration Script for PicoBrain Database
Migrates employees from CSV to PicoBrain API
Version: 1.0
Date: 2025-01-11
"""

import asyncio
import csv
import json
import logging
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import re

import aiohttp
from pydantic import BaseModel, EmailStr, Field, validator

# ==================== CONFIGURATION ====================

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
AUTH_ENDPOINT = f"{API_BASE_URL}/auth/login"
EMPLOYEES_ENDPOINT = f"{API_BASE_URL}/employees"
EMPLOYEES_BULK_ENDPOINT = f"{API_BASE_URL}/employees/bulk"

# Migration Configuration
CSV_FILE_PATH = "/Users/edo/PyProjects/input_files/Employees.csv"
BATCH_SIZE = 20
STOP_ON_ERROR = False
VALIDATE_ALL_FIRST = False

# Clinic ID Mapping (temp_id -> UUID)
CLINIC_ID_MAPPING = {
    "10": "c69dfe69-63c2-445f-9624-54c7876becb5",  # London
    "11": "44cc3318-35f9-45e9-a9b5-aab0e47c8c15",  # Milan
    "12": "2b79920a-0ebf-4684-bc11-2ca6316af262",  # Los Angeles
    "13": "f3711a7f-216a-493f-8543-d03d3fa4387f",  # Vancouver
    "14": "94646ff0-78c3-4d49-ab90-5336c861b3c4",  # New York
}

# Role Mapping
ROLE_MAPPING = {
    "doctor": "doctor",
    "staff": "staff",
    "manager": "manager",
    "finance": "admin",  # Map finance to admin
}

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('employee_migration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== DATA MODELS ====================

@dataclass
class MigrationResult:
    """Track migration results"""
    total_processed: int = 0
    successful: List[Dict] = field(default_factory=list)
    failed: List[Dict] = field(default_factory=list)
    skipped: List[Dict] = field(default_factory=list)

class EmployeeDTO(BaseModel):
    """DTO matching the API schema"""
    # Person fields
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_mobile_country_code: Optional[str] = None
    phone_mobile_number: Optional[str] = None
    phone_home_country_code: Optional[str] = None
    phone_home_number: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    
    # Employee fields
    employee_code: Optional[str] = None
    primary_clinic_id: str  # UUID as string
    role: str
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    license_expiry: Optional[date] = None
    hire_date: date
    termination_date: Optional[date] = None
    base_salary_minor: Optional[int] = None
    salary_currency: Optional[str] = None
    commission_rate: Optional[Decimal] = None
    is_active: bool = True
    can_perform_treatments: bool = False

# ==================== UTILITY FUNCTIONS ====================

def parse_date(date_str: str) -> Optional[date]:
    """Parse date from DD/MM/YYYY format"""
    if not date_str or date_str.strip() == "":
        return None
    
    try:
        # Handle DD/MM/YYYY format
        parts = date_str.strip().split('/')
        if len(parts) == 3:
            day, month, year = parts
            # Handle future dates that might be data entry errors
            year_int = int(year)
            if year_int > 2025:
                logger.warning(f"Future date detected: {date_str}, setting year to 2025")
                year_int = 2025
            return date(year_int, int(month), int(day))
    except Exception as e:
        logger.warning(f"Could not parse date '{date_str}': {e}")
        return None

def clean_email(email: str) -> Optional[str]:
    """Clean and validate email address"""
    if not email or email.strip() == "":
        return None
    
    email = email.strip().lower()
    
    # Check for obviously invalid emails
    if email in ["na@a.cpm", "xxx@picoclinics.com", ""]:
        return None
    
    # Basic email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return email
    
    return None

def parse_phone(phone_str: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse phone into country code and number"""
    if not phone_str or phone_str.strip() == "":
        return None, None
    
    phone = phone_str.strip()
    
    # Simple parsing - can be enhanced based on actual data patterns
    if phone.startswith('+'):
        # Try to extract country code
        if len(phone) > 10:
            return phone[:3], phone[3:]
    
    # Default to no country code
    return None, phone if len(phone) >= 4 else None

def parse_commission(commission_str: str) -> Optional[Decimal]:
    """Parse commission percentage"""
    if not commission_str or commission_str == "0":
        return None
    
    try:
        # Convert from decimal (0.1) to percentage (10)
        commission = float(commission_str)
        if 0 < commission < 1:
            commission = commission * 100
        return Decimal(str(commission))
    except:
        return None

def split_name(full_name: str) -> Tuple[str, str, Optional[str]]:
    """Split full name into first, last, and middle"""
    if not full_name:
        return "", "", None
    
    parts = full_name.strip().split()
    
    if len(parts) == 0:
        return "", "", None
    elif len(parts) == 1:
        # For single names, use the name as first name and a placeholder for last name
        return parts[0], "(Single)", None
    elif len(parts) == 2:
        return parts[0], parts[1], None
    else:
        # Assume first word is first name, last word is last name, rest is middle
        return parts[0], parts[-1], " ".join(parts[1:-1])

# ==================== MAIN MIGRATION FUNCTIONS ====================

def load_csv_data(file_path: str) -> List[Dict]:
    """Load and parse CSV file"""
    logger.info(f"Loading CSV from {file_path}")
    
    employees = []
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            employees.append(row)
    
    logger.info(f"Loaded {len(employees)} employee records")
    return employees

def transform_employee(row: Dict) -> Optional[EmployeeDTO]:
    """Transform CSV row to EmployeeDTO"""
    try:
        # Map clinic ID
        clinic_temp_id = row.get('clinic_temp_id', '').strip()
        if not clinic_temp_id or clinic_temp_id not in CLINIC_ID_MAPPING:
            logger.warning(f"Invalid clinic_temp_id: {clinic_temp_id} for {row.get('name')}")
            return None
        
        clinic_uuid = CLINIC_ID_MAPPING[clinic_temp_id]
        
        # Parse name
        first_name, last_name, middle_name = split_name(row.get('name', ''))
        if not first_name:
            logger.warning(f"Invalid name: {row.get('name')}")
            return None
        
        # For single names, check if we have a nickname that might be fuller
        if last_name == "(Single)" and row.get('nickname'):
            # Try using nickname as it might have full name
            nick_first, nick_last, nick_middle = split_name(row.get('nickname', ''))
            if nick_last and nick_last != "(Single)":
                first_name, last_name, middle_name = nick_first, nick_last, nick_middle
        
        # Determine email
        work_email = clean_email(row.get('work_email', ''))
        personal_email = clean_email(row.get('personal_email', ''))
        email = work_email or personal_email
        
        # Parse role
        role_raw = row.get('role', '').strip().lower()
        role = ROLE_MAPPING.get(role_raw, 'staff')  # Default to staff
        
        # Parse dates
        hire_date = parse_date(row.get('from_date', ''))
        if not hire_date:
            hire_date = date(2024, 1, 1)  # Default hire date
            logger.warning(f"No hire date for {first_name} {last_name}, using default")
        
        termination_date = parse_date(row.get('to_date', ''))
        
        # Determine if active
        is_active = True
        if termination_date and termination_date < date.today():
            is_active = False
        
        # Parse DOB
        dob = parse_date(row.get('dob', ''))
        
        # Parse salary
        base_salary = None
        try:
            salary_str = row.get('base_salary', '0')
            if salary_str and salary_str != '0':
                # Convert to minor units (cents/pence)
                base_salary = int(float(salary_str) * 100)
        except:
            pass
        
        # Parse commission
        commission = parse_commission(row.get('commission_percentage', ''))
        
        # Create DTO
        dto = EmployeeDTO(
            # Person fields
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            email=email,
            dob=dob,
            
            # Employee fields
            employee_code=row.get('temp_id', ''),  # Use temp_id as initial code
            primary_clinic_id=clinic_uuid,
            role=role,
            license_number=row.get('license_number') if row.get('license_number') else None,
            license_expiry=parse_date(row.get('license_expiration', '')),
            hire_date=hire_date,
            termination_date=termination_date,
            base_salary_minor=base_salary,
            commission_rate=commission,
            is_active=is_active,
            can_perform_treatments=(role == 'doctor'),
            
            # Address fields (stored in person)
            # Note: These would need to be added to the DTO if the API supports them
        )
        
        return dto
        
    except Exception as e:
        logger.error(f"Error transforming employee {row.get('name')}: {e}")
        return None

async def authenticate(session: aiohttp.ClientSession, username: str, password: str) -> Optional[str]:
    """Authenticate with the API and get token"""
    logger.info("Authenticating with API...")
    
    try:
        # Use form data for authentication (OAuth2 expects form-encoded data)
        data = aiohttp.FormData()
        data.add_field('username', username)
        data.add_field('password', password)
        
        async with session.post(AUTH_ENDPOINT, data=data) as response:
            if response.status == 200:
                result = await response.json()
                token = result.get('access_token')
                logger.info("Authentication successful")
                return token
            else:
                logger.error(f"Authentication failed: {response.status}")
                return None
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None

async def create_employees_batch(
    session: aiohttp.ClientSession,
    token: str,
    employees: List[EmployeeDTO]
) -> Tuple[List[Dict], List[Dict]]:
    """Create a batch of employees via API"""
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Prepare batch data - convert dates to strings for JSON serialization
    employees_data = []
    for emp in employees:
        emp_dict = emp.dict(exclude_none=True)
        # Convert date objects to ISO format strings
        for key, value in emp_dict.items():
            if isinstance(value, date):
                emp_dict[key] = value.isoformat()
            elif isinstance(value, Decimal):
                emp_dict[key] = str(value)
        employees_data.append(emp_dict)
    
    batch_data = {
        "employees": employees_data,
        "stop_on_error": STOP_ON_ERROR,
        "validate_all_first": VALIDATE_ALL_FIRST
    }
    
    try:
        async with session.post(
            EMPLOYEES_BULK_ENDPOINT,
            headers=headers,
            json=batch_data
        ) as response:
            
            if response.status in [200, 201]:
                result = await response.json()
                return result.get('created', []), result.get('failed', [])
            else:
                error_text = await response.text()
                logger.error(f"Batch creation failed: {response.status} - {error_text}")
                # Return all as failed
                failed = [
                    {"employee": emp.dict(), "error": f"API error: {response.status}"}
                    for emp in employees
                ]
                return [], failed
                
    except Exception as e:
        logger.error(f"Batch creation error: {e}")
        failed = [
            {"employee": emp.dict(), "error": str(e)}
            for emp in employees
        ]
        return [], failed

async def migrate_employees(username: str, password: str) -> MigrationResult:
    """Main migration function"""
    result = MigrationResult()
    
    # Load CSV data
    csv_data = load_csv_data(CSV_FILE_PATH)
    result.total_processed = len(csv_data)
    
    # Transform data
    logger.info("Transforming employee data...")
    employees = []
    for row in csv_data:
        dto = transform_employee(row)
        if dto:
            employees.append(dto)
        else:
            result.skipped.append({
                "original": row,
                "reason": "Failed to transform"
            })
    
    logger.info(f"Transformed {len(employees)} employees successfully")
    logger.info(f"Skipped {len(result.skipped)} employees due to data issues")
    
    # Create batches
    batches = [
        employees[i:i+BATCH_SIZE]
        for i in range(0, len(employees), BATCH_SIZE)
    ]
    logger.info(f"Created {len(batches)} batches of size {BATCH_SIZE}")
    
    # Execute migration
    async with aiohttp.ClientSession() as session:
        # Authenticate
        token = await authenticate(session, username, password)
        if not token:
            logger.error("Failed to authenticate. Aborting migration.")
            return result
        
        # Process batches
        for i, batch in enumerate(batches, 1):
            logger.info(f"Processing batch {i}/{len(batches)} ({len(batch)} employees)")
            
            created, failed = await create_employees_batch(session, token, batch)
            
            # Track results
            for item in created:
                result.successful.append({
                    "employee": item.get('employee'),
                    "person": item.get('person')
                })
            
            for item in failed:
                result.failed.append(item)
            
            logger.info(f"Batch {i}: {len(created)} created, {len(failed)} failed")
            
            # Small delay between batches
            if i < len(batches):
                await asyncio.sleep(1)
    
    return result

def generate_report(result: MigrationResult):
    """Generate migration report"""
    logger.info("=" * 60)
    logger.info("MIGRATION REPORT")
    logger.info("=" * 60)
    logger.info(f"Total Processed: {result.total_processed}")
    logger.info(f"Successful: {len(result.successful)}")
    logger.info(f"Failed: {len(result.failed)}")
    logger.info(f"Skipped: {len(result.skipped)}")
    logger.info("=" * 60)
    
    # Save detailed report
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_processed": result.total_processed,
            "successful": len(result.successful),
            "failed": len(result.failed),
            "skipped": len(result.skipped)
        },
        "successful": result.successful,
        "failed": result.failed,
        "skipped": result.skipped
    }
    
    report_file = f"migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    logger.info(f"Detailed report saved to: {report_file}")
    
    # Create ID mapping file
    if result.successful:
        id_mapping = {}
        for item in result.successful:
            emp = item.get('employee', {})
            if emp.get('employee_code'):
                id_mapping[emp['employee_code']] = emp.get('id')
        
        mapping_file = f"employee_id_mapping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(mapping_file, 'w') as f:
            json.dump(id_mapping, f, indent=2)
        
        logger.info(f"ID mapping saved to: {mapping_file}")

# ==================== AUTOMATED EXECUTION ====================

async def main():
    """Main entry point - Modified for autonomous execution"""
    logger.info("Starting Employee Migration to PicoBrain")
    logger.info(f"Source: {CSV_FILE_PATH}")
    logger.info(f"Target: {API_BASE_URL}")
    
    # Use correct admin credentials for autonomous execution
    username = "admin@picobrain.com"  # Use email format as per your docs
    password = "admin123"
    
    print("\n" + "=" * 60)
    print("Migration Configuration:")
    print(f"  - CSV File: {CSV_FILE_PATH}")
    print(f"  - API URL: {API_BASE_URL}")
    print(f"  - Batch Size: {BATCH_SIZE}")
    print(f"  - Stop on Error: {STOP_ON_ERROR}")
    print("=" * 60)
    
    # Run migration automatically
    try:
        result = await migrate_employees(username, password)
        generate_report(result)
        
        print("\n" + "=" * 60)
        print("MIGRATION COMPLETE")
        print(f"  ✅ Successful: {len(result.successful)}")
        print(f"  ❌ Failed: {len(result.failed)}")
        print(f"  ⭐️ Skipped: {len(result.skipped)}")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
