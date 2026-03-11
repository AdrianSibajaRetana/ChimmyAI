"""Cache SQLite para resultados de geocodificación."""

import sqlite3
from pathlib import Path

_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "geocode_cache.db"


class GeocodeCache:
    """Cache permanente de geocodificación usando SQLite."""

    def __init__(self, db_path: Path = _DB_PATH) -> None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS geocode (
                query   TEXT PRIMARY KEY,
                lat     REAL NOT NULL,
                lon     REAL NOT NULL,
                name    TEXT NOT NULL,
                country TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def get(self, query: str) -> dict | None:
        row = self._conn.execute(
            "SELECT lat, lon, name, country FROM geocode WHERE query = ?",
            (query.lower(),),
        ).fetchone()
        if row is None:
            return None
        return dict(row)

    def put(self, query: str, lat: float, lon: float, name: str, country: str) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO geocode (query, lat, lon, name, country) VALUES (?, ?, ?, ?, ?)",
            (query.lower(), lat, lon, name, country),
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()
