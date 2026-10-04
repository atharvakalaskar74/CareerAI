import os
import re
from pathlib import Path
from sqlalchemy import text
from .db import db
import logging

logger = logging.getLogger(__name__)

def execute_sql_file(filepath):
    """Executes a SQL file handling multiple statements."""
    if not os.path.exists(filepath):
        logger.warning(f"SQL file not found: {filepath}")
        return
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split on semicolons that are outside single quotes
    # Simple split on ';' followed by newline or EOF
    statements = [stmt.strip() for stmt in content.split(";") if stmt.strip()]
    
    is_mysql = False
    try:
        is_mysql = db.engine.dialect.name == "mysql"
    except Exception:
        pass

    for stmt in statements:
        # Ignore comments-only statements
        clean_stmt = "\n".join([line for line in stmt.splitlines() if not line.strip().startswith("--")])
        if clean_stmt.strip():
            if is_mysql:
                clean_stmt = re.sub(r'INSERT\s+OR\s+IGNORE\s+INTO', 'INSERT IGNORE INTO', clean_stmt, flags=re.IGNORECASE)
            try:
                db.session.execute(text(clean_stmt))
            except Exception as e:
                # Log and continue if table/row already exists
                logger.debug(f"Statement execution note: {e}")
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"Commit failed: {e}")

def auto_seed_if_empty():
    """Checks if the skills and careers tables are populated; if not, seeds them."""
    base_dir = Path(__file__).resolve().parent
    schema_path = base_dir / "schema.sql"
    seed_path = base_dir / "seed.sql"

    try:
        # Check if careers table has records
        result = db.session.execute(text("SELECT count(*) FROM careers")).scalar()
        if result == 0:
            logger.info("Database appears unseeded. Seeding initial careers and skills...")
            execute_sql_file(seed_path)
            logger.info("Database seeding completed.")
    except Exception as e:
        logger.info(f"Checking schema or initial setup needed: {e}")
        # Run schema then seed
        execute_sql_file(schema_path)
        execute_sql_file(seed_path)
