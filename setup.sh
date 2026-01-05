#!/bin/bash

echo "Setting up FinData SEC Analysis project..."

# 1. Create .gitignore
cat > .gitignore << 'EOF'
# Python
venv/
__pycache__/
*.py[cod]
*.so
*.egg-info/
.pytest_cache/
*.pyc

# Environment
.env
*.env
.env.*

# Data files
data/raw/*
data/staging/*
data/processed/*
!data/raw/.gitkeep
!data/staging/.gitkeep
!data/processed/.gitkeep

# Snowflake
profiles.yml
**/profiles.yml

# Airflow
airflow.db
airflow.cfg
logs/

# IDE
.vscode/
.idea/
*.swp
.DS_Store

# Credentials
*.pem
*.key

# Logs
*.log
EOF

echo "✓ Created .gitignore"

# 2. Create .gitkeep files
touch data/raw/.gitkeep
touch data/staging/.gitkeep
touch data/processed/.gitkeep
echo "✓ Created .gitkeep files"

# 3. Create README.md
cat > README.md << 'EOF'
# FinData Inc. - SEC Financial Statement Database

## Team Information
**Team Number:** [Your Team Number]

### Team Members & Contributions
- **Member 1:** [Name] - [Percentage]%
- **Member 2:** [Name] - [Percentage]%  
- **Member 3:** [Name] - [Percentage]%

## Attestation
WE ATTEST THAT WE HAVEN'T USED ANY OTHER STUDENTS' WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.

## Project Overview
Master financial statement database using SEC data, implemented with:
- **Database:** Snowflake
- **Transformation:** DBT
- **Orchestration:** Apache Airflow
- **Frontend:** Streamlit
- **API:** FastAPI

## Quick Start

### Installation
```bash
