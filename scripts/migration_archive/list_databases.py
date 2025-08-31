#!/usr/bin/env python3
"""
List all available databases and check for currencies table
"""

import psycopg2
from psycopg2 import sql

def list_databases():
    """List all available databases"""
    print("=" * 80)
    print("CHECKING AVAILABLE DATABASES")
    print("=" * 80)
    
    # Try different connection approaches
    connection_attempts = [
        {'dbname': 'postgres', 'user': 'edo'},
        {'dbname': 'edo', 'user': 'edo'},
        {'dbname': 'template1', 'user': 'edo'},
        {'dbname': 'picobrain', 'user': 'edo'},
        {'dbname': 'edo_brain', 'user': 'edo'},
        {'dbname': 'edo_brain_3', 'user': 'edo'},
    ]
    
    for attempt in connection_attempts:
        try:
            print(f"\nTrying connection: dbname={attempt['dbname']}, user={attempt['user']}")
            conn = psycopg2.connect(
                dbname=attempt['dbname'],
                user=attempt['user'],
                password='',
                host='localhost',
                port='5432'
            )
            cur = conn.cursor()
            
            print(f"✅ Connected to {attempt['dbname']}!")
            
            # List all databases
            cur.execute("""
                SELECT datname 
                FROM pg_database 
                WHERE datistemplate = false
                ORDER BY datname;
            """)
            databases = cur.fetchall()
            
            print("\n📋 Available databases:")
            for db in databases:
                print(f"  • {db[0]}")
            
            conn.close()
            
            # Now check each database for currencies table
            print("\n🔍 Checking for 'currencies' table in each database:")
            for db_name in databases:
                db_name = db_name[0]
                if db_name.startswith('edo') or 'brain' in db_name.lower() or 'pico' in db_name.lower():
                    try:
                        conn2 = psycopg2.connect(
                            dbname=db_name,
                            user=attempt['user'],
                            password='',
                            host='localhost',
                            port='5432'
                        )
                        cur2 = conn2.cursor()
                        
                        # Check for currencies table
                        cur2.execute("""
                            SELECT EXISTS (
                                SELECT FROM information_schema.tables 
                                WHERE table_schema = 'public' 
                                AND table_name = 'currencies'
                            );
                        """)
                        has_currencies = cur2.fetchone()[0]
                        
                        # Check for employees table
                        cur2.execute("""
                            SELECT EXISTS (
                                SELECT FROM information_schema.tables 
                                WHERE table_schema = 'public' 
                                AND table_name = 'employees'
                            );
                        """)
                        has_employees = cur2.fetchone()[0]
                        
                        status = []
                        if has_currencies:
                            status.append("✅ currencies")
                        if has_employees:
                            status.append("✅ employees")
                        
                        if status:
                            print(f"  {db_name}: {', '.join(status)}")
                        else:
                            print(f"  {db_name}: no relevant tables")
                        
                        conn2.close()
                    except Exception as e:
                        print(f"  {db_name}: ❌ Could not check ({str(e)[:50]})")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            continue
    
    print("\n❌ Could not connect to any database!")
    return False

if __name__ == "__main__":
    list_databases()
