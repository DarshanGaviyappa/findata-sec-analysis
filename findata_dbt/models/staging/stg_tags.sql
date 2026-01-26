SELECT
    tag,
    version,
    tlabel as tag_label
FROM {{ source('raw', 'raw_tag') }}
