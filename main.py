# This is the main application file for a Flask web application that allows users to log and manage their daily activities, moods, and notes.
# It imports necessary modules, sets up routes for the application, and defines functions to handle user interactions with the application.
# The application uses a SQLite database to store activity entries and provides functionality to add, edit, and delete entries.
# Created: 2026-10-23
# Last Modified: 2026-10-31
# Created by: Gyalzin Dorji

from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import date, timedelta, datetime
import db

app = Flask(__name__)
app.secret_key = 'any-long-random-text'  # Set a secret key for session management


# This route handles the home page of the application.
# It retrieves the day from the query parameters or defaults to today's date. 
# It validates the date format and ensures that the day is in ISO format (YYYY-MM-DD).

@app.route('/')
def home():
    day = request.args.get('day', '')
    try:
        date.fromisoformat(day)
    except ValueError:
        day = date.today().isoformat()
    return render_day(day)


# This function handles submitting a new activity entry from the web form. 
# It retrieves the activity name, start and end times, mood, and optional note from the submitted form, then converts the values into the appropriate formats. 
# It calls validate_entry() to check for errors; if any are found, it redisplays the page with the errors and the user's existing form data. 
# If validation passes, it gets or creates the activity in the database, saves the entry, and redirects the user to that day's timeline.
# If someone picks an existing activity, its name goes straight through, and get_or_create_activity finds it. 
# If they pick “Other”, the typed name is used, and a brand-new activity is created under General. Your validation still catches an empty name.
# This route ensures that the user receives feedback after saving an entry, using the flash message mechanism provided by Flask.

@app.route('/save_entry', methods = ['POST'])
def save_entry():
    choice = request.form.get('activity_choice', '')
    if choice == '__other__':
        activity = request.form.get('new_activity', '')
    else:
        activity = choice
    activity = activity.strip()
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
    flash('Saved.')
    return redirect(url_for('home', day = start_time[:10]))


# This route handles the deletion of an entry from the database.
# It takes the entry_id as a parameter from the URL and calls the delete_entry function from the db module to remove the entry from the database. 
# After deleting the entry, it redirects the user back to the home page, preserving the current day in the query parameters.
# It also flashes a message to inform the user that the entry has been deleted.

@app.route('/delete_entry/<int:entry_id>', methods = ['POST'])
def remove_entry(entry_id):
    db.delete_entry(entry_id)
    day = request.form.get('day', date.today().isoformat())
    flash(' Entry deleted.')
    return redirect(url_for('home',day = day))


# This route handles the editing of an entry in the database.
# It takes the entry_id as a parameter from the URL and retrieves the corresponding entry from the database using the get_entry function from the db module. 
# If the entry does not exist, it redirects the user back to the home page. Otherwise, it renders the 'edit.html' template with the retrieved entry data, allowing the user to edit the entry.
# It also flashes a message to inform the user that the entry is being edited.

@app.route('/edit_entry/<int:entry_id>')
def edit_entry(entry_id):
    entry = db.get_entry(entry_id)
    if entry is None:
        return redirect(url_for('home'))
    return render_edit(entry)


# This route handles the saving of changes made to an existing entry in the database.
# It takes the entry_id as a parameter from the URL and retrieves the updated form data from the request object. 
# It processes the form data, updates the corresponding entry in the database using the update_entry function from the db module.
# It also checks for errors in the form data and re-renders the edit page with the errors if any are found.
# It also flashes a message to inform the user that the changes have been saved.

@app.route('/update_entry/<int:entry_id>', methods = ['POST'])
def save_changes(entry_id):
    activity = activity_from_form()
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
            'note' : note
        }
        return render_edit(entry, errors)
    
    activity_id = db.get_or_create_activity(activity)
    db.update_entry(entry_id, activity_id, start_time, end_time, mood, note)
    flash('Changes saved.')
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


# activity_from_form() is the same logic you already have at the top of save_entry. 
# Once everything works, I can replace those lines in save_entry with activity = activity_from_form() to avoid repeating.

def activity_from_form():
    # works out the activity name from the dropdown and the "Other" box
    choice = request.form.get('activity_choice','')
    if choice == '__other__':
        activity = request.form.get('new_activity','')
    else:
        activity = choice
    return activity.strip()
    
# render_edit() builds the edit page in one place, so both routes below can reuse it.
    
def render_edit(entry, errors=None):
    activities = db.get_activities()
    names = [a['activity_name']for a in activities]
    return render_template('edit.html', entry = entry, errors = errors or [], activities = activities, activity_names = names)



# Converts a timestamp into the number of minutes since midnight by extracting the hour and minute. Returns the result as an integer.
def minutes_since_midnight(timestamp):
    return int(timestamp[11:13]) * 60 + int(timestamp[14:16])


