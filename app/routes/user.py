from flask import Blueprint, render_template
from flask_login import login_required

user = Blueprint('user', __name__)

@user.route('/dashboard', methods=["GET"])
@login_required
def dashboard():

	return render_template('user/dashboard.html')
	
	
@user.route('/treks', methods=["GET"])
@login_required
def treks():
	
	return render_template('user/treks.html')
	

@user.route('/bookings', methods=["GET"])
@login_required
def bookings():
	
	return render_template('user/bookings.html')
	
	
@user.route('/history', methods=["GET"])
@login_required
def history():
	
	return render_template('user/history.html')
	
	
@user.route('/profile', methods=["GET"])
@login_required
def profile():
	
	return render_template('user/profile.html')
