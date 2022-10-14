import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, make_response, Response, session
from flask import jsonify
from flask import make_response
from flask import session
from flask import Response
from werkzeug.exceptions import abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm
import email_validator
import models as dbHandler
from flask import Blueprint, render_template




def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_job(job_id):
    conn = get_db_connection()
    job = conn.execute('SELECT * FROM jobs WHERE job_id = ?',
                        (job_id,)).fetchone()
    conn.close()
    if job is None:
        abort(404)
    return job


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    return render_template('logout.html')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'projetindeed'


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login', methods=['POST', 'GET'])
def home():
    if request.method=='POST':
            email = request.form['email']
            paswword = request.form['password']
            dbHandler.insertUser(email, paswword)
            users = dbHandler.retrieveUsers()
            return render_template('index.html', users=users)
    else:
   		return render_template('index.html')


@app.route("/")
def index():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs)


@app.route('/<int:job_id>')
def job(job_id):
    job = get_job(job_id)
    return render_template('job.html', job=job)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        contract = request.form['contract']
        worktime = request.form['worktime']
        postalcode = request.form['postalcode']
        userstate = request.form['userstate']
        salary = request.form['salary']


        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO jobs (title, description, location, postalcode, contract, worktime, userstate, salary ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                         (title, description, location, postalcode, contract, worktime, userstate, salary))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    job= get_job(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        contract = request.form['contract']
        worktime = request.form['worktime']
        postalcode = request.form['postalcode']
        userstate = request.form['userstate']
        salary = request.form['salary']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE jobs SET title = ?, description = ?, location = ?, postalcode = ?, contract = ?, worktime = ?, userstate = ?, salary = ?'
                         ' WHERE job_id = ?',
                         (title, description, location, postalcode, contract, worktime, userstate, salary, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', job=job)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    job = get_job(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM jobs WHERE job_id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(job['title']))
    return redirect(url_for('index'))
