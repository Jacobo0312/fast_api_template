from sqlalchemy import Table, Column, Integer, String
from src.database.db import meta,engine

records = Table(
    "recordsJacobo2",
    meta,
    Column("id", String, primary_key=True),
    Column("timestamp", String),
    Column("method", String),
    Column("path", String),
    Column("query_params", String),
    Column("request_body", String),
    Column("response", String),
)

meta.create_all(engine)
