"""
This module provides a function to get a connection to the SQLite database.
Author: Gyalzin Dorji
Created: 2024-06-10
Last Modified: 2024-06-10
"""

import sqlite3
from pathlib import Path


# BASE_DIR is the folder where the python file is located. 
# DATABASE is the path to the database file. 
# SCHEMA is the path to the schema.sql file.

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "reflections.db"
SCHEMA = BASE_DIR / "schema.sql"

# This function returns a connection to the SQLite database. 
# It also sets the row factory to sqlite3.Row, which allows us to access the columns by name.
# It also enables foreign key support by executing the PRAGMA foreign_keys = ON command.

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# This function initializes the database by executing the SQL commands in the schema.sql file.
# with open (SCHEMA) as f opens the schema.sql file and reads its contents. The WITH statement ensures that the file is properly closed after its suite finishes, even if an exception is raised.
# Conn.executescript(f.read()) executes the SQL commands in the schema.sql file. The executescript() method allows us to execute multiple SQL commands at once.
# Conn.commit() commits the changes to the database. This is necessary because the executescript() method does not automatically commit the changes.

def init_db():
    with open(SCHEMA) as f:
        conn = get_connection()
        conn.executescript(f.read())
        conn.commit()
        conn.close()