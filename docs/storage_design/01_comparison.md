# Storage Approach Comparison

## Assignment Requirement
Evaluate three approaches for storing SEC financial statement data in Snowflake.

## Three Approaches

### 1. Raw Staging (As-Is Storage)
**Description**: Store data exactly as received from SEC  
**Tables**: SUB, TAG, NUM, PRE (4 tables)  
**Advantages**:
- Preserves original data structure
- Easy to load (direct copy)
- No data loss
- Flexible for any query

**Disadvantages**:
- Requires complex JOINs for analysis
- Not optimized for common queries
- Large table sizes (NUM has 3.7M+ rows)

**Use Case**: Data lake, audit trail, source of truth

---

### 2. JSON Storage (Denormalized Document)
**Description**: Convert to JSON documents, one per company/filing  
**Tables**: FINANCIAL_STATEMENTS_JSON (1 table with VARIANT column)  
**Advantages**:
- Fast single-record retrieval
- Flexible schema
- Easy to add new fields
- Good for APIs

**Disadvantages**:
- Harder to query across companies
- Aggregations are slower
- More storage space
- Complex transformations needed

**Use Case**: API backends, document storage, flexible schemas

---

### 3. Denormalized Fact Tables (Star Schema)
**Description**: Pre-joined tables optimized for analytics  
**Tables**: FACT_BALANCE_SHEET, FACT_INCOME_STATEMENT, FACT_CASH_FLOW (3 tables)  
**Advantages**:
- Optimized for analytics
- Fast aggregations
- Easy to understand
- Best for BI tools

**Disadvantages**:
- Must pre-define metrics
- Less flexible
- Data duplication
- Transformation complexity

**Use Case**: Business intelligence, dashboards, analysis

---

## Recommendation
**Use all three in a layered architecture:**
1. **Raw Staging**: Source of truth
2. **Denormalized Facts**: Analytics layer
3. **JSON**: API layer (optional)
