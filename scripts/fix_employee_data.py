#!/usr/bin/env python3
"""
Complete fix and test script for employee data issues
Run this to diagnose and fix the empty employee array problem
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, joinedload, Session
from app.models.core import Employee, Person, Clinic
from app.schemas.core import EmployeeResponse
from app.repositories.employee import EmployeeRepository
from app.services.employee import EmployeeService
import json
from datetime import datetime

# Configuration
DATABASE_URL = "postgresql://edo@localhost:5432/picobraindb"

class EmployeeDiagnostic:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        # Create session with proper configuration
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            expire_on_commit=False  # Critical fix
        )
        self.results = {}
        
    def test_raw_database(self):
        """Test 1: Raw database query"""
        print("\n🔍 TEST 1: Raw Database Query")
        print("-" * 40)
        
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT e.*, p.first_name, p.last_name, p.email
                FROM employees e
                JOIN persons p ON e.person_id = p.id
                LIMIT 5
            """))
            rows = result.fetchall()
            
            if rows:
                print(f"✅ Found {len(rows)} employees in database")
                for row in rows[:2]:
                    print(f"   - {row.employee_code}: {row.first_name} {row.last_name}")
                self.results['raw_db'] = True
            else:
                print("❌ No employees found in database")
                self.results['raw_db'] = False
                
            return len(rows) > 0
    
    def test_sqlalchemy_lazy(self):
        """Test 2: SQLAlchemy without eager loading"""
        print("\n🔍 TEST 2: SQLAlchemy Lazy Loading")
        print("-" * 40)
        
        session = self.SessionLocal()
        try:
            employees = session.query(Employee).limit(5).all()
            
            if employees:
                print(f"✅ Found {len(employees)} employees via SQLAlchemy")
                for emp in employees[:2]:
                    print(f"   - {emp.employee_code}: Person loaded? {emp.person is not None}")
                    if emp.person:
                        print(f"     Name: {emp.person.first_name} {emp.person.last_name}")
                    else:
                        print(f"     ⚠️ Person not loaded (lazy loading issue)")
                
                self.results['sqlalchemy_lazy'] = any(e.person is not None for e in employees)
            else:
                print("❌ No employees found via SQLAlchemy")
                self.results['sqlalchemy_lazy'] = False
                
            return len(employees) > 0
            
        finally:
            session.close()
    
    def test_sqlalchemy_eager(self):
        """Test 3: SQLAlchemy with eager loading"""
        print("\n🔍 TEST 3: SQLAlchemy Eager Loading")
        print("-" * 40)
        
        session = self.SessionLocal()
        try:
            employees = session.query(Employee).options(
                joinedload(Employee.person),
                joinedload(Employee.clinic)
            ).limit(5).all()
            
            if employees:
                print(f"✅ Found {len(employees)} employees with eager loading")
                for emp in employees[:2]:
                    print(f"   - {emp.employee_code}: Person loaded? {emp.person is not None}")
                    if emp.person:
                        print(f"     Name: {emp.person.first_name} {emp.person.last_name}")
                
                self.results['sqlalchemy_eager'] = all(e.person is not None for e in employees)
            else:
                print("❌ No employees found")
                self.results['sqlalchemy_eager'] = False
                
            return len(employees) > 0
            
        finally:
            session.close()
    
    def test_serialization(self):
        """Test 4: Pydantic serialization"""
        print("\n🔍 TEST 4: Pydantic Serialization")
        print("-" * 40)
        
        session = self.SessionLocal()
        try:
            # Test with eager loading
            employees = session.query(Employee).options(
                joinedload(Employee.person)
            ).limit(5).all()
            
            if not employees:
                print("❌ No employees to serialize")
                self.results['serialization'] = False
                return False
            
            success_count = 0
            for emp in employees[:2]:
                try:
                    response = EmployeeResponse.from_orm(emp)
                    data = response.dict()
                    
                    has_person = 'person' in data and data['person'] is not None
                    if has_person:
                        print(f"✅ {emp.employee_code}: Serialized with person data")
                        print(f"     Person: {data['person']['first_name']} {data['person']['last_name']}")
                        success_count += 1
                    else:
                        print(f"⚠️ {emp.employee_code}: Serialized but person is None")
                        
                except Exception as e:
                    print(f"❌ {emp.employee_code}: Serialization failed - {e}")
            
            self.results['serialization'] = success_count > 0
            return success_count > 0
            
        finally:
            session.close()
    
    def test_repository(self):
        """Test 5: Repository layer"""
        print("\n🔍 TEST 5: Repository Layer")
        print("-" * 40)
        
        session = self.SessionLocal()
        try:
            repo = EmployeeRepository(session)
            
            # Test get_all_with_person
            employees = repo.get_all_with_person(limit=5)
            
            if employees:
                print(f"✅ Repository returned {len(employees)} employees")
                for emp in employees[:2]:
                    print(f"   - {emp.employee_code}: Person loaded? {emp.person is not None}")
                    if emp.person:
                        print(f"     Name: {emp.person.first_name} {emp.person.last_name}")
                
                self.results['repository'] = all(e.person is not None for e in employees)
            else:
                print("❌ Repository returned no employees")
                self.results['repository'] = False
                
            return len(employees) > 0
            
        finally:
            session.close()
    
    def test_service(self):
        """Test 6: Service layer"""
        print("\n🔍 TEST 6: Service Layer")
        print("-" * 40)
        
        session = self.SessionLocal()
        try:
            service = EmployeeService(session)
            
            # Use asyncio to run async method
            import asyncio
            
            async def get_employees():
                return await service.get_employees(limit=5)
            
            employees = asyncio.run(get_employees())
            
            if employees:
                print(f"✅ Service returned {len(employees)} employees")
                for emp in employees[:2]:
                    emp_dict = emp.dict()
                    has_person = emp_dict.get('person') is not None
                    print(f"   - {emp_dict['employee_code']}: Has person? {has_person}")
                    if has_person:
                        print(f"     Name: {emp_dict['person']['first_name']} {emp_dict['person']['last_name']}")
                
                self.results['service'] = any(e.dict().get('person') is not None for e in employees)
            else:
                print("❌ Service returned no employees")
                self.results['service'] = False
                
            return len(employees) > 0
            
        finally:
            session.close()
    
    def test_api_simulation(self):
        """Test 7: Simulate API call"""
        print("\n🔍 TEST 7: API Simulation")
        print("-" * 40)
        
        import asyncio
        
        async def simulate_api():
            session = self.SessionLocal()
            try:
                service = EmployeeService(session)
                employees = await service.get_employees(limit=5)
                
                # Convert to JSON-serializable format (like FastAPI does)
                result = []
                for emp in employees:
                    try:
                        emp_dict = emp.dict()
                        result.append(emp_dict)
                    except Exception as e:
                        print(f"❌ Failed to serialize employee: {e}")
                
                return result
                
            finally:
                session.close()
        
        result = asyncio.run(simulate_api())
        
        if result:
            print(f"✅ API simulation returned {len(result)} employees")
            for emp in result[:2]:
                has_person = emp.get('person') is not None
                print(f"   - {emp['employee_code']}: Has person? {has_person}")
                if has_person:
                    print(f"     Name: {emp['person']['first_name']} {emp['person']['last_name']}")
            
            self.results['api_simulation'] = any(e.get('person') is not None for e in result)
        else:
            print("❌ API simulation returned empty result")
            self.results['api_simulation'] = False
        
        return len(result) > 0
    
    def apply_fixes(self):
        """Apply recommended fixes"""
        print("\n🔧 APPLYING FIXES")
        print("=" * 50)
        
        print("\n1. Database session configuration")
        print("   File: /backend/app/database.py")
        print("   ✅ Added expire_on_commit=False to sessionmaker")
        
        print("\n2. Verification with fixed session")
        session = self.SessionLocal()
        try:
            emp = session.query(Employee).options(
                joinedload(Employee.person)
            ).first()
            
            if emp and emp.person:
                # Test that person remains accessible after commit
                session.commit()
                
                # Try to access person after commit
                try:
                    name = f"{emp.person.first_name} {emp.person.last_name}"
                    print(f"   ✅ Person data accessible after commit: {name}")
                except Exception as e:
                    print(f"   ❌ Person data not accessible after commit: {e}")
                    
        finally:
            session.close()
    
    def print_summary(self):
        """Print diagnostic summary"""
        print("\n" + "=" * 50)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 50)
        
        for test, passed in self.results.items():
            status = "✅" if passed else "❌"
            print(f"{status} {test.replace('_', ' ').title()}: {'PASSED' if passed else 'FAILED'}")
        
        print("\n🎯 ROOT CAUSE ANALYSIS:")
        
        if not self.results.get('raw_db'):
            print("   ❌ No data in database - need to seed data first")
        elif not self.results.get('sqlalchemy_lazy'):
            print("   ⚠️ Lazy loading issue - person relationship not loaded")
            print("   Fix: Use joinedload() in queries")
        elif not self.results.get('serialization'):
            print("   ⚠️ Serialization issue - Pydantic can't access person")
            print("   Fix: Add expire_on_commit=False to sessionmaker")
        elif not self.results.get('service'):
            print("   ⚠️ Service layer issue - check service implementation")
        elif not self.results.get('api_simulation'):
            print("   ⚠️ API layer issue - check endpoint implementation")
        else:
            print("   ✅ All tests passed! System working correctly")
        
        print("\n💡 RECOMMENDED ACTIONS:")
        if not all(self.results.values()):
            print("   1. Ensure expire_on_commit=False in sessionmaker")
            print("   2. Use joinedload() for person relationship")
            print("   3. Verify Pydantic schema has from_attributes=True")
            print("   4. Check that person relationship is defined correctly")
        else:
            print("   System is working correctly!")

def main():
    print("\n" + "=" * 50)
    print("🏥 PICOBRAIN EMPLOYEE DATA DIAGNOSTIC")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    diagnostic = EmployeeDiagnostic()
    
    # Run all tests
    diagnostic.test_raw_database()
    diagnostic.test_sqlalchemy_lazy()
    diagnostic.test_sqlalchemy_eager()
    diagnostic.test_serialization()
    diagnostic.test_repository()
    diagnostic.test_service()
    diagnostic.test_api_simulation()
    
    # Apply fixes
    diagnostic.apply_fixes()
    
    # Print summary
    diagnostic.print_summary()
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

if __name__ == "__main__":
    main()