# MOOD FACES
MOOD_FACES = {
    1: "😢",
    2: "😕",
    3: "😐",
    4: "🙂",
    5: "😄"
}
# This function converts a timestamp into a human-readable clock label in 'HH:MM AM/PM' format.
# Example: "14:30" becomes "2:30 PM"
def clock_label (timestamp):
    # 'HH:MM' format
    hour = int(timestamp[11:13])
    minute = timestamp[14:16]
    suffix= 'am' if hour < 12 else 'pm'
    return f"{hour % 12 or 12}: {minute} {suffix}"

# This function makes overlapping entries sit side by side, so none of them hides another.
# Organises activity entries for display on a 24-hour timeline.
# Calculates each activity's position and height based on its start and end times.
# Assigns lanes to overlapping activities so they appear side by side without overlapping.
# Calculates the number of lanes needed for each group to determine the width of each activity.

def layout_entries(rows):
    entries = []
    for row in rows:
        entry = dict(row)
        start = minutes_since_midnight(entry['start_time'])
        end = max(minutes_since_midnight(entry['end_time']), start +15)
        entry['start_min'] = start
        entry['end_min'] = end
        entry['top'] = start / 1440 * 100
        entry['height'] = (end - start) / 1440 * 100
        entry['time_label'] = clock_label(entry['start_time'])
        entry['mood_face'] = MOOD_FACES.get(entry['mood'], '')
        entries.append(entry)
        
    # give each entry a lane, grouping entries that overlap    
    group = -1
    group_end = 0
    lane_ends = []
    
    for e in entries:
        if e['start_min'] >= group_end: # nothing overlaps, so start a new group
            group += 1
            lane_ends = []
            
        for i in range(len(lane_ends)):
            if lane_ends[i] <= e['start_min']: # this lane is free again
                e['lane'] = i
                lane_ends[i] = e['end_min']
                break
        else:                                      # No free lane, so open a new one
            e['lane'] = len(lane_ends)
            lane_ends.append(e['end_min'])
        e['group'] = group
        group_end = max(group_end, e['end_min'])
        
    # each group shares the width between its lanes
    lanes_in_group = {}
    for e in entries:
        lanes_in_group[e['group']] = max(lanes_in_group.get(e['group'], 0), e['lane'] + 1)
    for e in entries:
        e['lanes'] = lanes_in_group[e['group']]
    return entries
            
# This function provides default start and end times for a given day, ensuring that the start time is not later than 22:00 for today and 9:00 for other days.
# Returns a tuple containing the default start and end times as strings in the format 'YYYY-MM-DDTHH:MM'.
# The end time is always one hour after the start time.
            
def default_times(day):
    # today starts at the current hour (no later than 22:00); other days start at 9:00
    hour = min(datetime.now().hour, 22) if day == date.today().isoformat() else 9
    start = datetime.fromisoformat(day).replace(hour=hour)
    end = start + timedelta(hours = 1)
    return start.strftime('%Y-%m-%dT%H:%M'), end.strftime('%Y-%m-%dT%H:%M')


# This function formats a given date string into a more user-friendly format, displaying the day of the week, day of the month, and month name.
# If the date is not in the current year, it also includes the year in the formatted string. Returns the formatted date as a string.

def friendly_date(day):
    d = date.fromisoformat(day)
    label = f"{d:%A}, {d.day} {d:%B}"
    if d.year != date.today().year:
        label += f" {d.year}"
    return label

    
# This function renders the HTML for a specific day's timeline, including the previous and next day navigation, the list of entries, and the form for adding a new entry.
# It takes the day as a string in the format 'YYYY-MM-DD', optional errors, and an optional form dictionary.
# Returns the rendered HTML for the specified day.
# If the day is today, it calculates the scroll position based on the current time; if there are entries, it scrolls to the first entry; otherwise, it defaults to 8:00.
# If no form is provided, it generates default start and end times for the day.

def render_day(day, errors = None, form = None):
    current = date.fromisoformat(day)
    prev_day = (current - timedelta(days=1)).isoformat()
    next_day = (current + timedelta(days=1)).isoformat()
    entries = layout_entries(db.get_entries(day))
    
    now_top = None  # Initialize now_top to None
    if day == date.today().isoformat():
        now = datetime.now()
        now_top = (now.hour * 60 + now.minute) / 1440 *100
        scroll_to = now_top
    elif entries:
        scroll_to = entries[0] ['top'] # scroll to the first entry of the day if thre are entries
    else:
        scroll_to = 8 * 60 / 1440 *100 # 8:00 on empty days
        
    if not form:
        start, end = default_times(day)
        form = {'start_time': start, 'end_time': end}
    
    return render_template('index.html', entries = entries, day = day, prev_day = prev_day, next_day = next_day, errors = errors or [], form = form or {}, activities = db.get_activities(), scroll_to = scroll_to, now_top = now_top, day_label = friendly_date(day))



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001, debug=True)
    
