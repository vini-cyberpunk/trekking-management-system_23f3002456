from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user

from app.models import Staff, Trek, Booking
from app import db
from datetime import date

staff = Blueprint('staff', __name__)


@staff.route('/dashboard', methods=["GET"])
@login_required
def dashboard():
	
	login_id = current_user.login_id

	staff = Staff.query.filter_by(login_id=login_id).first()

	assigned_treks = staff.assigned_trek.all()

	completed_treks = staff.assigned_trek.filter_by(status="completed").all()

	upcoming_treks = staff.assigned_trek.filter( Trek.start_date > date.today() ).all()

	active_treks = staff.assigned_trek.filter(
		Trek.start_date <= date.today(),
		Trek.end_date >= date.today()
	).all()

	total_participants = sum(
		trek.bookings.count()
		for trek in staff.assigned_trek.all()
	)
	
	return render_template(
		'staff/dashboard.html',
		staff = staff,
		assigned_treks = assigned_treks,
		completed_treks = completed_treks,
		upcoming_treks = upcoming_treks,
		active_treks = active_treks,
		total_participants = total_participants
	)
	
	
@staff.route('/manage_trek/<int:trek_id>', methods=['GET', 'POST'])
@login_required
def manage_trek(trek_id):

	staff = Staff.query.filter_by(login_id=current_user.login_id).first()

	trek = Trek.query.get(trek_id)
	
	next_page = request.args.get('next')

	if request.method == "POST":

		trek.available_slots = request.form.get("available_slots")

		trek.status = request.form.get("status")

		db.session.commit()

		flash("Trek updated successfully.", "success")
		
		next_page = request.form.get('next')
		return redirect(next_page)
		

	return render_template(
		"staff/manage_trek.html",
		trek=trek,
		next_page=next_page
	)

	
	
@staff.route('/participants/<int:trek_id>', methods=["GET"])
@login_required
def participants(trek_id):

	staff = Staff.query.filter_by(login_id=current_user.login_id).first()

	trek = Trek.query.get(trek_id)

	bookings = Booking.query.filter_by(trek_id=trek_id).all()
	
	participants = trek.bookings.count()

	next_page = request.args.get('next')

	return render_template(
		"staff/participants.html",
		trek=trek,
		bookings=bookings,
		participants=participants,
		next_page=next_page
	)
	
	
@staff.route('/profile', methods=["GET"])
@login_required
def profile():

	login_id = current_user.login_id
	
	from app.models import Staff
	
	staff = Staff.query.filter_by(login_id=login_id).first()
	
	return render_template(
		'staff/profile.html', 
		staff = staff
	)
