from sqlalchemy import create_engine, text
from app.config import settings

engine = create_engine(settings.DATABASE_URL)

def seed_data():
    with engine.connect() as conn:
        # Insert currencies
        conn.execute(text("""
            INSERT INTO currencies (currency_code, currency_name, minor_units, decimal_places, symbol) 
            VALUES 
                ('EUR', 'Euro', 100, 2, '€'),
                ('GBP', 'British Pound', 100, 2, '£'),
                ('USD', 'US Dollar', 100, 2, '$')
            ON CONFLICT DO NOTHING;
        """))
        
        # Insert sample clinic
        conn.execute(text("""
            INSERT INTO clinics (code, name, functional_currency, city, country_code)
            VALUES ('LON', 'London Clinic', 'GBP', 'London', 'GB')
            ON CONFLICT DO NOTHING;
        """))
        conn.commit()

if __name__ == "__main__":
    seed_data()
    print("Core data seeded successfully")