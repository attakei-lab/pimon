"""Database(schema) configuration package."""
import peewee

engine = peewee.SqliteDatabase(None)
"""Binding database.

For using actually, bind real-data by ``engine.init()``.
"""
