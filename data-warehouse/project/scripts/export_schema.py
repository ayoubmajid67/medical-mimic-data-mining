"""Export database schema as SQL DDL."""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.schema import CreateSchema, CreateTable

from app.models.bronze import Base
from app.shared import logger


def export_schema(output_file: Path = None):
    """
    Export Bronze schema as SQL DDL.
    
    Args:
        output_file: Path to output SQL file. If None, prints to stdout.
    """
    logger.info("Generating SQL DDL for Bronze schema...")
    
    sql_statements = []
    
    # Create schema statement
    sql_statements.append("-- Create Bronze Schema")
    sql_statements.append("CREATE SCHEMA IF NOT EXISTS bronze;")
    sql_statements.append("")
    
    # Create table statements
    for table in Base.metadata.sorted_tables:
        sql_statements.append(f"-- Table: {table.name}")
        create_table = str(CreateTable(table).compile(compile_kwargs={"literal_binds": True}))
        sql_statements.append(create_table + ";")
        sql_statements.append("")
    
    full_sql = "\n".join(sql_statements)
    
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(full_sql, encoding="utf-8")
        logger.info(f"Schema exported to: {output_file}")
    else:
        print(full_sql)
    
    return full_sql


if __name__ == "__main__":
    output = Path("schema_bronze.sql") if len(sys.argv) > 1 else None
    export_schema(output)
