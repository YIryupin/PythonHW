from pathlib import Path

from db import DatabaseManager
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

MIGRATIONS_DIR = Path(__file__).parent / "migrations"

def run_migrations() -> None:
    """
    Накатываем все .sql‑миграции из папки migrations в алфавитном порядке.
    Скрипты должны быть ИДЕМПОТЕНТНЫМИ (CREATE TABLE IF NOT EXISTS и т.п.).
    """
    MIGRATIONS_DIR.mkdir(exist_ok=True)
    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

    if not migration_files:
        print("No migrations found.")
        return

    dbManager = DatabaseManager(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
    try:
        for path in migration_files:
            print(f"Applying migration {path.name}...")
            sql = path.read_text(encoding="utf-8")
            dbManager.execute_query(sql)
        print("Migrations applied successfully.")
    finally:
        dbManager.close()

if __name__ == "__main__":
    run_migrations()


