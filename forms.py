from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import sqlite3
class LoginForm(FlaskForm):
 date = StringField('date',validators=[DataRequired(),Email()])
 firstname = StringField('firstname',validators=[DataRequired(),Email()])
 lastname = StringField('lastname',validators=[DataRequired(),Email()])
 username= StringField('username',validators=[DataRequired(),Email()])
 email = StringField('email',validators=[DataRequired(),Email()])
 password = PasswordField('password',validators=[DataRequired()])
 remember = BooleanField('Remember Me')
 submit = SubmitField('Login')

 def validate_email(self, email):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    curs.execute("SELECT email FROM users where email = (?)",[email.data])
    valemail = curs.fetchone()
    if valemail is None:
      raise ValidationError('This Email ID is not registered. Please register before login')
