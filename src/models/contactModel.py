from sqlalchemy import Table, Column, Integer, String
from src.database.db import meta,engine

contacts = Table(
    "contactsJacobo",
    meta,
    Column("id", Integer, primary_key=True),
    Column("email", String),
    Column("firstname", String),
    Column("lastname", String),
    Column("phone", String),
    Column("website", String),
)

meta.create_all(engine)
