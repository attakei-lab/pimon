"""Database(schema) configuration package."""
import peewee

engine = peewee.DatabaseProxy()
"""Binding database.

For using actually, bind real-data by ``engine.init()``.
"""
