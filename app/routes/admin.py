from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from datetime import datetime
from app.models import User, Login, Trek, Booking, Staff
from app import db

admin = Blueprint('admin', __name__)

#################### ADMIN ####################
@admin.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	
	total_bookings = Booking.query.count()
	total_users = User.query.count()
	total_staff = Staff.query.count()
	total_treks = Trek.query.count()
	
	recent_users = User.query.order_by(User.user_id.desc()).limit(5).all()
	recent_staff = Staff.query.order_by(Staff.staff_id.desc()).limit(5).all()
	recent_treks = Trek.query.order_by(Trek.trek_id.desc()).limit(5).all()
	recent_bookings = Booking.query.order_by(Booking.booking_id.desc()).limit(5).all()
	
	return render_template(
		'admin/dashboard.html',
		total_bookings=total_bookings,
		total_users=total_users,
		total_staff=total_staff,
		total_treks=total_treks,
		
		recent_users=recent_users,
		recent_staff=recent_staff,
		recent_treks=recent_treks,
		recent_bookings=recent_bookings
	)


#################### USER ####################
@admin.route('/users', methods=['GET'])
@login_required
def users():

	base_query = User.query.join(User.login)

	total_users = base_query.order_by(User.user_id.desc()).all()
	active_users = base_query.filter(User.status == "active").order_by(User.user_id.desc()).all()
	inactive_users = base_query.filter(User.status == "inactive").order_by(User.user_id.desc()).all()
	
	current_filter = request.args.get('filter', '')
	
	if current_filter == "total":
		users = total_users
		
	elif current_filter == "active":
		users = active_users
		
	elif current_filter == "inactive":
		users = inactive_users
		
	else:
		query = base_query
		
		username = request.args.get('username', '').strip()
		user_id = request.args.get('user_id', '').strip()
		user_contact = request.args.get('user_contact', '').strip()
		email = request.args.get('email', '').strip()
		status = request.args.get('status', '').strip()

		if username:
			query = query.filter(
				User.username.ilike(f"%{username}%")
			)

		if user_id:
			query = query.filter(
				User.user_id == int(user_id)
			)

		if user_contact:
			query = query.filter(
				User.user_contact.ilike(f"%{user_contact}%")
			)

		if email:
			query = query.filter(
				Login.email.ilike(f"%{email}%")
			)

		if status:
			query = query.filter(
				User.status == status
			)

		users = query.order_by(User.user_id.desc()).all()

	return render_template(
		'admin/users.html',
		total_users=total_users,
		active_users=active_users,
		inactive_users=inactive_users,
		users=users
	)


@admin.route('/users/<int:user_id>/update-status', methods=['POST'])
@login_required
def update_user_status(user_id):
	
	user = User.query.get(user_id)
	status = request.form.get('status')
	
	user.status = status
	
	db.session.commit()
	
	next_page = request.form.get('next')
	return redirect(next_page)
	
	
@admin.route('user/<int:user_id>/delete_user', methods=["POST"])
@login_required
def delete_user(user_id):

	if user_id:
		user = User.query.get(user_id)
		
		db.session.delete(user)
		db.session.commit()
		
		flash("User Deleted Sucessfully!", "success")
		
	else:
		flash("Invalid User ID", "danger")
	
	next_page = request.form.get('next')
	return render_template(next_page)
	
	
