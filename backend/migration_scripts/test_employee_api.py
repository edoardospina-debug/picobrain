"""Test script for enhanced Employee API with composite creation"""
import asyncio
import httpx
import json
from datetime import date
from typing import Optional
from uuid import UUID


class EmployeeAPITester:
    """Test client for Employee API endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8000", token: Optional[str] = None):
        self.base_url = base_url
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    async def create_employee_with_person(self):
        """Test creating an employee with person data"""
        
        # Sample employee data with person fields
        employee_data = {
            # Person fields
            "first_name": "John",
            "last_name": "Smith",
            "middle_name": "Michael",
            "email": "john.smith@clinic.com",
            "phone_mobile_country_code": "+1",
            "phone_mobile_number": "5551234567",
            "dob": "1985-06-15",
            "gender": "M",
            "nationality": "US",
            "id_type": "passport",
            "id_number": "P123456789",
            
            # Employee fields
            "employee_code": None,  # Will be auto-generated
            "primary_clinic_id": "123e4567-e89b-12d3-a456-426614174000",  # Replace with actual clinic ID
            "role": "doctor",
            "specialization": "General Practice",
            "license_number": "MD123456",
            "license_expiry": "2025-12-31",
            "hire_date": str(date.today()),
            "base_salary_minor": 12000000,  # $120,000 in cents
            "salary_currency": "USD",
            "is_active": True,
            "can_perform_treatments": True
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/employees/",
                json=employee_data,
                headers=self.headers
            )
            
            if response.status_code == 201:
                result = response.json()
                print("✅ Employee created successfully!")
                print(f"Employee ID: {result['employee']['id']}")
                print(f"Employee Code: {result['employee']['employee_code']}")
                print(f"Person ID: {result['person']['id']}")
                print(f"Message: {result['message']}")
                return result
            else:
                print(f"❌ Failed to create employee: {response.status_code}")
                print(response.json())
                return None
    
    async def bulk_create_employees(self):
        """Test bulk employee creation"""
        
        bulk_data = {
            "employees": [
                {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "email": "jane.doe@clinic.com",
                    "primary_clinic_id": "123e4567-e89b-12d3-a456-426614174000",
                    "role": "nurse",
                    "hire_date": str(date.today()),
                    "license_number": "RN789012",
                    "license_expiry": "2026-06-30",
                    "can_perform_treatments": True
                },
                {
                    "first_name": "Bob",
                    "last_name": "Johnson",
                    "email": "bob.johnson@clinic.com",
                    "primary_clinic_id": "123e4567-e89b-12d3-a456-426614174000",
                    "role": "receptionist",
                    "hire_date": str(date.today()),
                    "base_salary_minor": 4000000,  # $40,000
                    "salary_currency": "USD"
                }
            ],
            "stop_on_error": False,
            "validate_all_first": True
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/employees/bulk",
                json=bulk_data,
                headers=self.headers,
                timeout=30.0
            )
            
            if response.status_code == 201:
                result = response.json()
                print("✅ Bulk creation completed!")
                print(f"Total processed: {result['total_processed']}")
                print(f"Successfully created: {result['total_created']}")
                print(f"Failed: {result['total_failed']}")
                
                if result['created']:
                    print("\nCreated employees:")
                    for emp in result['created']:
                        print(f"  - {emp['employee']['employee_code']}: {emp['person']['first_name']} {emp['person']['last_name']}")
                
                if result['failed']:
                    print("\nFailed creations:")
                    for failure in result['failed']:
                        print(f"  - Index {failure['index']}: {failure['error']}")
                
                return result
            else:
                print(f"❌ Bulk creation failed: {response.status_code}")
                print(response.json())
                return None
    
    async def get_employees(self, clinic_id: Optional[str] = None):
        """Test getting employees with filters"""
        
        params = {}
        if clinic_id:
            params['clinic_id'] = clinic_id
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/employees/",
                params=params,
                headers=self.headers
            )
            
            if response.status_code == 200:
                employees = response.json()
                print(f"✅ Found {len(employees)} employees")
                for emp in employees[:5]:  # Show first 5
                    print(f"  - {emp['employee_code']}: {emp['person']['first_name']} {emp['person']['last_name']} ({emp['role']})")
                return employees
            else:
                print(f"❌ Failed to get employees: {response.status_code}")
                return None
    
    async def get_medical_staff(self):
        """Test getting medical staff"""
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/employees/medical-staff",
                headers=self.headers
            )
            
            if response.status_code == 200:
                staff = response.json()
                print(f"✅ Found {len(staff)} medical staff members")
                for emp in staff:
                    print(f"  - {emp['employee_code']}: Dr. {emp['person']['first_name']} {emp['person']['last_name']}")
                return staff
            else:
                print(f"❌ Failed to get medical staff: {response.status_code}")
                return None


async def main():
    """Run the tests"""
    
    # Initialize tester (you'll need to get an auth token first)
    # For testing, you might want to disable auth temporarily or get a token via login
    tester = EmployeeAPITester(token="your-auth-token-here")
    
    print("=" * 60)
    print("EMPLOYEE API TESTS")
    print("=" * 60)
    
    # Test 1: Create a single employee with person
    print("\n1. Creating single employee with person...")
    employee = await tester.create_employee_with_person()
    
    # Test 2: Bulk create employees
    print("\n2. Bulk creating employees...")
    bulk_result = await tester.bulk_create_employees()
    
    # Test 3: Get all employees
    print("\n3. Getting all employees...")
    employees = await tester.get_employees()
    
    # Test 4: Get medical staff
    print("\n4. Getting medical staff...")
    medical_staff = await tester.get_medical_staff()
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
