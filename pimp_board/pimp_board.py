import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , pimp_board.py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    SQLALCHEMY_DATABASE_URI='postgresql://pimp:changeme@localhost/pimp_board'
))
app.config.from_envvar('PIMP_BOARD_SETTINGS', silent=True)

db = SQLAlchemy(app)

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    #db.session.dispose()

def init_db():
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def show_entries():
    entries = db.session.query(Entry).order_by(Entry.id)
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    try:
        entry = Entry(
            title=request.form['title'],
            text=request.form['text'],
        )
        db.session.add(entry)
        db.session.commit()
    except:
        flash('Error adding new entry')
    else:
        flash('New entry was successfully posted')

    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    text = db.Column(db.String)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<id {}>'.format(self.id)

