# This is the main application file for a Flask web application that allows users to log and manage their daily activities, moods, and notes.
# It imports necessary modules, sets up routes for the application, and defines functions to handle user interactions with the application.
# The application uses a SQLite database to store activity entries and provides functionality to add, edit, and delete entries.
# Created: 2026-10-23
# Last Modified: 2026-10-28
# Created by: Gyalzin Dorji

from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date, timedelta
import db

app = Flask(__name__)

# This route handles the home page of the application.
# It retrieves the day from the query parameters or defaults to today's date. 

@app.route('/')
def home():
    day = request.args.get('day', date.today().isoformat())  # Get the day from query parameters or use today's date
    return render_day(day)


# This function handles submitting a new activity entry from the web form. 
# It retrieves the activity name, start and end times, mood, and optional note from the submitted form, then converts the values into the appropriate formats. 
# It calls validate_entry() to check for errors; if any are found, it redisplays the page with the errors and the user's existing form data. 
# If validation passes, it gets or creates the activity in the database, saves the entry, and redirects the user to that day's timeline.

@app.route('/save_entry', methods = ['POST'])
def save_entry():
    activity = request.form['activity']
    start_time = request.form['start_time']
    start_time = start_time.replace('T', ' ') + ':00' # Convert to datetime format
    end_time = request.form['end_time']
    end_time = end_time.replace('T', ' ') + ':00' # Convert to datetime format
    mood = request.form.get('mood')
    mood = int(mood) if mood else None # Convert mood to integer if it exists, otherwise set to None
    note = request.form.get('note')
    note = note if note else None # Set note to None if it doesn't exist
    
    errors = validate_entry(activity, start_time, end_time, mood)
    if errors:
        return render_day(start_time[:10], errors = errors, form = request.form)
    
    
    activity_id = db.get_or_create_activity(activity)
    db.add_entry(activity_id, start_time, end_time, mood, note)
    return redirect(url_for('home', day = start_time[:10]))


# This route handles the deletion of an entry from the database.
# It takes the entry_id as a parameter from the URL and calls the delete_entry function from the db module to remove the entry from the database. 
# After deleting the entry, it redirects the user back to the home page, preserving the current day in the query parameters.

@app.route('/delete_entry/<int:entry_id>', methods = ['POST'])
def remove_entry(entry_id):
    db.delete_entry(entry_id)
    day = request.form.get('day', date.today().isoformat())
    return redirect(url_for('home',day = day))


# This route handles the editing of an entry in the database.
# It takes the entry_id as a parameter from the URL and retrieves the corresponding entry from the database using the get_entry function from the db module. 
# If the entry does not exist, it redirects the user back to the home page. Otherwise, it renders the 'edit.html' template with the retrieved entry data, allowing the user to edit the entry.

@app.route('/edit_entry/<int:entry_id>')
def edit_entry(entry_id):
    entry = db.get_entry(entry_id)
    if entry is None:
        return redirect(url_for('home'))
    return render_template('edit.html', entry = entry)


# This route handles the saving of changes made to an existing entry in the database.
# It takes the entry_id as a parameter from the URL and retrieves the updated form data from the request object. 
# It processes the form data, updates the corresponding entry in the database using the update_entry function from the db module.
# It also checks for errors

@app.route('/update_entry/<int:entry_id>', methods = ['POST'])
def save_changes(entry_id):
    activity = request.form['activity']
    start_time = request.form['start_time'].replace('T', ' ') + ':00' # Convert to datetime format
    end_time = request.form['end_time'].replace('T', ' ') + ':00' # Convert to datetime format
    mood = request.form.get('mood')
    mood = int(mood) if mood else None # Convert mood to integer if it exists, otherwise set to None
    note = request.form.get('note') or None # Set note to None if it doesn't exist
    
    errors = validate_entry(activity, start_time, end_time, mood)
    if errors:
        entry = {
            'entry_id' : entry_id,
            'activity_name' : activity,
            'start_time' : start_time,
            'end_time' : end_time,
            'mood' : mood,
            'note' : note,
        }
        return render_template('edit.html', entry = entry, errors = errors)
    
    activity_id = db.get_or_create_activity(activity)
    db.update_entry(entry_id, activity_id, start_time, end_time, mood, note)
    return redirect(url_for ('home', day = start_time[:10])) # Redirect to the home page with the day of the updated entry. It extracts the date part from the start_time string (first 10 characters) to use as the day parameter in the redirect URL.


# This function checks whether an activity entry is valid and collects any errors in a list. 
# It checks that the activity name isn't empty, that the end time comes after the start time, and that the mood is between 1 and 5 if one is provided.
# Finally, it returns the list of errors, which will be empty if all checks pass.

def validate_entry(activity, start_time, end_time, mood):
    errors = []
    if not activity.strip():
        errors.append("Please give the activity a name.")
    if end_time <=start_time:
        errors.append("The end time needs to come after the start time.")
    elif start_time[:10] != end_time[:10]:
        errors.append("An activity needs to start and end on the same day. You can add a second entry for the next day.")
    if mood is not None and not 1 <= mood <= 5:
        errors.append("Mood should be a number from 1 to 5.")
    return errors



# Converts a timestamp into the number of minutes since midnight by extracting the hour and minute. Returns the result as an integer.
def minutes_since_midnight(timestamp):
    return int(timestamp[11:13]) * 60 + int(timestamp[14:16])
    
# This function prepares everything needed to display a particular day's activity timeline.
# It converts the date string into a date object, calculates the previous and next days, retrieves the day's activities from the database, and passes all this information to index.html using render_template(). 
# The errors and form parameters are optional, allowing the page to display validation errors and preserve previously entered form data when needed.
# Prepares and displays a day's timeline by retrieving entries from the database and calculating their position and height as percentages of a 24-hour timeline. 
# It also determines the previous and next dates and passes the data, errors, and form values to the HTML template for rendering.

def render_day(day, errors = None, form = None):
    current = date.fromisoformat(day)
    prev_day = (current - timedelta(days=1)).isoformat()
    next_day = (current + timedelta(days=1)).isoformat()
    entries = []
    for row in db.get_entries(day):
        entry = dict(row)
        start = minutes_since_midnight(entry['start_time'])
        end = minutes_since_midnight(entry['end_time'])
        entry['top'] = start / 1440 *100
        entry['height'] = max(end - start, 15)/1440 * 100
        entries.append(entry)
    return render_template('index.html', entries = entries, day = day, prev_day = prev_day, next_day = next_day, errors = errors or [], form = form or {})



if __name__ == '__main__':
    app.run(debug=True) 
    
