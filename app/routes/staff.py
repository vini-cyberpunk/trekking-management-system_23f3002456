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

	total_treks = staff.assigned_trek.all()

	completed_treks = staff.assigned_trek.filter_by(status="completed").all()

	upcoming_treks = staff.assigned_trek.filter( 
		Trek.start_date > date.today(),
		Trek.status != "completed"
	).all()

	active_treks = staff.assigned_trek.filter(
		Trek.start_date <= date.today(),
		Trek.end_date >= date.today(),
	).all()

	total_participants = sum(
		trek.bookings.count()
		for trek in staff.assigned_trek.all()
	)
	
	trek_id = request.args.get('trek_id', type=int)
	trek_name = request.args.get('trek_name', '').strip()
	trek_location = request.args.get('trek_location', '').strip()
	status = request.args.get('status')
	
	current_filter = request.args.get('filter', '')
	
	if current_filter == "total":
		treks = total_treks
		
	elif current_filter == "active":
		treks = active_treks
		
	elif current_filter == "upcoming":
		treks = upcoming_treks
	
	elif current_filter == "completed":
		treks = completed_treks
		
	else:
	
		query = staff.assigned_trek
		
		if trek_id:
			query = query.filter_by(trek_id=trek_id)
			
		if trek_name:
			query = query.filter(Trek.trek_name.ilike(f"%{trek_name}%"))
			
		if trek_location:
			query = query.filter(Trek.location.ilike(f"%{trek_location}%"))
			
		if status:
			query = query.filter_by(status=status)
			
		treks = query.all()
	
	return render_template(
		'staff/dashboard.html',
		staff = staff,
		total_treks = total_treks,
		completed_treks = completed_treks,
		upcoming_treks = upcoming_treks,
		active_treks = active_treks,
		total_participants = total_participants,
		
		treks = treks
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
	
	
@staff.route('/profile', methods=["GET", "POST"])
@login_required
def profile():

	login_id = current_user.login_id
	
	staff = Staff.query.filter_by(login_id=login_id).first()
	
	if request.method=="POST":
		staff_name = request.form.get('staff_name', '').strip()
		staff_contact = request.form.get('staff_contact', '').strip()
		
		if staff_name:
			staff.staff_name = staff_name
		
		if staff_contact:
			staff.staff_contact = staff_contact
		
		db.session.commit()
		
		return redirect(url_for('staff.profile'))
	
	return render_template(
		'staff/profile.html',
		staff = staff
	)
