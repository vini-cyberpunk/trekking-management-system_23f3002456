from flask import Blueprint, render_template
from flask_login import login_required

admin = Blueprint('admin', __name__)

@admin.route('/dashboard', methods=['GET'])
@login_required
def dashboard():

	from app.models import User, Login, Trek, Booking, Staff
	
	total_bookings = Booking.query.count()
	total_users = User.query.count()
	total_staff = Staff.query.count()
	total_treks = Trek.query.count()
	
	return render_template(
		"admin/dashboard.html",
		total_bookings=total_bookings,
		total_users=total_users,
		total_staff=total_staff,
		total_treks=total_treks
	)
