"""Examine SEC data structure"""
import pandas as pd
from pathlib import Path

data_dir = Path("data/raw/sample/2024q4")

print("=" * 80)
print("SEC FINANCIAL STATEMENT DATA STRUCTURE - Q4 2024")
print("=" * 80)

# 1. SUB.txt - Submission information
print("\n1. SUB.txt - Submission/Company Information")
print("-" * 80)
sub_full = pd.read_csv(data_dir / "sub.txt", sep='\t')
sub = sub_full.head(5)
print(f"Shape: {sub_full.shape}")
print(f"Columns ({len(sub.columns)}): {', '.join(sub.columns[:10])}...")
print("\nSample data:")
print(sub[['cik', 'name', 'sic', 'countryba', 'form', 'period']].head(3))

# 2. TAG.txt - Tag definitions
print("\n\n2. TAG.txt - Financial Statement Tags/Taxonomy")
print("-" * 80)
tag_full = pd.read_csv(data_dir / "tag.txt", sep='\t')
tag = tag_full.head(5)
print(f"Shape: {tag_full.shape}")
print(f"Columns ({len(tag.columns)}): {', '.join(tag.columns)}")
print("\nSample data:")
print(tag[['tag', 'version', 'custom', 'abstract', 'datatype']].head(3))

# 3. NUM.txt - Numeric data
print("\n\n3. NUM.txt - Numeric Financial Values")
print("-" * 80)
num_full = pd.read_csv(data_dir / "num.txt", sep='\t')
num = num_full.head(5)
print(f"Shape: {num_full.shape}")
print(f"Columns ({len(num.columns)}): {', '.join(num.columns)}")
print("\nSample data:")
print(num[['adsh', 'tag', 'version', 'ddate', 'qtrs', 'uom', 'value']].head(3))

# 4. PRE.txt - Presentation information
print("\n\n4. PRE.txt - Presentation/Display Information")
print("-" * 80)
pre_full = pd.read_csv(data_dir / "pre.txt", sep='\t')
pre = pre_full.head(5)
print(f"Shape: {pre_full.shape}")
print(f"Columns ({len(pre.columns)}): {', '.join(pre.columns)}")
print("\nSample data:")
print(pre[['adsh', 'report', 'line', 'stmt', 'tag']].head(3))

print("\n" + "=" * 80)
print("KEY RELATIONSHIPS:")
print("=" * 80)
print("""
1. SUB.txt contains company/filing metadata (CIK, name, filing date, period)
2. TAG.txt defines all possible financial statement tags
3. NUM.txt contains actual numeric values linked to submissions via 'adsh'
4. PRE.txt defines how tags are presented in financial statements

Primary Key Relationships:
- SUB: adsh (unique submission identifier)
- TAG: tag + version (unique tag identifier)
- NUM: adsh + tag + ddate + qtrs (links submissions to values)
- PRE: adsh + report + line (presentation order)

For denormalized tables, we'll JOIN:
- SUB (company info) + NUM (values) + TAG (definitions)
""")

print("\n" + "=" * 80)
print("NEXT STEPS:")
print("=" * 80)
print("1. Document this schema in docs/sec_data_schema.md")
print("2. Create ER diagram")
print("3. Design three storage approaches")
print("4. Set up Snowflake and create tables")
