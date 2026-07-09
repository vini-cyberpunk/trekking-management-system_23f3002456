from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import Login, User, Staff

auth = Blueprint('auth', __name__)

#################### HOME ####################
@auth.route('/')
def home():

	if current_user.is_authenticated:
		if current_user.role == 'admin':
			return redirect(url_for('admin.dashboard'))
		elif current_user.role == 'staff':
			return redirect(url_for('staff.dashboard'))
		else:
			return redirect(url_for('user.dashboard'))

	return redirect(url_for('auth.login'))
	

#################### REGISTER ####################
@auth.route('/register', methods=['GET','POST'])
def register():
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

	if request.method == 'GET':
				
		return render_template('auth/login.html')

	if request.method == 'POST':
	
		email = request.form.get('email')
		password = request.form.get('password')

		login = Login.query.filter_by(email=email).first()
		
		if login:
		
			if check_password_hash(login.password, password):
			
				login_user(login)
				
				if current_user.role == 'admin':
					return redirect(url_for('admin.dashboard'))
				
				elif current_user.role == 'staff':
				
					staff = Staff.query.filter_by(login_id=current_user.login_id).first()
					
					if staff.status in ["inactive", "pending"]:
						flash( "Account is inactive", "danger")
						return redirect(url_for('auth.login'))
				
					else:
						return redirect(url_for('staff.dashboard'))
				
				else:
				
					from app.models import User
					user = User.query.filter_by(login_id=current_user.login_id).first()
					
					print(user)
					
					if user.status == "inactive":
						logout_user(user)
						return redirect(url_for('auth.login'))
						
					else:
						return redirect(url_for('user.dashboard'))
					
			else:
				return redirect(url_for('auth.login'))
				
		else:
			return redirect(url_for('auth.login'))
			
			
#################### LOGOUT ####################
@auth.route('/logout', methods=['GET'])
def logout():
	logout_user()
	return redirect(url_for('auth.login'))
