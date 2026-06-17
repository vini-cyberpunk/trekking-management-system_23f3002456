from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
	return render_template('base.html')

@auth.route('/register', methods=['GET','POST'])
def register():
	if request.method == 'GET':
		return render_template('auth/register.html')

	if request.method == 'POST':
		email = request.form.get('email')
		name = request.form.get('name')
		contact = request.form.get('contact')
		password_hash = generate_password_hash(request.form.get('password'))
		role = request.form.get('role')
		
		from app.models import Login, User, Staff
		from app import db
		
		existing_user = Login.query.filter_by(email=email).first()
		if existing_user:
			return render_template('auth/register.html')
		
		new_login = Login(email=email, password=password_hash, role=role)
		
		db.session.add(new_login)
		db.session.commit()
		
		login_id = new_login.login_id
		
		if role=="trekker":
			new_user = User(login_id=login_id, username=name, user_contact=contact, status="active")
			db.session.add(new_user)
			db.session.commit()
			
		elif role=="staff":
			new_staff = Staff(login_id=login_id, staff_name=name, staff_contact=contact, status="pending")
			db.session.add(new_staff)
			db.session.commit()
			
		return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		if current_user.role == 'admin':
			return redirect(url_for('admin.dashboard'))
		elif current_user.role == 'staff':
			return redirect(url_for('staff.dashboard'))
		else:
			return redirect(url_for('user.dashboard'))

	if request.method == 'GET':
		return render_template('auth/login.html')

	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		from app.models import Login
		user = Login.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password, password):
				login_user(user)
				if current_user.role == 'admin':
					return redirect(url_for('admin.dashboard'))
				
				elif current_user.role == 'staff':
					if current_user.status in ["inactive", "pending"]:
						logout_user(user)
						return redirect(url_for('auth.login'))
				
					return redirect(url_for('staff.dashboard'))
				
				else:
					if current_user.status == "inactive":
						logout_user(user)
						return redirect(url_for('auth.login'))
						
					return redirect(url_for('user.dashboard'))
					
			else:
				return render_template('auth/login.html')
		else:
			return render_template('auth/login.html')
			
@auth.route('/logout', methods=['GET'])
def logout():
	logout_user()
	return redirect(url_for('auth.login'))
