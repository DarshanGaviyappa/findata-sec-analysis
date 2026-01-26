-- Staging model for submissions
SELECT
    adsh,
    cik,
    name as company_name,
    form as form_type
FROM {{ source('raw', 'raw_sub') }}
