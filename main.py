# Imports
from flask import render_template, flash, redirect, url_for, request, Flask, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from wtforms import Form, StringField, TextField, PasswordField, validators, SubmitField, TextAreaField, RadioField, IntegerField, DateTimeField, FileField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
import sys
import pymysql
import sqlite3
import os
import datetime
import re

db = pymysql.connect(host='35.229.79.169', user='root', password='password', db='med_minder')
c = db.cursor()

## FLASK FORMS subclassed from FlaskForm


class LoginForm(FlaskForm):
	username = TextField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
	username = TextField('Username', validators=[DataRequired()])
	#Add built in Validator
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirmPass', message='Passwords must match')])
	confirmPass = PasswordField('Repeat Password', validators=[DataRequired()])
	submit = SubmitField('Sign Up')

class ConfirmMedicationAdd(FlaskForm):
	submit = SubmitField('Confirm')

# Add Rx Manual Form
class AddManual(FlaskForm):
	medication = StringField('Medication', validators=[DataRequired()])
	dosage = IntegerField('Dosage', validators=[DataRequired()])
	freq = StringField('Frequency', validators=[DataRequired()])
	refills = IntegerField('Refills', validators=[DataRequired()])
	dateFill = DateTimeField('Date Filled', validators=[DataRequired()])
	doc = StringField('Physician', validators=[DataRequired()])
	pharm = StringField('Pharmacy', validators=[DataRequired()])
	submit =  SubmitField('Submit: ')

class AddScan(FlaskForm):
	# Initiate OCR to get text file
	submit =  SubmitField('Add Prescription via Camera')

# Remove Rx Form
class Remove(FlaskForm):
	medication = StringField('Medication', validators=[DataRequired()])
	submit =  SubmitField('Remove Prescription')

## User class

class User():
	def __init__(self, id, username, setup, password):
		self.id = id
		self.name = username
		self.password = password
		self.ident = ident
		self.profileSetup = int(setup)


class Medication():
	def __init__(self, id, addedDate, dosage, freq, refill):
		self.id = id
		self.addedDate = addedDate
		self.dosage = dosage
		self.freq = frequency
		self.refill = refills


## Creating the Flask app object and login manager

app = Flask(__name__)

skey = os.urandom(12)
app.config['SECRET_KEY'] = skey
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
images_folder = 'documents/rx_images/'
translation_folder = 'documents/text_translations/'
allowed_extensions = set(['txt', 'jpg'])



# Login manager uses this function to manage user sessions.
# Function does a lookup by id and returns the User object if
# it exists, None otherwise.

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in allowed_extensions

def load_users():
	c.execute("SELECT * from users")
	users = c.fetchall()

# Init User and Medication Databases

user_db = {}
med_db = {}


# Login manager uses this function to manage user sessions.
# Function does a lookup by id and returns the User object if
# it exists, None otherwise.
@login_manager.user_loader
def load_user(id):
	return user_db.get(id)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	db = pymysql.connect(host='35.229.79.169', user='root', password='password', db='med_minder')
	c = db.cursor()
	c.execute('SELECT * from usermeds')
	l = c.fetchall()
	db.close()
	return render_tamplate ('index.html', data=l)



@app.route('/addrxman', methods=['GET', 'POST'])
def addrxman():
	form = AddManual()
	if form.validate_on_submit():
		db = pymysql.connect(host='35.229.79.169', user='root', password='password', db='med_minder')
		c = db.cursor()
		sql = 'INSERT INTO usermeds(med_name, med_dose, num_refills, med_freq) VALUES'\
		"(%s, %s, %s, %s)"
		c.execute (sql, (usermeds, str(med_name), int(med_dose), int(num_refills), int(med_freq)))
		db.commit()
		db.close()
		return (redirect('/view'))
	return render_template('index.html', form_add=form)


@app.route('/remove',methods=['GET', 'POST'])
def removerx():
	form = Remove()
	if form.validate_on_submit():
		db = pymysql.connect(host='35.229.79.169', user='root', password='password', db='med_minder')
		c = db.cursor()
		sql = "DELETE FROM usermeds WHERE name = '"+med_name+"'"
		c.execute (sql)
		db.commit()
		db.close()
		return (redirect('/view'))
		return render_template('index.html', form_add=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/about')
def about():
		return render_template('about.html', title='About')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
