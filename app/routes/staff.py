from flask import Blueprint, render_template
from flask_login import login_required

staff = Blueprint('staff', __name__)


@staff.route('/dashboard', methods=["GET"])
@login_required
def dashboard():
	
	return render_template('staff/dashboard.html')
	

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
	
	return render_template('staff/profile.html')