#################### STAFF ####################
@admin.route('/staff', methods=["GET"])
@login_required
def staff():
	
	base_query = Staff.query.join(Login).join(Trek)
	
	total_staff = base_query.order_by(Staff.staff_id.desc()).all()
	active_staff = base_query.filter(Staff.status=="active").order_by(Staff.staff_id.desc()).all()
	inactive_staff = base_query.filter(Staff.status=="inactive").order_by(Staff.staff_id.desc()).all()
	pending_staff = base_query.filter(Staff.status=="pending").order_by(Staff.staff_id.desc()).all()
	
	current_filter = request.args.get('filter', '')
	
	if current_filter == "total":
		staff = total_staff
		
	elif current_filter == "active":
		staff = active_staff
		
	elif current_filter == "inactive":
		staff = inactive_staff
		
	elif current_filter == "pending":
		staff = pending_staff
		
	else:
		query = base_query
	
		staff_id = request.args.get('staff_id', '')
		staff_name = request.args.get('staff_name', '')
		email = request.args.get('email', '')
		staff_contact = request.args.get('staff_contact', '')
		trek_name = request.args.get('trek_name', '')
		status = request.args.get('status', '')
		
		if staff_id:
			query = query.filter(Staff.staff_id==staff_id)
			
		if staff_name:
			query = query.filter(
				Staff.staff_name.ilike(f"%{staff_name}%")
			)
			
		if staff_contact:
			query = query.filter(
				Staff.staff_contact.ilike(f"%{staff_contact}%")
			)
			
		if email:
			query = query.filter(
				Login.email.ilike(f"%{email}%")
			)
			
		if trek_name:
			query = query.filter(
				Trek.trek_name.ilike(f"%{trek_name}%")
			)
			
		if status:
			query = query.filter(Staff.status==status)
		
		staff = query.order_by(Staff.staff_id.desc()).all()
		
	return render_template(
		'admin/staff.html',
		staff=staff,
		total_staff=total_staff,
		active_staff=active_staff,
		inactive_staff=inactive_staff,
		pending_staff=pending_staff
	)
	
	
@admin.route('/staff/<int:staff_id>/update-status', methods=['POST'])
@login_required
def update_staff_status(staff_id):

	staff = Staff.query.get(staff_id)

	if staff.status == "pending":
	
		action = request.form.get('action')

		if action == "approve":
			staff.status = "active"
			
		elif action == "reject":
			db.session.delete(staff)
			
		db.session.commit()
		
	else:
	
		status = request.form.get('status')
		
		staff.status = status
		
		db.session.commit()
	
	next_page = request.form.get('next')
	return redirect(next_page)
	
	
@admin.route('staff/<int:staff_id>/delete_staff', methods=["POST"])
@login_required
def delete_staff(staff_id):
	
	staff = Staff.query.get(staff_id)
	
	db.session.delete(staff)
	db.session.commit()
	
	next_page = request.form.get('action')
	return render_template(next_page)
	

#################### Trek ####################
@admin.route('/treks', methods=["GET"])
@login_required
def treks():

	base_query = Trek.query
	
	total_treks = base_query.order_by(Trek.trek_id.desc()).all()
	pending_treks = base_query.filter_by(status="pending").order_by(Trek.trek_id.desc()).all()
	approved_treks = base_query.filter_by(status="approved").order_by(Trek.trek_id.desc()).all()
	open_treks = base_query.filter_by(status="open").order_by(Trek.trek_id.desc()).all()
	closed_treks = base_query.filter_by(status="closed").order_by(Trek.trek_id.desc()).all()
	active_treks = base_query.filter_by(status="started").order_by(Trek.trek_id.desc()).all()
	completed_treks = base_query.filter_by(status="completed").order_by(Trek.trek_id.desc()).all()
	unassigned_treks = base_query.filter( Trek.assigned_staff == None ).order_by(Trek.trek_id.desc()).all()

	current_filter = request.args.get('filter', '')
	
	if current_filter == "total":
		treks = total_treks
		
	elif current_filter == "active":
		treks = active_treks
		
	elif current_filter == "open":
		treks = open_treks
		
	elif current_filter == "pending":
		treks = pending_treks
		
	elif current_filter == "approved":
		treks = approved_treks
		
	elif current_filter == "closed":
		treks = closed_treks
		
	elif current_filter == "completed":
		treks = completed_treks
		
	elif current_filter == "unassigned":
		treks = unassigned_treks
		
	else:
		query = base_query
		
		trek_id = request.args.get('trek_id', '')
		trek_name = request.args.get('trek_name', '').strip()
		trek_location = request.args.get('trek_location', '').strip()
		staff_name = request.args.get('staff_name', '').strip()
		status = request.args.get('status', '')
		
		if trek_id:
			query = query.filter(Trek.trek_id==trek_id)
			
		if trek_name:
			query = query.filter(Trek.trek_name.ilike(f"%{trek_name}%"))
			
		if trek_location:
			query = query.filter(Trek.trek_location.ilike(f"%{trek_location}%"))
			
		if staff_name:
			query = query.join(Staff, Staff.staff_id==Trek.assigned_staff).filter(Staff.staff_name.ilike(f"%{staff_name}%"))
			
		if status:
			query = query.filter(Trek.status==status)
		
		treks=query.order_by(Trek.trek_id.desc()).all()

	return render_template(
		'admin/treks.html',
		total_treks=total_treks,
		pending_treks=pending_treks,
		approved_treks=approved_treks,
		open_treks=open_treks,
		closed_treks=closed_treks,
		active_treks=active_treks,
		completed_treks=completed_treks,
		unassigned_treks=unassigned_treks,
		treks=treks
	)
	
	
