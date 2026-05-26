from pathlib import Path

import duckdb

from src.config import PROJECT_ROOT, settings


class DuckDBLoader:
    def __init__(self, db_path: str | None = None):
        resolved = Path(db_path or settings.duckdb_path)
        if not resolved.is_absolute():
            resolved = PROJECT_ROOT / resolved
        resolved.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = str(resolved)

    def load_parquet(self, parquet_path: Path, table_name: str) -> int:
        """Load a Parquet file into a DuckDB table (CREATE OR REPLACE)."""
        con = duckdb.connect(self.db_path)
        try:
            con.execute(
                f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_parquet(?)",
                [str(parquet_path)],
            )
            count = con.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
            return count
        finally:
            con.close()

    def query(self, sql: str) -> list[dict]:
        """Run a SQL query and return results as list of dicts."""
        con = duckdb.connect(self.db_path)
        try:
            result = con.execute(sql)
            columns = [desc[0] for desc in result.description]
            return [dict(zip(columns, row)) for row in result.fetchall()]
        finally:
            con.close()

    def tables(self) -> list[str]:
        """List all tables in the database."""
        con = duckdb.connect(self.db_path)
        try:
            rows = con.execute("SHOW TABLES").fetchall()
            return [row[0] for row in rows]
        finally:
            con.close()
