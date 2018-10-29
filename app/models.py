from datetime import datetime
from app import db


class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))


class Messages(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(999))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	sender = db.Column(db.Integer, db.ForeignKey('users.id'))
	receiver = db.Column(db.Integer, db.ForeignKey('users.id'))