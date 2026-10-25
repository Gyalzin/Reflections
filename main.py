from flask import Flask, render_template, request, redirect, url_for, session
import db

app = Flask(__name__)

@app.route('/')
def home():
    entries = db.get_entries('2026-10-23')
    return render_template('index.html', entries=entries)


if __name__ == '__main__':
    app.run(debug=True) 