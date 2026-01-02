# Medical Mimic Data Mining

 This project implements a comprehensive medical data warehouse for the MIMIC-III Clinical Database using Python, SQLAlchemy, and PostgreSQL. It focuses on the Medallion Architecture (Bronze, Silver, Gold) to transform raw clinical logs into actionable insights.

## 📁 Project Structure

```
project/
├── app/
│   ├── models/bronze/          # SQLAlchemy models (16 tables)
│   ├── transformers/bronze/    # CSV loaders
│   └── shared/                 # Infrastructure (DB, config, logging)
├── scripts/                    # Utility scripts
├── dataset/                    # CSV data files (not in git)
├── docker-compose.yml          # PostgreSQL setup
└── requirements.txt            # Python dependencies
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- Docker & Docker Compose
- MIMIC-III CSV dataset

### 2. Setup

```bash
# Clone and navigate to project
cd data-warehouse/project

# Copy environment template
cp .env.example .env

# Edit .env with your settings (optional)

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux / macOS
source venv/bin/activate
# On Windows
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start PostgreSQL database
docker-compose up -d

# Wait for PostgreSQL to be ready (check logs)
docker-compose logs -f postgres

```

### 3. Initialize Database

```bash
# Create Bronze schema and all tables
python scripts/init_db.py
```

This creates 16 tables in the `bronze` schema:

- Patient demographics (PATIENTS, ADMISSIONS, ICUSTAYS)
- Staff & services (CAREGIVERS, SERVICES, TRANSFERS)
- Dictionaries (D_ITEMS, D_LABITEMS)
- Events (LABEVENTS, INPUTEVENTS_CV, INPUTEVENTS_MV, OUTPUTEVENTS, PRESCRIPTIONS, PROCEDUREEVENTS_MV, MICROBIOLOGYEVENTS, NOTEEVENTS)

### 4. Load Data

```bash
# Load all tables
python scripts/load_bronze.py

# Load specific table
python scripts/load_bronze.py --table PATIENTS

# Custom CSV directory and batch size
python scripts/load_bronze.py --csv-dir ./path/to/csvs --batch-size 5000
```

## 📊 Database Tables

### Core Tables

- **PATIENTS**: Patient demographics
- **ADMISSIONS**: Hospital admissions
- **ICUSTAYS**: ICU stay records

### Event Tables (High Volume)

- **LABEVENTS**: Laboratory test results
- **INPUTEVENTS_CV/MV**: IV fluids and medications (CareVue/MetaVision)
- **OUTPUTEVENTS**: Patient outputs (urine, drainage)
- **PRESCRIPTIONS**: Medication orders
- **PROCEDUREEVENTS_MV**: Medical procedures
- **MICROBIOLOGYEVENTS**: Culture and sensitivity results

### Reference Tables

- **D_ITEMS**: Item definitions
- **D_LABITEMS**: Lab test definitions
- **CAREGIVERS**: Healthcare provider roles

## 🔧 Configuration

Edit `.env` file:

```env
# Database
POSTGRES_USER=mimic_user
POSTGRES_PASSWORD=mimic_password
POSTGRES_DB=mimic_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Data
CSV_DATA_PATH=./dataset
BATCH_SIZE=1000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Access PostgreSQL
docker exec -it mimic_postgres psql -U mimic_user -d mimic_db

# Access pgAdmin
# Navigate to http://localhost:5050
# Login: admin@mimic.local / admin
```

## 📝 Usage Examples

### Python API

```python
from app.shared import get_db
from app.models.bronze import BronzePatients

# Query patients
with next(get_db()) as db:
    patients = db.query(BronzePatients).limit(10).all()
    for patient in patients:
        print(f"Patient {patient.subject_id}: {patient.gender}")
```

### SQL Queries

```sql
-- View all tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'bronze' ORDER BY table_name;

-- Count patients
SELECT COUNT(*) FROM bronze.patients;

-- Admissions with Sepsis diagnosis
SELECT * FROM bronze.admissions 
WHERE diagnosis ILIKE '%sepsis%' 
LIMIT 10;
```

## 🏗️ Architecture

### High-Level Vision

 ![High Level Architecture](../conception/HIGH_LEVEL_ARCH.png)

 The ultimate vision for **Medical Mimic Data Mining** extends beyond a traditional Data Warehouse. The goal is to build a comprehensive **Data-Driven Ecosystem** comprising three interconnected pillars:

1. **Data Warehouse Module** (Current Focus): The central source of truth, ingesting and structuring clinical data (Bronze/Silver/Gold).
2. **AI-Models Cluster**: A dedicated environment for training and serving predictive models (e.g., Sepsis Prediction, Mortality Risk) using the clean data from the Gold Layer.
3. **Full-Stack Application**: A clinician-facing portal to visualize insights and real-time alerts.

### Data Flow

1. **CSV Files** → **Bronze Loaders** → **PostgreSQL (Bronze Schema)**
2. **Batch Processing**: Data loaded in configurable batch sizes
3. **Error Handling**: Skip malformed rows, log errors
4. **Audit Fields**: All tables have `created_at` and `updated_at` timestamps

### Design Patterns

- **Dependency Injection**: IoC container for shared resources
- **Repository Pattern**: Separate data access from business logic
- **Factory Pattern**: SessionLocal for database sessions

## 🧪 Testing

```bash
# Test database connection
python -c "from app.shared import test_connection; print(test_connection())"

# Test single table load
python scripts/load_bronze.py --table PATIENTS --batch-size 10
```

### Test the jupiter files :

1. Activate venv env :

```bash
source venv/scripts/activate  
```

2. Register the kernel for Jupyter

```bash
python -m ipykernel install --user --name=mimic-venv --display-name="MIMIC Data Warehouse (venv)"
```

## 📚 References

- [MIMIC-III Documentation](https://mimic.mit.edu/docs/iii/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

## 🤝 Contributing

1. Follow PEP 8 style guide
2. Add type hints to all functions
3. Update docstrings for new classes/functions
4. Test before committing

## 📄 License

This project follows the MIMIC-III data use agreement. Ensure you have proper access credentials before using the dataset.
