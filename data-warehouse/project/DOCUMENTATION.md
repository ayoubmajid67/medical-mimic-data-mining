# MIMIC-III Data Warehouse - Complete Documentation

A comprehensive data warehouse implementation for MIMIC-III Clinical Database using the Medallion Architecture pattern (Bronze → Silver → Gold layers).

---

## Table of Contents

1. [Quick Start](#-quick-start)
2. [Project Structure](#-project-structure)
3. [Architecture Overview](#️-architecture-overview)
4. [Configuration](#️-configuration)
5. [Scripts Reference](#-scripts-reference)
6. [Data Loading Deep Dive](#-data-loading-deep-dive)
7. [Batch Processing Explained](#-batch-processing-explained)
8. [Commands Reference](#-commands-reference)
9. [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Git

### Running with Docker (Recommended)

```bash
# 1. Clone and navigate to project
cd project

# 2. Copy environment file
cp .env.example .env

# 3. Start all services
docker compose up -d

# 4. Initialize database schema
docker compose run --rm app python -m scripts.init_db

# 5. Load data into bronze layer
docker compose run --rm app python -m scripts.load_bronze
```

### Access Points
| Service | URL | Credentials |
|---------|-----|-------------|
| PostgreSQL | `localhost:5432` | `mimic_user` / `mimic_password` |
| pgAdmin | http://localhost:5050 | `admin@mimic.com` / `admin` |

---

## 📁 Project Structure

```
project/
├── app/                          # Main application code
│   ├── models/                   # SQLAlchemy models
│   │   └── bronze/              # Bronze layer (raw data)
│   │       ├── admissions.py    # Hospital admissions
│   │       ├── caregivers.py    # Healthcare providers
│   │       ├── dictionaries.py  # D_ITEMS, D_LABITEMS
│   │       ├── icustays.py      # ICU stays
│   │       ├── inputevents.py   # CV & MV input events
│   │       ├── labevents.py     # Lab test results
│   │       ├── microbiologyevents.py
│   │       ├── noteevents.py    
│   │       ├── outputevents.py  # Patient outputs
│   │       ├── patients.py      # Patient demographics
│   │       ├── prescriptions.py # Medications
│   │       ├── procedureevents.py
│   │       ├── procedures_icd.py # ICD-9 codes
│   │       ├── services.py      # Medical services
│   │       └── transfers.py     # Patient transfers
│   ├── shared/                  # Shared infrastructure
│   │   ├── config.py           # Configuration management
│   │   ├── db_engine.py        # Database connection
│   │   └── logger.py           # Logging setup
│   └── transformers/           # ETL transformers
│       └── bronze/
│           └── base_loader.py  # Core CSV loading logic
├── scripts/                     # Utility scripts
│   ├── init_db.py              # Initialize database
│   ├── load_bronze.py          # Load CSV to bronze
│   ├── benchmark_loading.py    # Performance testing
│   └── verify_setup.py         # Verify installation
├── dataset/                     # MIMIC-III CSV files
├── docker-compose.yml          # Docker services
├── Dockerfile                  # App container
├── requirements.txt            # Python dependencies
└── .env.example               # Environment template
```

---

## 🏗️ Architecture Overview

### Medallion Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MIMIC-III CSV Files                      │
│  (PATIENTS, ADMISSIONS, ICUSTAYS, LABEVENTS, etc.)         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     BRONZE LAYER                            │
│  Raw data ingestion - 1:1 mapping from CSV files           │
│  Schema: bronze.*                                           │
│  Tables: 16 tables matching source files                   │
└───────────────────────────┬─────────────────────────────────┘
                            │ (Cleaning & Standardization)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     SILVER LAYER                            │
│  Cleaned, validated, conformant data                       │
│  Schema: silver.*                                          │
│  (To be implemented)                                       │
└───────────────────────────┬─────────────────────────────────┘
                            │ (Aggregation & Business Logic)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      GOLD LAYER                             │
│  Business-ready aggregates & analytics                     │
│  Schema: gold.*                                            │
│  (To be implemented)                                       │
└─────────────────────────────────────────────────────────────┘
```

### Bronze Layer Tables (16 total)

| Category | Table | CSV File | Description |
|----------|-------|----------|-------------|
| **Demographics** | PATIENTS | PATIENTS.csv | Patient demographics |
| | ADMISSIONS | ADMISSIONS.csv | Hospital admissions |
| | ICUSTAYS | ICUSTAYS.csv | ICU stays |
| **Staff/Services** | CAREGIVERS | CAREGIVERS.csv | Healthcare providers |
| | SERVICES | SERVICES.csv | Medical service assignments |
| | TRANSFERS | TRANSFERS.csv | Patient transfers |
| **Dictionaries** | D_ITEMS | D_ITEMS.csv | Item definitions |
| | D_LABITEMS | D_LABITEMS.csv | Lab item definitions |
| **Events** | LABEVENTS | LABEVENTS.csv | Lab test results |
| | INPUTEVENTS_CV | INPUTEVENTS_CV.csv | Inputs (CareVue system) |
| | INPUTEVENTS_MV | INPUTEVENTS_MV.csv | Inputs (MetaVision system) |
| | OUTPUTEVENTS | OUTPUTEVENTS.csv | Patient outputs |
| | PRESCRIPTIONS | PRESCRIPTIONS.csv | Medications |
| | PROCEDUREEVENTS_MV | PROCEDUREEVENTS_MV.csv | Procedures |
| | MICROBIOLOGYEVENTS | MICROBIOLOGYEVENTS.csv | Microbiology |
| **Codes** | PROCEDURES_ICD | PROCEDURES_ICD.csv | ICD-9 procedure codes |

---

## ⚙️ Configuration

All configuration is managed via environment variables. Copy `.env.example` to `.env`:

```bash
# Database Configuration
POSTGRES_USER=mimic_user
POSTGRES_PASSWORD=mimic_password
POSTGRES_DB=mimic_db
POSTGRES_HOST=localhost        # Use 'postgres' in Docker
POSTGRES_PORT=5432

# Application
ENV=development
LOG_LEVEL=INFO
CSV_DATA_PATH=./dataset
BATCH_SIZE=1000                # ← Controls batch processing

# Database Connection Pool
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_RECYCLE=3600
```

---

## 📜 Scripts Reference

### Overview

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `init_db.py` | Creates database schemas and tables | First-time setup |
| `load_bronze.py` | Loads CSV files into bronze tables | Data ingestion |
| `benchmark_loading.py` | Tests loading performance | Performance tuning |
| `verify_setup.py` | Validates installation | Troubleshooting |
| `example_queries.py` | Sample SQL queries | Learning/Demo |

---

### `load_bronze.py` - Production Data Loader

**Purpose**: Main script for loading CSV data into the Bronze layer. Designed for production use with full control over what and how to load.

**Features**:
- Load all tables or a specific table
- Configurable batch size via CLI or environment
- Progress logging and statistics
- Error handling with detailed reporting

**Usage**:
```bash
# Load ALL tables
python -m scripts.load_bronze

# Load specific table
python -m scripts.load_bronze --table PATIENTS

# Custom batch size (override .env)
python -m scripts.load_bronze --batch-size 500

# Custom CSV directory
python -m scripts.load_bronze --csv-dir /path/to/data

# Full example
python -m scripts.load_bronze --table LABEVENTS --batch-size 2000 --csv-dir ./dataset
```

**Output Example**:
```
=== Loading Statistics ===
PATIENTS:
  Total rows: 100
  Loaded: 100
  Errors: 0

ADMISSIONS:
  Total rows: 129
  Loaded: 129
  Errors: 0
```

---

### `benchmark_loading.py` - Performance Testing

**Purpose**: Finds the optimal batch size for your system by testing different values and measuring performance (rows/second).

**How It Works**:
1. Selects a small table (CAREGIVERS) for testing
2. Tests multiple batch sizes: [100, 500, 1000, 5000]
3. Measures duration and calculates rows/second
4. Reports the optimal batch size

**Usage**:
```bash
python -m scripts.benchmark_loading
```

**Output Example**:
```
=== Bronze Layer Performance Benchmark ===
Table: CAREGIVERS

Testing batch size: 100
Duration: 0.45s
Rows/sec: 222.22

Testing batch size: 500
Duration: 0.22s
Rows/sec: 454.55

Testing batch size: 1000
Duration: 0.18s
Rows/sec: 555.56

Testing batch size: 5000
Duration: 0.15s
Rows/sec: 666.67

=== Benchmark Results ===
Optimal batch size: 5000
```

**Key Difference from `load_bronze.py`**:

| Aspect | `load_bronze.py` | `benchmark_loading.py` |
|--------|------------------|------------------------|
| **Purpose** | Production data loading | Performance testing |
| **Tables** | All or specific | Single small table |
| **Batch Size** | Fixed (from config) | Tests multiple values |
| **Output** | Loading statistics | Performance metrics |
| **Use Case** | Daily ETL operations | One-time optimization |

---

## 📊 Data Loading Deep Dive

### The Loading Pipeline

```
CSV File → BaseCSVLoader → Transform → Batch → Database
    │            │              │         │          │
    │            │              │         │          └── Session commit
    │            │              │         └── Group N rows together
    │            │              └── Parse types (str→int, datetime, etc.)
    │            └── Read file, handle errors
    └── Source file (e.g., PATIENTS.csv)
```

### `BaseCSVLoader` Class (Core Engine)

Located in `app/transformers/bronze/base_loader.py`, this class handles all CSV loading:

```python
class BaseCSVLoader:
    def __init__(self, model_class, csv_path, batch_size=1000, skip_errors=True):
        # model_class: SQLAlchemy model (e.g., BronzePatients)
        # csv_path: Path to CSV file
        # batch_size: Rows per database transaction
        # skip_errors: Continue on row errors or fail fast
```

**Key Methods**:

| Method | Purpose |
|--------|---------|
| `parse_value()` | Converts CSV strings to Python types |
| `transform_row()` | Applies field mapping to entire row |
| `read_csv_batches()` | Generator yielding batches of rows |
| `load_batch()` | Inserts batch into database |
| `load()` | Orchestrates full process |

---

## 🔄 Batch Processing Explained

### What is Batch Processing?

Instead of inserting rows one-by-one, we group them into **batches** and commit them together. This dramatically improves performance.

### Without Batching (Slow) ❌

```python
for row in csv_reader:
    session.add(Model(**row))
    session.commit()  # ← Commit after EVERY row = slow!
```

**Problem**: Each `commit()` is a database round-trip. With 1 million rows, that's 1 million round-trips!

### With Batching (Fast) ✅

```python
batch = []
for row in csv_reader:
    batch.append(Model(**row))
    
    if len(batch) >= BATCH_SIZE:
        session.add_all(batch)
        session.commit()  # ← Commit after N rows = fast!
        batch = []
```

**Benefit**: With `BATCH_SIZE=1000`, 1 million rows = only 1,000 round-trips!

### How It Works in Our Code

From `base_loader.py`:

```python
# 1. Read CSV in batches
def read_csv_batches(self, field_mapping):
    batch = []
    for row in reader:
        transformed = self.transform_row(row, field_mapping)
        batch.append(transformed)
        
        if len(batch) >= self.batch_size:  # ← When batch is full
            yield batch                     # ← Return it
            batch = []                      # ← Start new batch
    
    if batch:  # ← Don't forget remaining rows
        yield batch

# 2. Load each batch
def load_batch(self, session, batch):
    for row in batch:
        instance = self.model_class(**row)
        session.add(instance)
    
    session.commit()  # ← Single commit for entire batch
```

### Choosing the Right Batch Size

| Batch Size | Pros | Cons |
|------------|------|------|
| **Small (100-500)** | Lower memory usage, faster error recovery | More DB round-trips |
| **Medium (1000-2000)** | Good balance | - |
| **Large (5000+)** | Fewer round-trips, faster overall | Higher memory, longer rollbacks |

**Recommendation**: Start with `BATCH_SIZE=1000`, use `benchmark_loading.py` to optimize.

### Error Handling in Batches

```python
skip_errors = True  # Default behavior

# If a row fails:
# - Log the error
# - Skip that row
# - Continue with the rest of the batch
# - Commit successful rows
```

Statistics track everything:
```python
stats = {
    "total": 10000,   # Total rows in CSV
    "loaded": 9998,   # Successfully inserted
    "errors": 2       # Failed rows (logged)
}
```

---

## 🔧 Commands Reference

### Docker Commands

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f
docker compose logs -f postgres   # Specific service

# Stop services
docker compose down

# Rebuild and start
docker compose up -d --build

# Run scripts
docker compose run --rm app python -m scripts.init_db
docker compose run --rm app python -m scripts.load_bronze
docker compose run --rm app python -m scripts.load_bronze --table PATIENTS
docker compose run --rm app python -m scripts.benchmark_loading
docker compose run --rm app python -m scripts.verify_setup
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run scripts
python -m scripts.init_db
python -m scripts.load_bronze
python -m scripts.verify_setup
```

---

## 🔍 Troubleshooting

### Database Connection Failed
```bash
# Check if PostgreSQL is running
docker compose ps

# Check logs
docker compose logs postgres
```

### Permission Denied on Dataset
```bash
# Ensure read permissions
chmod -R 644 dataset/*.csv
```

### Out of Memory During Loading
```bash
# Reduce batch size in .env
BATCH_SIZE=500
```

### Slow Loading Performance
```bash
# Run benchmark to find optimal batch size
python -m scripts.benchmark_loading

# Increase batch size if memory allows
BATCH_SIZE=5000
```

### PostgreSQL Volume Issues
```bash
# Remove old volumes and start fresh
docker compose down
docker volume rm mimic-data-warehouse-composer_postgres_data
docker compose up -d
```

---

## 📚 Additional Resources

- [MIMIC-III Documentation](https://mimic.mit.edu/docs/iii/)
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)
- [Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Performance_Optimization)
