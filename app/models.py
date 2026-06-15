from app import db
from flask_login import UserMixin

class Login(UserMixin, db.Model):
	__tablename__ = 'login'
	login_id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)
	role = db.Column(db.Enum('admin','trekker','staff'), nullable=False)
	
	def get_id(self):
		return str(self.login_id)

class User(db.Model):
	__tablename__ = 'user'
	user_id = db.Column(db.Integer, primary_key=True)
	login_id = db.Column(db.Integer, db.ForeignKey('login.login_id', ondelete='CASCADE'), unique=True, nullable=False)
	username = db.Column(db.String(50), nullable=False)
	user_contact = db.Column(db.String(10), nullable=True)
	status = db.Column(db.Enum('active', 'inactive'), nullable=False)

class Staff(db.Model):
	__tablename__ = 'staff'
	staff_id = db.Column(db.Integer, primary_key=True)
	login_id = db.Column(db.Integer, db.ForeignKey('login.login_id', ondelete='CASCADE'), unique=True, nullable=False)
	staff_name = db.Column(db.String(50), nullable=False)
	staff_contact = db.Column(db.String(10), nullable=True)
	status = db.Column(db.Enum('active', 'inactive', 'pending'), nullable=False)
	assigned_treks = db.relationship('Trek', backref='staff', lazy=True)

class Trek(db.Model):
	__tablename__ = 'trek'
	trek_id = db.Column(db.Integer, primary_key=True)
	trek_name = db.Column(db.String(150), nullable=False)
	trek_location = db.Column(db.String(300), nullable=False)
	difficulty = db.Column(db.Enum('easy','moderate','hard'), nullable=False)
	available_slots = db.Column(db.Integer, nullable=False)
	assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id', ondelete='SET NULL'), nullable=True)
	duration = db.Column(db.Integer, nullable=False)
	start_date = db.Column(db.DateTime, nullable=False)
	end_date = db.Column(db.DateTime, nullable=False)
	status = db.Column(db.Enum('pending','approved','open','closed','completed'), nullable=False)
	
	__table_args__ = (
		db.CheckConstraint(
			'available_slots >= 0',
			name = 'check_slots_positive',
		),
		
		db.CheckConstraint(
			'end_date > start_date',
			name = 'check_date_valid'
		),
	)

class Booking(db.Model):
	__tablename__ = 'booking'
	booking_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='RESTRICT'), nullable=False)
	trek_id = db.Column(db.Integer, db.ForeignKey('trek.trek_id', ondelete='SET NULL'), nullable=True)
	booking_date = db.Column(db.DateTime, nullable=False)
	status = db.Column(db.Enum('booked','cancelled','completed'), nullable=False)
	
	
