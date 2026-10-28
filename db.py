"""
This module handles database operations for the Reflections application.

- Connects to the SQLite database (reflections.db).
- Initialises database tables using schema.sql.
- Adds activities and entries, and retrieves entries for a specific day.
- Enables foreign key constraints to maintain database relationships.
- Provides functions for main.py to use in Flask routes.
Dependencies:sqlite3, pathlib
Author: Gyalzin Dorji
Created: 2026-10-23
Last Modified: 2026-10-24
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
    
    
# This function retrieves the activity_id for a given activity_name from the activity table.
# If the activity_name does not exist in the table, it creates a new activity with the given activity_name and category_id, and returns the new activity_id.
# It takes two parameters:
# - activity_name: the name of the activity to retrieve or create.
# - category_id: the category ID to use when creating a new activity (default is 1).
# It executes a SELECT SQL command to check if the activity_name exists in the table. If it does, it retrieves the activity_id. 
# If it does not, it executes an INSERT SQL command to create a new activity and retrieves the new activity_id. It commits the changes to the database and closes the connection.

def get_or_create_activity(activity_name, category_id = 1):
    conn = get_connection()
    row = (conn.execute(
        "SELECT activity_id FROM activity WHERE activity_name = ?", (activity_name,)
    )).fetchone()
    if row:
        activity_id = row["activity_id"]
    else:
        cur = conn.execute(
            "INSERT INTO activity (activity_name, category_id) VALUES (?,?)", (activity_name, category_id),
        )
        conn.commit()
        activity_id = cur.lastrowid
    conn.close()
    return activity_id

# This function deletes an entry from the entry table in the database based on the provided entry_id.
# It takes one parameter: entry_id, which is the ID of the entry to be deleted
# It executes a DELETE SQL command to remove the entry from the database.

def delete_entry(entry_id):
    conn = get_connection()
    conn.execute("DELETE FROM entry where entry_id = ?", (entry_id,))
    conn.commit()
    conn.close()
    
# This function retrieves a specific entry from the entry table in the database based on the provided entry_id.
# It takes one parameter: entry_id, which is the ID of the entry to be retrieved
# It executes a SELECT SQL command to retrieve the entry from the database, joining with the activity table to get the activity_name associated with the entry.
# It returns a single row as a sqlite3.Row object that allows us to access the columns by name. 
# It closes the connection after retrieving the data.   
    
def get_entry(entry_id):
    conn = get_connection()
    row = conn.execute("""SELECT entry.*, activity.activity_name 
                       FROM entry
                       JOIN activity ON entry.activity_id = activity.activity_id
                       WHERE entry.entry_id = ?""", (entry_id,),).fetchone()
    conn.close()
    return row
    
  
  
# This function updates an existing entry in the entry table in the database based on the provided entry_id.
# It executes an UPDATE SQL command to modify the entry in the database with the new values provided for activity_id, start_time, end_time, mood, and note.
# It commits the changes to the database and closes the connection.
  
def update_entry(entry_id, activity_id, start_time, end_time, mood, note):
    conn = get_connection()
    conn.execute(
        """UPDATE entry
           SET activity_id = ?, start_time = ?, end_time = ?, mood = ?, note = ?
           WHERE entry_id = ?""",
        (activity_id, start_time, end_time, mood, note, entry_id),)
    conn.commit()
    conn.close()