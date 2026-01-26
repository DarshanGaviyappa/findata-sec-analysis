SELECT
    s.adsh as fact_id,
    s.cik,
    s.company_name,
    s.form_type,
    COUNT(DISTINCT t.tag) as tag_count
FROM {{ ref('stg_submissions') }} s
LEFT JOIN {{ source('raw', 'raw_tag') }} t
    ON 1=1
GROUP BY s.adsh, s.cik, s.company_name, s.form_type
LIMIT 10