@admin.route('/trek/<int:trek_id>/update-status', methods=['POST'])
@login_required
def update_trek_status(trek_id):

	trek = Trek.query.get(trek_id)

	if trek.status == "pending":
	
		action = request.form.get('action')

		if action == "approve":
			trek.status = "approved"
			
		elif action == "reject":
			db.session.delete(trek)
			
		db.session.commit()
		
	else:
	
		status = request.form.get('status')
		
		if status == "completed":
			bookings = Booking.query.filter_by(
				trek_id = trek.trek_id,
				status = "booked"
			).all()
			
			for booking in bookings:
				booking.status = "completed"
		
		trek.status = status
		
		db.session.commit()
	
	next_page = request.form.get('next')
	return redirect(next_page)
	
	
@admin.route('trek/<int:trek_id>/delete_trek', methods=["POST"])
@login_required
def delete_trek(trek_id):

	trek = Trek.query.get(trek_id)
	
	bookings = Booking.query.filter_by(
		trek_id = trek.trek_id,
		status = "booked"
	).all()
	
	for booking in bookings:
		booking.status = "cancelled"
	
	db.session.delete(trek)
	db.session.commit()
	
	flash("Trek Deleted Successfully!", "success")
	
	next_page = request.form.get('next')
	return redirect(next_page)
	
	
@admin.route('trek/add_trek', methods=['GET', 'POST'])
@login_required
def add_trek():
	
	staff = Staff.query.filter_by(status='active').all()
	
	if request.method == 'POST':
	
		next_page = request.form.get('next')
	
		assigned_staff_id = request.form.get('assigned_staff_id')
		
		start_date = datetime.strptime(
			request.form.get('start_date'),
			'%Y-%m-%d'
		)

		end_date = datetime.strptime(
			request.form.get('end_date'),
			'%Y-%m-%d'
		)

		if end_date < start_date:

			flash(
				'End date cannot be earlier than start date.',
				'danger'
			)

			return redirect(url_for('admin.add_trek', staff=staff, previous_page=next_page))

		trek = Trek(

			trek_name=request.form.get('trek_name'),

			trek_location=request.form.get('trek_location'),

			difficulty=request.form.get('difficulty'),

			duration=int(request.form.get('duration')),

			available_slots=int(
				request.form.get('available_slots')
			),

			assigned_staff_id=(
				int(assigned_staff_id)
				if assigned_staff_id
				else None
			),

			status=request.form.get('status'),
		
			start_date=start_date,

			end_date=end_date

		)

		db.session.add(trek)

		db.session.commit()

		flash(
			'Trek created successfully.',
			'success'
		)
		
		return redirect(next_page)

	previous_page = request.args.get('previous')
	return render_template('admin/add_trek.html',staff=staff, previous_page=previous_page)
	
	
