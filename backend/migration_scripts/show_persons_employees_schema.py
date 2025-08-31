#!/usr/bin/env python3
"""
Display complete schema for Persons and Employees tables
"""

import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=False)

def show_table_schema(table_name):
    """Display complete schema for a table"""
    
    with engine.connect() as conn:
        # Get column information from information_schema
        query = text("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default,
                udt_name
            FROM information_schema.columns
            WHERE table_name = :table_name
            ORDER BY ordinal_position;
        """)
        
        result = conn.execute(query, {"table_name": table_name})
        columns = result.fetchall()
        
        if not columns:
            print(f"❌ Table '{table_name}' not found")
            return None
        
        schema_data = []
        for col in columns:
            col_name = col[0]
            data_type = col[1]
            max_length = col[2]
            nullable = col[3]
            default = col[4]
            udt_name = col[5]  # User-defined type name (for enums)
            
            # Format data type with length
            if max_length:
                type_str = f"{data_type}({max_length})"
            elif data_type == 'USER-DEFINED':
                type_str = f"ENUM ('{udt_name}')"
            else:
                type_str = data_type
            
            # Format nullable
            null_str = "NULL" if nullable == 'YES' else "NOT NULL"
            
            # Format default
            if default:
                if 'uuid_generate' in default:
                    default_str = "uuid_generate_v4()"
                elif 'CURRENT_TIMESTAMP' in default:
                    default_str = "CURRENT_TIMESTAMP"
                else:
                    default_str = str(default)[:30]
            else:
                default_str = "-"
            
            schema_data.append([col_name, type_str, null_str, default_str])
        
        return schema_data

def show_foreign_keys(table_name):
    """Show foreign key relationships for a table"""
    
    with engine.connect() as conn:
        query = text("""
            SELECT
                kcu.column_name,
                ccu.table_name AS foreign_table,
                ccu.column_name AS foreign_column
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND tc.table_name = :table_name;
        """)
        
        result = conn.execute(query, {"table_name": table_name})
        return result.fetchall()

def show_enum_values(enum_name):
    """Get possible values for an enum type"""
    
    with engine.connect() as conn:
        query = text("""
            SELECT enumlabel 
            FROM pg_enum 
            WHERE enumtypid = (
                SELECT oid FROM pg_type WHERE typname = :enum_name
            )
            ORDER BY enumsortorder;
        """)
        
        result = conn.execute(query, {"enum_name": enum_name})
        values = [row[0] for row in result]
        return values

def main():
    print("=" * 80)
    print("DATABASE SCHEMA INSPECTION - PERSONS & EMPLOYEES TABLES")
    print("=" * 80)
    
    # PERSONS TABLE
    print("\n📋 PERSONS TABLE SCHEMA")
    print("-" * 60)
    
    persons_schema = show_table_schema('persons')
    if persons_schema:
        print("\nField Structure:")
        print("-" * 60)
        print(f"{'Field Name':<25} {'Data Type':<25} {'Nullable':<10} {'Default':<20}")
        print("-" * 60)
        for row in persons_schema:
            print(f"{row[0]:<25} {row[1]:<25} {row[2]:<10} {row[3]:<20}")
        
        # Check for gender enum values
        print("\nEnum Values:")
        gender_values = show_enum_values('gender_type')
        if gender_values:
            print(f"  gender_type: {', '.join(gender_values)}")
        
        # Show foreign keys
        fks = show_foreign_keys('persons')
        if fks:
            print("\nForeign Keys:")
            for fk in fks:
                print(f"  {fk[0]} → {fk[1]}.{fk[2]}")
        
        # Count records
        with engine.connect() as conn:
            count_result = conn.execute(text("SELECT COUNT(*) FROM persons"))
            count = count_result.scalar()
            print(f"\nCurrent Records: {count}")
    
    # EMPLOYEES TABLE
    print("\n" + "=" * 80)
    print("\n📋 EMPLOYEES TABLE SCHEMA")
    print("-" * 60)
    
    employees_schema = show_table_schema('employees')
    if employees_schema:
        print("\nField Structure:")
        print("-" * 60)
        print(f"{'Field Name':<25} {'Data Type':<25} {'Nullable':<10} {'Default':<20}")
        print("-" * 60)
        for row in employees_schema:
            print(f"{row[0]:<25} {row[1]:<25} {row[2]:<10} {row[3]:<20}")
        
        # Check for role enum values
        print("\nEnum Values:")
        role_values = show_enum_values('employee_role')
        if role_values:
            print(f"  employee_role: {', '.join(role_values)}")
        
        # Show foreign keys
        fks = show_foreign_keys('employees')
        if fks:
            print("\nForeign Key Relationships:")
            for fk in fks:
                print(f"  {fk[0]} → {fk[1]}.{fk[2]}")
        
        # Count records
        with engine.connect() as conn:
            count_result = conn.execute(text("SELECT COUNT(*) FROM employees"))
            count = count_result.scalar()
            print(f"\nCurrent Records: {count}")
    
    # RELATIONSHIP SUMMARY
    print("\n" + "=" * 80)
    print("\n🔗 ENTITY RELATIONSHIP PATTERN")
    print("-" * 60)
    print("""
    Person (Base Entity)
      ├── Employee (via person_id FK)
      │   └── Role determines behavior (doctor, nurse, manager, etc.)
      ├── Client (via person_id FK)
      └── User (via person_id FK for authentication)
    
    Employee → Clinic (via primary_clinic_id FK)
    """)
    
    print("\n" + "=" * 80)
    print("✅ SCHEMA INSPECTION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
