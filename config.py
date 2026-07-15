import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///tmsdb.sqlite3')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@treko.com')
	ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin#123')
