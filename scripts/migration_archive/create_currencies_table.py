#!/usr/bin/env python3
"""
Simple script to create and populate the currencies table in PicoBrain database
"""

import psycopg2
from psycopg2 import sql
import sys

# Database configuration
DB_CONFIG = {
    'dbname': 'picobraindb',
    'user': 'edo',
    'password': 'edopico',
    'host': 'localhost',
    'port': 5432
}

def main():
    print("\n" + "="*60)
    print("CREATING CURRENCIES TABLE IN PICOBRAIN DATABASE")
    print("="*60)
    
    try:
        # Connect to database
        print("\nConnecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("✓ Connected successfully")
        
        # Drop existing table if needed (for clean start)
        print("\nDropping existing currencies table if exists...")
        cur.execute("DROP TABLE IF EXISTS currencies CASCADE;")
        conn.commit()
        print("✓ Dropped existing table (if any)")
        
        # Create currencies table
        print("\nCreating currencies table...")
        create_table_sql = """
        CREATE TABLE currencies (
            currency_code CHAR(3) PRIMARY KEY,
            currency_name VARCHAR(100) NOT NULL,
            minor_units INTEGER NOT NULL DEFAULT 100,
            decimal_places INTEGER NOT NULL DEFAULT 2,
            symbol VARCHAR(10),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        cur.execute(create_table_sql)
        conn.commit()
        print("✓ Currencies table created")
        
        # Insert currencies
        print("\nInserting currencies...")
        currencies = [
            ('USD', 'US Dollar', 100, 2, '$'),
            ('EUR', 'Euro', 100, 2, '€'),
            ('GBP', 'British Pound', 100, 2, '£'),
            ('CAD', 'Canadian Dollar', 100, 2, 'C$'),
        ]
        
        insert_sql = """
        INSERT INTO currencies (currency_code, currency_name, minor_units, decimal_places, symbol)
        VALUES (%s, %s, %s, %s, %s);
        """
        
        for currency in currencies:
            cur.execute(insert_sql, currency)
            print(f"  ✓ Inserted {currency[0]} - {currency[1]}")
        
        conn.commit()
        print(f"\n✓ Inserted {len(currencies)} currencies")
        
        # Verify
        print("\nVerifying currencies table...")
        cur.execute("SELECT currency_code, currency_name, symbol FROM currencies ORDER BY currency_code;")
        results = cur.fetchall()
        
        print("\nCurrencies in database:")
        for code, name, symbol in results:
            print(f"  {code}: {name} ({symbol})")
        
        # Check table structure
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'currencies'
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()
        
        print("\nTable structure:")
        for col_name, data_type in columns:
            print(f"  - {col_name}: {data_type}")
        
        cur.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ SUCCESS! Currencies table created and populated")
        print("="*60)
        print("\nYou can now run the employee migration script!")
        
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        print(f"Error code: {e.pgcode if hasattr(e, 'pgcode') else 'N/A'}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
