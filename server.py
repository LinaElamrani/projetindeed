import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, make_response, Response, session
from flask import jsonify
from flask import make_response
from flask import session
from flask import Response
from werkzeug.exceptions import abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import email_validator
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm
import sys


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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'projetindeed'

# AUTHENTIFICATION / CONNECTION

login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, email, password):
        if sys.version_info[0] >= 3:
            unicode = str
            self.id = unicode(id)
            self.email = email
            self.password = password
            self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id

@login_manager.user_loader
def load_user(user_id):
   conn = sqlite3.connect('database.db')
   curs = conn.cursor()
   curs.execute("SELECT * from users where user_id = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2])


@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
     return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
     conn = sqlite3.connect('database.db')
     curs = conn.cursor()
     curs.execute("SELECT * FROM users where email = (?)", [form.email.data])
     user = list(curs.fetchone())
     Us = load_user(user[0])
     Us_email = user[5]
     Us_password = user[6]

    #  flash(user)
    #  flash( Us_password)
    #  flash( Us_email)
    #  flash(form.email.data)
    #  flash(form.password.data)

     if form.email.data == Us_email and form.password.data == Us_password:
        login_user(Us, remember=form.remember.data)
        Umail = list({form.email.data})[0].split('@')[0]
        return render_template('index.html',title='Login', form=form)
     else:
        flash('Login Unsuccessfull.')
  return render_template('login.html',title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')



# CRUD

@app.route("/")
@login_required
def index():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    if request.method == 'POST':
        # flash('dede')
        fullname = request.form['fullname']
        email = request.form['email']
        phone= request.form['phone']
        cv = request.form['cv']

        user = current_user
        job= get_job(id)
        numero = "1"
        flash(('lolo'))
        if not fullname:
            flash('Title is required!')
        if not email:
            flash('Title is required!')
        if not phone:
            flash('Title is required!')
        if not cv:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO applications (numero, user_id, job_id) VALUES (?, ?, ?)',
                         (numero,user,job))
            conn.commit()
            conn.close()
            return redirect(url_for('create'))

    return render_template('index.html' ,jobs=jobs)




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
