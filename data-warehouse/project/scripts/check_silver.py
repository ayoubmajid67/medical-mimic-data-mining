"""Check Silver layer tables."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.shared import get_db

def main():
    with get_db() as s:
        print('Silver Layer Tables:')
        print('='*50)
        for r in s.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='silver' ORDER BY table_name")):
            print(f'  - {r[0]}')
    return 0

if __name__ == "__main__":
    sys.exit(main())
