from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date, timedelta
import db

app = Flask(__name__)

# This route handles the home page of the application.
# It retrieves the day from the query parameters or defaults to today's date. 
# It then calculates the previous and next days and retrieves the entries for the specified day from the database. 
# Finally, it renders the 'index.html' template with the retrieved entries and day information.


@app.route('/')
def home():
    day = request.args.get('day', date.today().isoformat())  # Get the day from query parameters or use today's date
    current = date.fromisoformat(day) # Convert the day string to a date object
    prev_day = (current - timedelta(days = 1)).isoformat() 
    next_day = (current + timedelta(days = 1)).isoformat() 
    entries = db.get_entries(day)
    return render_template('index.html', entries=entries, day = day, prev_day = prev_day, next_day = next_day)


# This route handles the form submission for saving a new entry.
# It retrieves the form data from the request object, processes it, and then redirects the user back to the home page.
# This route is defined to handle POST requests to the '/save_entry' URL. It retrieves the activity, start time, end time, mood, and note from the form data. 
# The start and end times are converted to a datetime format by replacing the 'T' character with a space and appending ':00'. The mood is converted to an integer if it exists; otherwise, it is set to None.
# The note is also set to None if it doesn't exist. Finally, the user is redirected back to the home page after processing the form data.

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
    print(f"Activity: {activity}, Start Time: {start_time}, End Time: {end_time}, Mood: {mood}, Note: {note}")
    activity_id = db.get_or_create_activity(activity)
    db.add_entry(activity_id, start_time, end_time, mood, note)
    return redirect(url_for('home'))


# This route handles the deletion of an entry from the database.
# It takes the entry_id as a parameter from the URL and calls the delete_entry function from the db module to remove the entry from the database. 
# After deleting the entry, it redirects the user back to the home page, preserving the current day in the query parameters.

@app.route('/delete_entry/<int:entry_id>', methods = ['POST'])
def remove_entry(entry_id):
    db.delete_entry(entry_id)
    day = request.form.get('day', date.today().isoformat())
    return redirect(url_for('home',day = day))

if __name__ == '__main__':
    app.run(debug=True) 
    