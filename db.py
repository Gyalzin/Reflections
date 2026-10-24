"""
This module contains functions for interacting with the SQLite database.
It provides functions to get a connection to the database, initialize the database, add activities and entries, and retrieve entries.
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
        
        
# This function adds a new activity to the activity table in the database.
# It takes two parameters: activity_name and category_id.
# It executes an INSERT INTO SQL command to add the new activity to the database.
# It commits the changes to the database and closes the connection.

def add_activity(activity_name, category_id):
    conn = get_connection()
    conn.execute("INSERT INTO activity (activity_name, category_id) VALUES (?, ?)", (activity_name, category_id))
    conn.commit()
    conn.close()
    
# This function adds a new entry to the entry table in the database.
# It takes five parameters: activity_id, start_time, end_time, mood, and note
# It executes an INSERT INTO SQL command to add the new entry to the database.
# It commits the changes to the database and closes the connection.
    
def add_entry(activity_id, start_time, end_time, mood = None, note = None):
    conn = get_connection()
    conn.execute("INSERT INTO entry (activity_id, start_time, end_time, mood, note) VALUES (?, ?, ?, ?, ?)", (activity_id, start_time, end_time, mood, note))
    conn.commit()
    conn.close()
    
    
 # This function retrieves all entries from the entry table for a specific day.
 # It takes one parameter: day, which is a string in the format 'YYYY-MM-DD'.
 # It executes a SELECT SQL command to retrieve all entries for the specified day, ordered by start_time.
 # It returns a list of rows, where each row is a sqlite3.Row object that allows us to access the columns by name. It closes the connection after retrieving the data.   

def get_entries(day):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM entry WHERE date(start_time) = ? ORDER BY start_time", (day,)).fetchall()
    conn.close()
    return rows
    
    
    
    