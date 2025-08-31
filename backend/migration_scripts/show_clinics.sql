-- SQL query to inspect clinics table
-- Run with: psql -d picobraindb -f show_clinics.sql

-- Show table structure
\echo '===================================='
\echo 'CLINICS TABLE STRUCTURE'
\echo '===================================='

\d clinics

-- Show all data
\echo ''
\echo '===================================='
\echo 'CLINICS TABLE DATA'
\echo '===================================='

SELECT * FROM clinics ORDER BY code;

-- Show field types and constraints
\echo ''
\echo '===================================='
\echo 'COLUMN DETAILS'
\echo '===================================='

SELECT 
    column_name AS "Field Name",
    data_type AS "Data Type",
    character_maximum_length AS "Max Length",
    is_nullable AS "Nullable",
    column_default AS "Default Value"
FROM information_schema.columns
WHERE table_name = 'clinics'
ORDER BY ordinal_position;

-- Summary
\echo ''
\echo '===================================='
\echo 'SUMMARY'
\echo '===================================='

SELECT 
    COUNT(*) as "Total Clinics",
    COUNT(DISTINCT functional_currency) as "Currencies",
    COUNT(DISTINCT country_code) as "Countries"
FROM clinics;

-- Group by currency
\echo ''
\echo 'Clinics by Currency:'
SELECT functional_currency, COUNT(*) as count 
FROM clinics 
GROUP BY functional_currency 
ORDER BY functional_currency;

-- Group by country
\echo ''
\echo 'Clinics by Country:'
SELECT country_code, COUNT(*) as count 
FROM clinics 
GROUP BY country_code 
ORDER BY country_code;
