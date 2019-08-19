# Imports
from flask import render_template, flash, redirect, url_for, request, Flask, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from wtforms import Form, StringField, DateTimeField, TextField, PasswordField, validators, SubmitField, TextAreaField, RadioField, IntegerField, FloatField, FileField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
import sys
import pymysql #used to connect SQL DB to python and run queries
import sqlite3
import getpass
from email.message import EmailMessage
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
import os
import datetime
import re
from PIL import Image
from io import BytesIO
import base64
import io
import ocr_simple


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
class AddManualForm(FlaskForm):
	med_name = StringField('Medication', validators=[DataRequired()])
	dosage = IntegerField('Dosage', validators=[DataRequired()])
	frequency = StringField('Frequency', validators=[DataRequired()])
	refills = IntegerField('Refills', validators=[DataRequired()])
	dateFill = DateField('Date Filled', validators=[])
	doc = StringField('Physician', validators=[DataRequired()])
	pharm = StringField('Pharmacy', validators=[DataRequired()])
	submit =  SubmitField('Submit: ')

class AddScan(FlaskForm):
	# Add Scan Form
	submit =  SubmitField('Add Prescription via Camera')

# Remove Rx Form
class RemoveForm(FlaskForm):
	med_name = SelectField('Medication', choices= [], coerce=int)
	submit =  SubmitField('Remove Prescription')

## User class

class User(UserMixin):
	def __init__(self, username, password):
		self.id = username.replace("'", "")
		# hash the password and output it to stderr
		self.password = password


class Medication():
	def __init__(self, medname, dateFill, dosage, frequency, refills):
		self.id = medname
		self.dateFill = dateFill
		self.dosage = dosage
		self.frequency = frequency
		self.refills = refills


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

# Code for allowed file extensions

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Code to load users and meds as functions to load later

def load_users():
	c.execute("SELECT * from users")
	users = c.fetchall()
	# print (users)
	for user in users:
		user_db[user[1]]=user[2]
	# print(user_db)
	
def load_meds():
	c.execute("SELECT * from usermeds")
	meds = c.fetchall()
	for med in meds:
		med_db[str(med[0])] = Medication(med[0],med[1],med[2],med[3],med[4])

# Init User and Medication Databases

user_db = {"wmaroney78@gmail.com":'abc'}
med_db = {}

load_users()
load_meds()


	
	
def profileIsSetup():
	if current_user.profileSetup == 1:
		return True
	else:
		return False
	


# Login manager uses this function to manage user sessions.
# Function does a lookup by id and returns the User object if
# it exists, None otherwise.
@login_manager.user_loader
def load_user(id):
	return User(id, user_db[id])
	
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	db = pymysql.connect(host='35.229.79.169', user='root', password='password', db='med_minder')
	c = db.cursor()
	c.execute('SELECT * from usermeds')
	l = c.fetchall()
	db.close()
	return render_template ('index.html', data=l)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	# display the login form
	form = LoginForm()
	if form.validate_on_submit():
		user = form.username.data
		# validate user
		valid_password = user_db[form.username.data]
		if user is None or not valid_password:
			print('Invalid username or password', file=sys.stderr)
			redirect(url_for('index'))
		else:
			print(user)
			login_user(User (user, valid_password))
			# print(user.is_authenticated)
			flash('Login Successful', category='success')
			return redirect(url_for('index'))

	return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	# display the login form
	form = SignupForm()
	if form.validate_on_submit():
		user = form.username.data
		exists = user_db.get(user)
		# validate user
		if exists is None:
			user_pass = form.password.data
			c.execute ('INSERT INTO users (user_id, user_email, user_password) VALUES ({},"{}","{}")'.format(0,user, user_pass))
			db.commit()
			load_users()
			return redirect(url_for('index'))
		else:
			flash('Invalid User Name or Password', category='error')
			return redirect(url_for('index'))

	return render_template('signUP.html', title='Sign Up', form=form)

@app.route('/addscan', methods=['GET', 'POST'])
def addscan ():
	return render_template('addscan.html')
	
@app.route('/imgprocess', methods=['GET', 'POST'])
def imgprocess():
	form = AddManualForm()
	data = request.form['img'] # grab the image captured
	image_data = re.sub('^data:image/.+;base64,', '', request.form['img']) # remove metadata (mimetype)
	im = Image.open(BytesIO(base64.b64decode(image_data))) # open the image in memory
	im = im.convert("RGB") # convert to a format recognized by JPEG encoding mime
	im.save("test.jpg") # save the image as test.jpg or can be a path to some folder as well and renamed
	text = ocr_simple.img_to_text("test.jpg")
	return render_template("addrxman.html", upload=True, text=text, form=form) #push user to addrx manual form

@app.route('/addrxman', methods=['GET', 'POST'])
def addrxman():
	form = AddManualForm()
	if form.validate_on_submit():
		med_name = form.med_name.data
		doc = form.doc.data
		dateFill = form.dateFill.data
		frequency = form.frequency.data
		dosage = form.dosage.data
		refills = form.refills.data
		db = pymysql.connect(host='35.229.79.169', user='root', password='password', db='med_minder')
		c = db.cursor()
		user_id = c.execute ('SELECT user_id FROM users WHERE user_email="{}"'.format(current_user.id))
		#print(user_id)
		sql = ('INSERT INTO usermeds (med_id, user_id, med_name, med_freq, med_dose, dr_name, refill_date, num_refills) VALUES ({},"{}","{}","{}","{}","{}","{}","{}")'.format(0, user_id, med_name, frequency, dosage, doc, dateFill, refills))
		c.execute (sql)
		db.commit()
		load_meds()
		return (redirect('/index'))
	return render_template('addrxman.html', title='Add Rx', form=form)


@app.route('/remove',methods=['GET', 'POST'])
def removerx():
	form = RemoveForm()
	db = pymysql.connect(host='35.229.79.169', user='root', password='password', db='med_minder')
	c = db.cursor()
	user_id = c.execute ('SELECT user_id FROM users WHERE user_email="{}"'.format(current_user.id))
	c.execute('SELECT med_id, med_name from usermeds WHERE user_id = {}'.format(user_id))
	meds=c.fetchall()
	form.med_name.choices = meds
	if form.validate_on_submit():
		sql = "DELETE FROM usermeds WHERE med_id = '{}'".format(form.med_name.data)
		c.execute (sql)
		db.commit()
		db.close()
		return (redirect('/index'))
	return render_template('removerx.html', title='Remove Rx', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/about')
def about():
	return render_template('about.html', title='About')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)

