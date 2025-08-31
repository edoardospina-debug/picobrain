#!/usr/bin/env python3
"""
Initialize Currencies Table - Fix database setup issue
"""

import asyncio
import aiohttp
import psycopg2
from psycopg2 import sql

# Database connection
DB_CONFIG = {
    "host": "localhost",
    "database": "picobrain",
    "user": "picobrain",
    "password": "picobrain123"  # Update if different
}

def initialize_currencies_table():
    """Create and populate the currencies table"""
    try:
        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Connected to PostgreSQL database")
        
        # Create currencies table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS currencies (
            currency_code VARCHAR(3) PRIMARY KEY,
            currency_name VARCHAR(100) NOT NULL,
            symbol VARCHAR(10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(create_table_query)
        print("✅ Currencies table created/verified")
        
        # Insert common currencies
        currencies = [
            ('USD', 'US Dollar', '$'),
            ('EUR', 'Euro', '€'),
            ('GBP', 'British Pound', '£'),
            ('CAD', 'Canadian Dollar', 'C$'),
            ('AUD', 'Australian Dollar', 'A$'),
            ('JPY', 'Japanese Yen', '¥'),
            ('CNY', 'Chinese Yuan', '¥'),
            ('CHF', 'Swiss Franc', 'CHF'),
            ('INR', 'Indian Rupee', '₹'),
            ('MXN', 'Mexican Peso', '$'),
        ]
        
        insert_query = """
        INSERT INTO currencies (currency_code, currency_name, symbol) 
        VALUES (%s, %s, %s)
        ON CONFLICT (currency_code) DO NOTHING;
        """
        
        for currency in currencies:
            cursor.execute(insert_query, currency)
        
        conn.commit()
        print(f"✅ Inserted {len(currencies)} currencies")
        
        # Verify currencies
        cursor.execute("SELECT currency_code, currency_name FROM currencies")
        results = cursor.fetchall()
        print("\nAvailable currencies:")
        for code, name in results:
            print(f"  • {code}: {name}")
        
        cursor.close()
        conn.close()
        print("\n✅ Database setup complete!")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        # Try alternative approach through API
        print("\nAttempting to fix through API instead...")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def verify_api_currencies():
    """Verify currencies are accessible through API"""
    async with aiohttp.ClientSession() as session:
        # Login
        print("\nVerifying through API...")
        data = aiohttp.FormData()
        data.add_field('username', 'admin@picobrain.com')
        data.add_field('password', 'admin123')
        
        try:
            async with session.post(
                "http://localhost:8000/api/v1/auth/login", 
                data=data
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    token = result['access_token']
                    print("✅ API authentication successful")
                    
                    # Try to get currencies if endpoint exists
                    headers = {"Authorization": f"Bearer {token}"}
                    async with session.get(
                        "http://localhost:8000/api/v1/currencies",
                        headers=headers
                    ) as curr_resp:
                        if curr_resp.status == 200:
                            currencies = await curr_resp.json()
                            print(f"✅ Found {len(currencies)} currencies via API")
                        else:
                            print(f"⚠️ Currencies endpoint returned: {curr_resp.status}")
                else:
                    print(f"❌ API authentication failed: {resp.status}")
        except Exception as e:
            print(f"⚠️ API verification error: {e}")

def main():
    print("=" * 60)
    print("FIXING DATABASE - CREATING CURRENCIES TABLE")
    print("=" * 60)
    
    # Try to create currencies table
    success = initialize_currencies_table()
    
    if success:
        # Verify through API
        asyncio.run(verify_api_currencies())
        print("\n✅ Database is now ready for employee migration!")
        print("You can now run the migration scripts again.")
    else:
        print("\n⚠️ Could not create currencies table directly.")
        print("The database might require different credentials or permissions.")
        print("\nAlternative solutions:")
        print("1. Check database credentials in backend/.env")
        print("2. Run database migrations manually")
        print("3. Contact database administrator")

if __name__ == "__main__":
    main()
