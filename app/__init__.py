from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login = LoginManager()

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	login.init_app(app)

	@login.user_loader
	def load_user(user_id):
		from app.models import Login
		return Login.query.get(int(user_id)) 

	from app.routes.auth import auth
	app.register_blueprint(auth)

	from app.routes.admin import admin
	app.register_blueprint(admin, url_prefix='/admin')

	from app.routes.user import user
	app.register_blueprint(user, url_prefix='/user')

	from app.routes.staff import staff
	app.register_blueprint(staff, url_prefix='/staff')

	with app.app_context():
		from app import models
		db.create_all()
		
		admin_email = app.config['ADMIN_EMAIL']
		admin_password = app.config['ADMIN_PASSWORD']
		
		admin = models.Login.query.filter_by(email=admin_email).first()
		
		if not admin:
			admin = models.Login(email=admin_email, password=generate_password_hash(admin_password), role="admin")
			
			db.session.add(admin)
			db.session.commit()
			
	return app

