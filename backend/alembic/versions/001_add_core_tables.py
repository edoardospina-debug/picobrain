"""add_core_tables
Revision ID: 001
Create Date: 2024-xx-xx
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ENUM
import logging

# revision identifiers
revision = '001'
down_revision = None

# Set up logging
logger = logging.getLogger(__name__)

def upgrade():
    # Note: gen_random_uuid() is built-in since PostgreSQL 13
    # No need for uuid-ossp extension in PostgreSQL 17+
    
    logger.info("Creating currencies table")
    op.create_table('currencies',
        sa.Column('currency_code', sa.CHAR(3), primary_key=True),
        sa.Column('currency_name', sa.VARCHAR(100), nullable=False),
        sa.Column('minor_units', sa.Integer, nullable=False),
        sa.Column('decimal_places', sa.Integer, nullable=False),
        sa.Column('symbol', sa.VARCHAR(10)),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    
    logger.info("Creating clinics table")
    op.create_table('clinics',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('code', sa.VARCHAR(10), nullable=False, unique=True),
        sa.Column('name', sa.VARCHAR(100), nullable=False),
        sa.Column('functional_currency', sa.CHAR(3), 
                  sa.ForeignKey('currencies.currency_code', 
                               name='fk_clinics_functional_currency',
                               ondelete='RESTRICT')),
        sa.Column('city', sa.VARCHAR(100)),
        sa.Column('country_code', sa.CHAR(2)),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    
    logger.info("Creating persons table with gender_type ENUM")
    # Let SQLAlchemy create the gender_type ENUM automatically
    op.create_table('persons',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('first_name', sa.VARCHAR(100), nullable=False),
        sa.Column('last_name', sa.VARCHAR(100), nullable=False),
        sa.Column('email', sa.VARCHAR(255), unique=True),
        sa.Column('phone_mobile', sa.VARCHAR(50)),
        sa.Column('dob', sa.Date),
        sa.Column('gender', sa.Enum('M', 'F', 'O', 'N', name='gender_type')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    
    logger.info("Creating clients table")
    op.create_table('clients',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('person_id', UUID(as_uuid=True), 
                  sa.ForeignKey('persons.id', 
                               name='fk_clients_person_id',
                               ondelete='CASCADE'), 
                  nullable=False, unique=True),
        sa.Column('client_code', sa.VARCHAR(20), unique=True),
        sa.Column('acquisition_date', sa.Date, server_default=sa.func.current_date()),
        sa.Column('preferred_clinic_id', UUID(as_uuid=True), 
                  sa.ForeignKey('clinics.id', 
                               name='fk_clients_preferred_clinic_id',
                               ondelete='SET NULL')),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    
    logger.info("Creating employees table with employee_role ENUM")
    # Let SQLAlchemy create the employee_role ENUM automatically
    op.create_table('employees',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('person_id', UUID(as_uuid=True), 
                  sa.ForeignKey('persons.id', 
                               name='fk_employees_person_id',
                               ondelete='CASCADE'), 
                  nullable=False, unique=True),
        sa.Column('employee_code', sa.VARCHAR(20), unique=True),
        sa.Column('primary_clinic_id', UUID(as_uuid=True), 
                  sa.ForeignKey('clinics.id', 
                               name='fk_employees_primary_clinic_id',
                               ondelete='RESTRICT'), 
                  nullable=False),
        sa.Column('role', sa.Enum('doctor', 'nurse', 'receptionist', 'manager', 'finance', 'admin', 
                                   name='employee_role'), nullable=False),
        sa.Column('license_number', sa.VARCHAR(50)),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('TRUE')),
        sa.Column('can_perform_treatments', sa.Boolean, server_default=sa.text('FALSE')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    
    logger.info("Creating users table with user_role ENUM")
    # Let SQLAlchemy create the user_role ENUM automatically
    op.create_table('users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('person_id', UUID(as_uuid=True), 
                  sa.ForeignKey('persons.id', 
                               name='fk_users_person_id',
                               ondelete='CASCADE'), 
                  nullable=False, unique=True),
        sa.Column('username', sa.VARCHAR(50), nullable=False, unique=True),
        sa.Column('password_hash', sa.VARCHAR(255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'manager', 'staff', 'medical', 'finance', 'readonly', 
                                   name='user_role'), nullable=False),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    
    logger.info("Migration 001 upgrade completed successfully")

def downgrade():
    logger.info("Starting migration 001 downgrade")
    
    # Drop tables in reverse order
    tables_to_drop = ['users', 'employees', 'clients', 'persons', 'clinics', 'currencies']
    
    for table in tables_to_drop:
        try:
            op.drop_table(table)
            logger.info(f"Dropped table: {table}")
        except Exception as e:
            logger.warning(f"Could not drop table {table}: {str(e)}")
    
    # Drop ENUMs with CASCADE to handle dependencies
    connection = op.get_bind()
    
    enums_to_drop = ['user_role', 'employee_role', 'gender_type']
    
    for enum_type in enums_to_drop:
        try:
            connection.execute(sa.text(f'DROP TYPE IF EXISTS {enum_type} CASCADE'))
            logger.info(f"Dropped ENUM type: {enum_type}")
        except Exception as e:
            logger.warning(f"Could not drop ENUM {enum_type}: {str(e)}")
    
    logger.info("Migration 001 downgrade completed")