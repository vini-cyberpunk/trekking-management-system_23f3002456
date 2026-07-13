from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import Login, User, Staff

auth = Blueprint('auth', __name__)

#################### HOME ####################
@auth.route('/')
def home():

	return redirect(url_for('auth.login'))
		
	

#################### REGISTER ####################
@auth.route('/register', methods=['GET','POST'])
def register():
	
	next_page, msg, msg_type = validate_login(current_user)
	
	if next_page:
		if msg:
			flash(msg, msg_type)
		return redirect(next_page)
	
	if request.method == 'GET':
		return render_template('auth/register.html')

	elif request.method == 'POST':
		
		# getting the form values
		email = request.form.get('email', '').strip()
		name = request.form.get('name', '').strip()
		contact = request.form.get('contact','').strip()
		password_hash = generate_password_hash(request.form.get('password'))
		role = request.form.get('role', '')
		
		# existing user check
		existing_user = Login.query.filter_by(email=email).first()
		if existing_user:
			flash("Account Already Exists", "danger")
			return redirect(url_for('auth.register'))
		
		# add new login
		new_login = Login(email=email, password=password_hash, role=role)
		
		db.session.add(new_login)
		db.session.commit()
		
		# getting newly generated login id
		login_id = new_login.login_id
		print(login_id)
		
		# registering according to role
		if new_login.role=="trekker":
			new_user = User(login_id=login_id, username=name, user_contact=contact, status="active")
			db.session.add(new_user)
			db.session.commit()
			
			
		elif new_login.role=="staff":
			new_staff = Staff(login_id=login_id, staff_name=name, staff_contact=contact, status="pending")
			db.session.add(new_staff)
			db.session.commit()
			
		# redirecting to login page
		return redirect(url_for('auth.login'))


#################### LOGIN ####################
@auth.route('/login', methods=['GET','POST'])
def login():

	next_page, msg, msg_type = validate_login(current_user)
	
	if next_page:
		if msg:
			flash(msg, msg_type)
			
		return redirect(next_page)

	if request.method == 'GET':
				
		return render_template('auth/login.html')

	if request.method == 'POST':
	
		email = request.form.get('email')
		password = request.form.get('password')

		login = Login.query.filter_by(email=email).first()
		
		if login:
		
			if check_password_hash(login.password, password):
			
				login_user(login)
				
				next_page, msg, msg_type = validate_login(current_user)
				if msg:
					flash(msg, msg_type)
					
				return redirect(next_page)
					
			else:
				flash("Invalid Password!", "danger")
				return redirect(url_for('auth.login'))
				
		else:
			flash("Invalid Credentials!", "danger")
			return redirect(url_for('auth.login'))
			
			
#################### LOGOUT ####################
@auth.route('/logout', methods=['GET'])
def logout():
	logout_user()
	return redirect(url_for('auth.login'))
	
	
#################### CUSTOM FUNCTIONS ####################
def validate_login(current_user):
	
	msg = ""
	msg_type = ""
	next_page = ""

	if current_user.is_authenticated:
	
		login_id = current_user.get_id()
		if current_user.role == 'admin':
			msg = "Login Successful!"
			msg_type = "success"
			return url_for('admin.dashboard'), msg, msg_type
			
		elif current_user.role == 'staff':
		
			staff = Staff.query.filter_by(login_id=login_id).first()
			if staff.status == "inactive":
				msg = "Your account is currently inactive! Try again later."
				msg_type = "danger"
				logout_user()
				return url_for('auth.login'), msg, msg_type
				
			elif staff.status == "active":
				msg = "Login Successful!"
				msg_type = "success"
				return url_for('staff.dashboard'), msg, msg_type
				
		elif current_user.role == 'trekker':
		
			user = User.query.filter_by(login_id=login_id).first()
			if user.status == "inactive":
				msg = "Your account is currently inactive! Try again later."
				msg_type = "danger"
				logout_user()
				return url_for('auth.login'), msg, msg_type
				
			elif user.status == "active":
				msg = "Login Successful!"
				msg_type = "success"
				return url_for('user.dashboard'), msg, msg_type
				
	else:
		return next_page, msg, msg_type
				

