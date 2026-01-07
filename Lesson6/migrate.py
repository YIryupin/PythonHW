# import time
from pathlib import Path

# import psycopg2

from db import DatabaseManager
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


MIGRATIONS_DIR = Path(__file__).parent / "migrations"


# def wait_for_db(max_attempts: int = 10, delay_seconds: int = 3) -> None:
#     """
#     Ждём, пока база данных будет доступна.
#     Полезно при старте через docker-compose, когда контейнер бота поднимается
#     быстрее, чем Postgres.
#     """
#     for attempt in range(1, max_attempts + 1):
#         try:
#             conn = get_connection()
#             conn.close()
#             print("Database is ready.")
#             return
#         except psycopg2.OperationalError as exc:
#             print(f"Database is not ready yet (attempt {attempt}/{max_attempts}): {exc}")
#             time.sleep(delay_seconds)

#     raise RuntimeError("Database is not available after several attempts")


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

    # wait_for_db()
    # conn = get_connection()
    # conn.autocommit = True
    # try:
    #     with conn.cursor() as cur:
    #         for path in migration_files:
    #             print(f"Applying migration {path.name}...")
    #             sql = path.read_text(encoding="utf-8")
    #             cur.execute(sql)
    #     print("Migrations applied successfully.")
    # finally:
    #     conn.close()


if __name__ == "__main__":
    run_migrations()


