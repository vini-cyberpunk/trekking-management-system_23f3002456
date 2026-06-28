from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required


admin = Blueprint('admin', __name__)

#################### ADMIN ####################
@admin.route('/dashboard', methods=['GET'])
@login_required
def dashboard():

	from app.models import User, Login, Trek, Booking, Staff
	
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

	from app.models import User, Login

	base_query = User.query.join(Login)

	total_users = base_query.count()
	active_users = base_query.filter(User.status == "active").count()
	inactive_users = base_query.filter(User.status == "inactive").count()

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

	users = query.order_by(
		User.user_id.desc()
	).all()

	return render_template(
		'admin/users.html',
		total_users=total_users,
		active_users=active_users,
		inactive_users=inactive_users,
		users=users,
		username=username,
		user_id=user_id,
		user_contact=user_contact,
		email=email,
		status=status
	)


@admin.route('/users/<int:user_id>/update-status', methods=['POST'])
@login_required
def update_user_status(user_id):
	
	from app import db
	from app.models import User
	
	user = User.query.get(user_id)
	status = request.form.get('status')
	
	user.status = status
	
	db.session.commit()
	
	next_page = request.form.get('next')
	return redirect(next_page)
	
	
@admin.route('user/<int:user_id>/delete_user', methods=["POST"])
@login_required
def delete_user(user_id):
	
	from app import db
	from app.models import User
	
	user = User.query.get(user_id)
	
	db.session.delete(user)
	db.session.commit()
	
	next_page = request.form.get('action')
	return render_template(next_page)
	
	
#################### STAFF ####################
@admin.route('/staff', methods=["GET"])
@login_required
def staff():
	
	from app.models import Staff
	
	staff = Staff.query.all()
	return render_template('admin/staff.html', staff=staff)
	
	
@admin.route('/staff/<int:staff_id>/update-status', methods=['POST'])
@login_required
def update_staff_status(staff_id):

	from app.models import Staff
	from app import db

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
	
	from app import db
	from app.models import Staff
	
	staff = Staff.query.get(staff_id)
	
	db.session.delete(staff)
	db.session.commit()
	
	next_page = request.form.get('action')
	return render_template(next_page)
	

#################### Trek ####################
@admin.route('/treks', methods=["GET"])
@login_required
def treks():

	return render_template('admin/treks.html')
	
	
@admin.route('/trek/<int:trek_id>/update-status', methods=['POST'])
@login_required
def update_trek_status(trek_id):

	from app.models import Trek
	from app import db

	trek = Trek.query.get(trek_id)

	if trek.status == "pending":
	
		action = request.form.get('action')

		if action == "approve":
			trek.status = "approved"
			
		elif action == "reject":
			trek.status = "rejected"
			
		db.session.commit()
		
	else:
	
		status = request.form.get('status')
		
		trek.status = status
		
		db.session.commit()
	
	next_page = request.form.get('next')
	return redirect(next_page)
	
	
@admin.route('trek/<int:trek_id>/delete_trek', methods=["POST"])
@login_required
def delete_trek(trek_id):
	
	from app.models import Trek
	from app import db
	
	trek = Trek.query.get(trek_id)
	
	db.session.delete(trek)
	db.session.commit()
	
	next_page = request.form.get('next')
	return redirect(next_page)
	
	
@admin.route('trek/add_trek', methods=['GET', 'POST'])
@login_required
def add_trek():

	from datetime import datetime
	from app.models import Trek, Staff
	from app import db
	
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
	print(previous_page)
	return render_template('admin/add_trek.html',staff=staff, previous_page=previous_page)
	
	
@admin.route('/edit_trek/<int:trek_id>', methods=['GET', 'POST'])
@login_required
def edit_trek(trek_id):

	from datetime import datetime
	from app import db
	from app.models import Trek, Staff

	trek = Trek.query.get(trek_id)

	staff = Staff.query.filter_by(status='active').all()

	if request.method == 'POST':

		start_date = datetime.strptime(
			request.form.get('start_date'),
			'%Y-%m-%d'
		).date()

		end_date = datetime.strptime(
			request.form.get('end_date'),
			'%Y-%m-%d'
		).date()

		if end_date < start_date:

			flash(
				'End date cannot be earlier than start date.',
				'danger'
			)

			return redirect(
				url_for(
					'admin.edit_trek',
					trek_id=trek_id
				)
			)

		booked = len(trek.bookings)

		new_slots = int(request.form.get('available_slots'))

		if new_slots < booked:

			flash(
				f'Available slots cannot be less than registered participants ({booked}).',
				'danger'
			)

			return redirect(
				url_for(
					'admin.edit_trek',
					trek_id=trek_id
				)
			)

		trek.trek_name = request.form.get('trek_name')

		trek.trek_location = request.form.get('trek_location')

		trek.difficulty = request.form.get('difficulty')

		trek.duration = int(
			request.form.get('duration')
		)

		trek.available_slots = new_slots

		assigned_staff_id = request.form.get('assigned_staff_id')

		trek.assigned_staff_id = (
			int(assigned_staff_id)
			if assigned_staff_id
			else None
		)

		trek.status = request.form.get('status')

		trek.start_date = start_date

		trek.end_date = end_date

		db.session.commit()

		flash(
			'Trek updated successfully.',
			'success'
		)

		return redirect(
			url_for('admin.treks')
		)

	return render_template(
		'admin/edit_trek.html',
		trek=trek,
		staff=staff
	)

	
	
#################### Booking ####################
@admin.route('/bookings', methods=["GET"])
@login_required
def bookings():

	return render_template('admin/bookings.html')
	

	
