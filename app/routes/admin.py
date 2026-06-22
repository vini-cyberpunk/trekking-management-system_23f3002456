from flask import Blueprint, render_template, request, redirect, url_for
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

@admin.route('/users', methods=['GET'])
@login_required
def users():

    from app.models import User
    
    query = User.query
    
    total_users = query.count()
    active_users = query.filter_by(status="active").count()
    inactive_users = query.filter_by(status="inactive").count()

    username = request.args.get('username', '').strip()
    user_id = request.args.get('user_id', '').strip()
    user_contact = request.args.get('user_contact', '').strip()
    status = request.args.get('status', '').strip()

    query = User.query

    if username:
        query = query.filter(
            User.username.ilike(f"%{username}%")
        )

    if user_id:
        query = query.filter(
            User.user_id == user_id
        )

    if user_contact:
        query = query.filter(
            User.user_contact.ilike(f"%{user_contact}%")
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
        users=users
    )
	
	
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

	staff = Staff.query.get_or_404(staff_id)
	status = request.form.get('status')

	if status not in ['pending', 'active', 'inactive']:
		return redirect(url_for('admin.staff'))

	staff.status = status

	db.session.commit()

	return redirect(url_for('admin.staff'))
	
	
@admin.route('/treks', methods=["GET"])
@login_required
def treks():

	return render_template('admin/treks.html')
	
@admin.route('/bookings', methods=["GET"])
@login_required
def bookings():

	return render_template('admin/bookings.html')
	

	
