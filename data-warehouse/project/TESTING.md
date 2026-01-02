# Testing Guide

## Running Tests

### All Tests
```bash
# Run all tests with coverage
python scripts/run_tests.py

# Or use pytest directly
pytest tests/ -v
```

### Specific Test Files
```bash
# Test models only
pytest tests/test_models.py -v

# Test loaders only
pytest tests/test_loaders.py -v

# Test configuration only
pytest tests/test_config.py -v
```

### Coverage Report
```bash
# Generate HTML coverage report
pytest tests/ --cov=app --cov-report=html

# View report
# Open htmlcov/index.html in browser
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_models.py       # Model unit tests
├── test_loaders.py      # Loader unit tests
└── test_config.py       # Configuration tests
```

## Writing New Tests

### Model Test Example
```python
def test_create_patient():
    patient = BronzePatients(
        row_id=1,
        subject_id=10001,
        gender="M",
        dob=datetime(1980, 1, 1),
        expire_flag=False,
    )
    assert patient.subject_id == 10001
```

### Loader Test Example
```python
def test_parse_value_int():
    loader = BaseCSVLoader(BronzePatients, Path("dummy.csv"))
    assert loader.parse_value("123", "int") == 123
```

## Performance Testing

### Benchmark Data Loading
```bash
python scripts/benchmark_loading.py
```

This tests different batch sizes and reports:
- Load duration
- Rows per second
- Optimal batch size

## Integration Testing

### Database Tests (requires running PostgreSQL)
```bash
# Start database
docker-compose up -d

# Run integration tests
pytest tests/ -m integration
```

## Test Markers

Use markers to categorize tests:

```python
@pytest.mark.unit
def test_model_creation():
    pass

@pytest.mark.integration
def test_database_insert():
    pass

@pytest.mark.slow
def test_large_csv_load():
    pass
```

Run specific markers:
```bash
pytest -m unit      # Unit tests only
pytest -m integration  # Integration tests only
pytest -m "not slow"   # Skip slow tests
```

## Continuous Integration

Add to CI/CD pipeline:
```yaml
- name: Run Tests
  run: |
    pip install -r requirements.txt
    pytest tests/ --cov=app
```

## Test Coverage Goals

- **Models**: 90%+ coverage
- **Loaders**: 85%+ coverage
- **Configuration**: 95%+ coverage
- **Overall**: 85%+ coverage

## Troubleshooting Tests

### Import Errors
```bash
# Ensure project root is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Database Connection Errors
```bash
# Check database is running
docker-compose ps

# Check connection
python -c "from app.shared import test_connection; print(test_connection())"
```

### Fixture Errors
```bash
# Clear pytest cache
pytest --cache-clear
```
