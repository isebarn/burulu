
import os

class Config(object):
	SECRET_KEY = 'secret!' 
	DEBUG=True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	REDIS_URL = os.environ.get('REDISCLOUD_URL')