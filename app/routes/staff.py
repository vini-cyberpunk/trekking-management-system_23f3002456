from flask import Blueprint, render_template
from flask_login import login_required, current_user

staff = Blueprint('staff', __name__)


@staff.route('/dashboard', methods=["GET"])
@login_required
def dashboard():
	
	login_id = current_user.login_id
	
	from app.models import Staff
	
	staff = Staff.query.filter_by(login_id=login_id).first()
	
	return render_template('staff/dashboard.html', staff = staff)
	

@staff.route('/assigned_treks', methods=["GET"])
@login_required
def assigned_treks():
	
	return render_template('staff/assigned_treks.html')
	
	
@staff.route('/participants', methods=["GET"])
@login_required
def participants():
	
	return render_template('staff/participants.html')
	
	
@staff.route('/profile', methods=["GET"])
@login_required
def profile():

	login_id = current_user.login_id
	
	from app.models import Staff
	
	staff = Staff.query.filter_by(login_id=login_id).first()
	
	return render_template('staff/profile.html', staff = staff)