@admin.route('/edit_trek/<int:trek_id>', methods=['GET', 'POST'])
@login_required
def edit_trek(trek_id):

	trek = Trek.query.get(trek_id)

	staff = Staff.query.filter_by(status='active').all()
	
	next_page = request.args.get("next", "")
	print(next_page)

	if request.method == 'POST':

		start_date = request.form.get('start_date', '')
		end_date = request.form.get('end_date', '')
		trek_location = request.form.get('trek_location', '')
		trek_name = request.form.get('trek_name', '')
		difficulty = request.form.get('difficulty')
		duration = request.form.get('duration')
		status = request.form.get('status')
		assigned_staff_id = request.form.get('assigned_staff_id', '')
		new_slots = request.form.get('total_slots', '')
		
		if start_date:
			start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
		
		if end_date:
			end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
		
		if end_date < start_date:

			flash('End date cannot be earlier than start date.', 'danger')

			return redirect(url_for(
					'admin.edit_trek',
					trek_id=trek_id,
					trek=trek,
					next_page=next_page
				))
		
		if trek_name:
			trek.trek_name = trek_name
			
		if trek_location:
			trek.trek_location = trek_location
			
		if difficulty:
			trek.difficulty = difficulty
		
		if duration:
			trek.duration = int(duration)
			
		if new_slots:
		
			booked_slots = trek.bookings.filter_by(status="booked").count()

			if int(new_slots) < booked_slots:

				flash(
					f'Available slots cannot be less than registered participants ({booked_slots}).',
					'danger'
				)

				return redirect(
					url_for(
						'admin.edit_trek',
						trek_id=trek_id,
						trek=trek,
						next_page=next_page
					)
				)
		
			trek.available_slots = int(new_slots) - booked_slots
			
		if assigned_staff_id:
			trek.assigned_staff_id = assigned_staff_id
			
		if status:
			trek.status = status
			
		if start_date:
			trek.start_date = start_date
			
		if end_date:
			trek.end_date = end_date

		db.session.commit()

		flash(
			'Trek updated successfully.',
			'success'
		)

		return redirect(next_page)
		
	total_slots = (
		trek.available_slots +
		Booking.query.filter_by(
		    trek_id=trek.trek_id,
		    status="booked"
		).count()
	)

	return render_template(
		'admin/edit_trek.html',
		trek_id=trek_id,
		trek=trek,
		staff=staff,
		total_slots=total_slots,
		next_page=next_page
	)

	
	
#################### Booking ####################
@admin.route('/bookings', methods=["GET"])
@login_required
def bookings():

	total_bookings = Booking.query.order_by(Booking.booking_id.desc()).all()
	confirmed_bookings = Booking.query.filter_by(status="booked").order_by(Booking.booking_id.desc()).all()
	cancelled_bookings = Booking.query.filter_by(status="cancelled").order_by(Booking.booking_id.desc()).all()
	completed_bookings = Booking.query.filter_by(status="completed").order_by(Booking.booking_id.desc()).all()
	
	current_filter = request.args.get('filter', '')
	
	if current_filter == "confirmed":
		bookings = confirmed_bookings
		
	elif current_filter == "cancelled":
		bookings = cancelled_bookings
		
	elif current_filter == "completed":
		bookings = completed_bookings
		
	elif current_filter == "total":
		bookings = total_bookings
		
	else:
		booking_id = request.args.get('booking_id', '')
		username = request.args.get('username', '').strip()
		staff_name = request.args.get('staff_id', '').strip()
		trek_name = request.args.get('trek_name', '').strip()
		trek_location = request.args.get('trek_location', '').strip()
		status = request.args.get('status', '')
		
		query = Booking.query.join(Booking.user).join(Booking.trek)
		
		if booking_id:
			query = query.filter(Booking.booking_id==booking_id)
			
		if username:
			query = query.filter(User.username.ilike(f"%{username}%"))
		
		if trek_name:
			query = query.filter(Trek.trek_name.ilike(f"%{trek_name}%"))
			
		if trek_location:
			query = query.filter(Trek.trek_location.ilike(f"%{trek_location}%"))
			
		if status:
			query = query.filter(Status.status==status)
			
		bookings = query.order_by(Booking.booking_id.desc()).all()

	return render_template(
		'admin/bookings.html',
		total_bookings=total_bookings,
		confirmed_bookings=confirmed_bookings,
		cancelled_bookings=cancelled_bookings,
		completed_bookings=completed_bookings,
		bookings=bookings
	)
	

	
