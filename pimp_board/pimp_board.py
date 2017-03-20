from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_login import LoginManager, current_user, login_required

app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , pimp_board.py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    SQLALCHEMY_DATABASE_URI='postgresql://pimp:changeme@localhost/pimp_board'
))
app.config.from_envvar('PIMP_BOARD_SETTINGS', silent=True)

db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

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
def index():
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

    return redirect(url_for('index'))

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

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    email = db.Column('email',db.String(50), unique=True , index=True)
    password = db.Column('password' , db.Binary(60))
    first_name = db.Column('first_name', db.String(15))
    last_name = db.Column('last_name', db.String(15))
    registered_on = db.Column('registered_on' , db.DateTime)
 
    def __init__(self, email, password, first_name, last_name):        
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)

from auth import auth_blueprint
app.register_blueprint(auth_blueprint)
