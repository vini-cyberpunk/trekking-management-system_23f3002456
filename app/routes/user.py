from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user

from app import db
from app.models import User, Trek, Booking
from datetime import datetime


user = Blueprint('user', __name__)

@user.route('/dashboard', methods=["GET"])
@login_required
def dashboard():

	login_id = current_user.get_id()
	
	user = User.query.filter_by(login_id=login_id).first()
	
	available_treks = Trek.query.filter_by(status='open').all()
	
	bookings = user.bookings

	today = datetime.now()

	upcoming_treks = Trek.query.filter( Trek.start_date >= today ).all()

	completed_treks = Trek.query.filter( Trek.end_date < today ).all()
	
	active_treks = Trek.query.filter(
		Trek.start_date <= today,
		Trek.end_date >= today
	).all()

	return render_template(
		'user/dashboard.html',
		user=user,
		available_treks=available_treks,
		bookings=bookings,
		upcoming_treks=upcoming_treks,
		completed_treks=completed_treks,
		active_treks=active_treks
	)
	
	
@user.route('/treks', methods=["GET"])
@login_required
def treks():

	query = Trek.query.filter_by(status="open")

	trek_name = request.args.get('trek_name', '')
	location = request.args.get('location', '')
	difficulty = request.args.get('difficulty', '')
	start_date = request.args.get('start_date')
	end_date = request.args.get('end_date')
	
	if trek_name:
		query = query.filter( Trek.trek_name.ilike(f"%{trek_name}%") )
		
	if location:
		query = query.filter( Trek.location.ilike(f"%{location}%") )
		
	if difficulty:
		query = query.filter_by(difficulty=difficulty)
		
	if start_date:
		query = query.filter( Trek.start_date >= start_date )
		
	if end_date:
		query = query.filter( Trek.end_date <= end_date )
		
	treks = query.all()
	
	return render_template(
		'user/treks.html',
		treks=treks
	)
	

@user.route('/bookings', methods=["GET"])
@login_required
def bookings():

	login_id = current_user.get_id()
	
	user = User.query.filter_by(login_id=login_id).first()
	
	bookings = user.bookings
	
	return render_template(
		'user/bookings.html',
		bookings=bookings
	)
	
	
@user.route('/book_trek/<int:trek_id>', methods=["GET"])
@login_required
def book_trek(trek_id):

	login_id = current_user.get_id()
	
	user = User.query.filter_by(login_id=login_id).first()
	trek = Trek.query.get(trek_id)
	
	existing_booking = Booking.query.filter_by( user_id=user.user_id, trek_id=trek.trek_id ).first()
	
	if existing_booking:
		flash("Booking Already Exists!", "warning")
	
	elif trek.status=="open" and trek.available_slots > 0:
		trek.available_slots -= 1
		
		booking = Booking(
			user_id=user.user_id,
			trek_id=trek_id,
			booking_date=datetime.now(),
			status="booked"
		)
		
		flash("Successfully Booked!", "success")
		
		db.session.add(booking)
		db.session.commit()
		
		
	
	next_page = request.args.get('next')
	return redirect(next_page)
	
	
@user.route('/profile', methods=["GET"])
@login_required
def profile():
	
	return render_template('user/profile.html')
