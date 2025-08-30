import psycopg2

# Database connection - no password needed for local setup
conn = psycopg2.connect(
    dbname="picobraindb",
    user="edo",
    host="localhost"
)

def seed_data():
    with conn.cursor() as cur:
        # Insert currencies
        cur.execute("""
            INSERT INTO currencies (currency_code, currency_name, minor_units, decimal_places, symbol) 
            VALUES 
                ('EUR', 'Euro', 100, 2, '€'),
                ('GBP', 'British Pound', 100, 2, '£'),
                ('USD', 'US Dollar', 100, 2, '$'),
                ('CAD', 'Canadian Dollar', 100, 2, 'C$')
            ON CONFLICT (currency_code) DO NOTHING;
        """)
        
        # Insert sample clinics
        cur.execute("""
            INSERT INTO clinics (code, name, functional_currency, city, country_code)
            VALUES 
                ('LON', 'London Clinic', 'GBP', 'London', 'GB'),
                ('MIL', 'Milan Clinic', 'EUR', 'Milan', 'IT'),
                ('NYC', 'New York Clinic', 'USD', 'New York', 'US')
            ON CONFLICT (code) DO NOTHING;
        """)
        
        conn.commit()
        print("✅ Core data seeded successfully")

if __name__ == "__main__":
    seed_data()
    conn.close()