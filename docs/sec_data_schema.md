# SEC Financial Statement Data Schema

## Overview
SEC provides financial statement data in 4 related tables, updated quarterly.

## Table Descriptions

### 1. SUB.txt - Submission Information
**Records**: ~6,500 per quarter  
**Purpose**: Company and filing metadata

**Key Columns**:
- `adsh`: Unique submission identifier (Primary Key)
- `cik`: Central Index Key (company identifier)
- `name`: Company name
- `sic`: Standard Industrial Classification code
- `form`: Filing form type (10-K, 10-Q, etc.)
- `period`: Fiscal period end date
- `fy`: Fiscal year
- `fp`: Fiscal period (Q1, Q2, Q3, FY)

### 2. TAG.txt - Tag Definitions
**Records**: ~84,000  
**Purpose**: Financial statement taxonomy/definitions

**Key Columns**:
- `tag`: Tag name (e.g., "Assets", "Revenue")
- `version`: Taxonomy version (e.g., "us-gaap/2024")
- `custom`: Whether tag is custom (0=standard, 1=custom)
- `datatype`: Data type (monetary, shares, etc.)
- `tlabel`: Tag label/description

### 3. NUM.txt - Numeric Values
**Records**: ~3.7 MILLION per quarter  
**Purpose**: Actual financial statement numbers

**Key Columns**:
- `adsh`: Links to SUB (submission identifier)
- `tag`: Links to TAG (financial metric)
- `version`: Taxonomy version
- `ddate`: Data date (as of date)
- `qtrs`: Number of quarters (0=point-in-time, 1=quarterly, 4=annual)
- `uom`: Unit of measure (USD, shares, etc.)
- `value`: The actual numeric value

### 4. PRE.txt - Presentation
**Records**: ~737,000 per quarter  
**Purpose**: How data is presented in statements

**Key Columns**:
- `adsh`: Links to SUB
- `report`: Report number
- `line`: Line number in statement
- `stmt`: Statement type (BS, IS, CF, etc.)
- `tag`: Links to TAG

## Relationships
```
SUB (1) ----< NUM (Many)
  |              |
  |              v
  |           TAG (Lookup)
  |
  +----------< PRE (Many)
                 |
                 v
              TAG (Lookup)
```

## Key Relationships:
- One submission (SUB) has many numeric values (NUM)
- One submission (SUB) has many presentation lines (PRE)
- Numeric values (NUM) reference tags (TAG) for definitions
- Presentation lines (PRE) reference tags (TAG) for display

## Statement Types
- **BS**: Balance Sheet
- **IS**: Income Statement  
- **CF**: Cash Flow Statement
- **EQ**: Statement of Equity
- **CI**: Comprehensive Income

## Denormalization Strategy
For fact tables, we'll JOIN:
- SUB (company info) + NUM (values) + TAG (definitions)
- Filter by statement type and key metrics
- Create separate tables for BS, IS, CF
