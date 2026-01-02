# Bronze Layer - Quick Reference

## Common Commands

### Setup
```bash
# Start database
docker-compose up -d

# Create tables
python scripts/init_db.py

# Verify setup
python scripts/verify_setup.py
```

### Data Loading
```bash
# Load single table
python scripts/load_bronze.py --table PATIENTS

# Load all tables
python scripts/load_bronze.py

# Custom batch size
python scripts/load_bronze.py --table LABEVENTS --batch-size 5000
```

### Querying
```bash
# Run example queries
python scripts/example_queries.py

# Python interactive
python
>>> from app.shared import get_db
>>> from app.models.bronze import BronzePatients
>>> with next(get_db()) as db:
...     count = db.query(BronzePatients).count()
...     print(f"Patients: {count}")
```

### Database Management
```bash
# PostgreSQL CLI
docker exec -it mimic_postgres psql -U mimic_user -d mimic_db

# Export schema
python scripts/export_schema.py schema_bronze.sql

# View logs
tail -f logs/app.log
```

## SQL Queries

### Count all tables
```sql
SELECT 
    tablename, 
    schemaname
FROM pg_tables 
WHERE schemaname = 'bronze' 
ORDER BY tablename;
```

### Table sizes
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_total_relation_size(schemaname||'.'||tablename) AS bytes
FROM pg_tables 
WHERE schemaname = 'bronze' 
ORDER BY bytes DESC;
```

### Row counts
```sql
SELECT 
    'patients' as table_name, 
    COUNT(*) as row_count 
FROM bronze.patients
UNION ALL
SELECT 'admissions', COUNT(*) FROM bronze.admissions
UNION ALL
SELECT 'icustays', COUNT(*) FROM bronze.icustays;
```

## File Locations

- **Models**: `app/models/bronze/*.py`
- **Loaders**: `app/transformers/bronze/*.py`
- **Config**: `app/shared/config.py`
- **Scripts**: `scripts/*.py`
- **Logs**: `logs/app.log`
- **Data**: `dataset/*.csv`

## Troubleshooting

### Database won't start
```bash
docker-compose down
docker-compose up -d
docker-compose logs -f postgres
```

### Tables not created
```bash
# Check connection
python -c "from app.shared import test_connection; print(test_connection())"

# Re-run init
python scripts/init_db.py
```

### Import errors
```bash
# Ensure you're in project root
cd data-warehouse/project

# Install dependencies
pip install -r requirements.txt
```

### CSV file not found
```bash
# Check path in .env
cat .env | grep CSV_DATA_PATH

# List CSV files
ls dataset/
```

## Model Reference

| Table | Model Class | Primary Key |
|-------|-------------|-------------|
| patients | `BronzePatients` | subject_id |
| admissions | `BronzeAdmissions` | hadm_id |
| icustays | `BronzeICUStays` | icustay_id |
| labevents | `BronzeLabEvents` | row_id |
| inputevents_cv | `BronzeInputEventsCareVue` | row_id |
| inputevents_mv | `BronzeInputEventsMetaVision` | row_id |

See `app/models/bronze/__init__.py` for complete list.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| POSTGRES_HOST | localhost | Database host |
| POSTGRES_PORT | 5432 | Database port |
| POSTGRES_DB | mimic_db | Database name |
| CSV_DATA_PATH | ./dataset | CSV files location |
| BATCH_SIZE | 1000 | Loading batch size |
| LOG_LEVEL | INFO | Logging level |
