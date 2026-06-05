import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
	ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

