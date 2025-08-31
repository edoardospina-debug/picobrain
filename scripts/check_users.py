#!/usr/bin/env python3
"""
Check what users actually exist in the database
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json

print("=" * 60)
print("CHECKING ACTUAL DATABASE USERS")
print("=" * 60)

try:
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="picobrain_db",
        user="postgres",
        password="postgres",
        cursor_factory=RealDictCursor
    )
    
    with conn.cursor() as cur:
        # Get all users
        cur.execute("""
            SELECT 
                id,
                username,
                email,
                full_name,
                role,
                is_active,
                created_at
            FROM users
            ORDER BY created_at;
        """)
        
        users = cur.fetchall()
        
        if users:
            print(f"\n✅ Found {len(users)} users in database:\n")
            for user in users:
                print(f"  Username: {user['username']}")
                print(f"  Email:    {user['email']}")
                print(f"  Name:     {user['full_name']}")
                print(f"  Role:     {user['role']}")
                print(f"  Active:   {user['is_active']}")
                print(f"  Created:  {user['created_at']}")
                print("  " + "-" * 40)
        else:
            print("\n❌ No users found in database!")
            print("\nCreating default admin user...")
            
    conn.close()
    
except Exception as e:
    print(f"\n❌ Database error: {e}")
    print("\nMake sure PostgreSQL is running:")
    print("  brew services start postgresql@16")

print("\n" + "=" * 60)
print("NOTE: Passwords are hashed, so we can't see them directly")
print("But we can test login with the backend API")
print("=" * 60)
