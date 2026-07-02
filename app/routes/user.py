from flask import Blueprint, render_template, url_for, request, flash
from flask_login import login_required, current_user

from app import db
from app.models import User, Trek, Booking

user = Blueprint('user', __name__)

@user.route('/dashboard', methods=["GET"])
@login_required
def dashboard():

	login_id = current_user.get_id()
	
	user = User.query.filter_by(login_id=login_id).first()
	
	available_treks = Trek.query.filter_by(status='open').all()
	
	booked_treks = user.bookings

	return render_template(
		'user/dashboard.html',
		user=user,
		available_treks=available_treks,
		booked_treks=booked_treks
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
	
	return render_template('user/bookings.html')
	
	
@user.route('/history', methods=["GET"])
@login_required
def history():
	
	return render_template('user/history.html')
	
	
@user.route('/profile', methods=["GET"])
@login_required
def profile():
	
	return render_template('user/profile.html')
