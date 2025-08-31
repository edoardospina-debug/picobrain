#!/usr/bin/env python3
"""
Export Persons and Employees table schemas to JSON
"""

import sys
import json
from pathlib import Path
from sqlalchemy import create_engine, text

# Database connection
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=False)

def get_table_schema(table_name):
    """Get complete schema for a table"""
    
    with engine.connect() as conn:
        # Get column information
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
        
        columns = []
        for row in result:
            columns.append({
                'column_name': row[0],
                'data_type': row[1],
                'max_length': row[2],
                'nullable': row[3] == 'YES',
                'default': row[4],
                'udt_name': row[5]
            })
        
        # Get foreign keys
        fk_query = text("""
            SELECT
                kcu.column_name,
                ccu.table_name AS foreign_table,
                ccu.column_name AS foreign_column
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND tc.table_name = :table_name;
        """)
        
        fk_result = conn.execute(fk_query, {"table_name": table_name})
        
        foreign_keys = []
        for row in fk_result:
            foreign_keys.append({
                'column': row[0],
                'references': f"{row[1]}.{row[2]}"
            })
        
        # Get row count
        count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        row_count = count_result.scalar()
        
        return {
            'table_name': table_name,
            'columns': columns,
            'foreign_keys': foreign_keys,
            'row_count': row_count
        }

def get_enum_values(enum_name):
    """Get values for an enum type"""
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
        return [row[0] for row in result]

def main():
    # Get schemas
    persons_schema = get_table_schema('persons')
    employees_schema = get_table_schema('employees')
    
    # Get enum values
    enums = {
        'gender_type': get_enum_values('gender_type'),
        'employee_role': get_enum_values('employee_role')
    }
    
    # Combine all data
    output = {
        'persons': persons_schema,
        'employees': employees_schema,
        'enums': enums
    }
    
    # Save to file
    output_file = Path(__file__).parent / 'persons_employees_schema.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"✅ Schema exported to {output_file}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("PERSONS & EMPLOYEES TABLE SCHEMAS")
    print("=" * 70)
    
    print(f"\n📋 PERSONS TABLE")
    print(f"   Fields: {len(persons_schema['columns'])}")
    print(f"   Records: {persons_schema['row_count']}")
    print(f"   Foreign Keys: {len(persons_schema['foreign_keys'])}")
    
    print(f"\n📋 EMPLOYEES TABLE") 
    print(f"   Fields: {len(employees_schema['columns'])}")
    print(f"   Records: {employees_schema['row_count']}")
    print(f"   Foreign Keys: {len(employees_schema['foreign_keys'])}")
    
    print(f"\n📋 ENUMS")
    for enum_name, values in enums.items():
        print(f"   {enum_name}: {', '.join(values)}")

if __name__ == "__main__":
    main()
