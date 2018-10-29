from app import app, socketio, db, redis_store

from flask import Flask, render_template, session, request, redirect, make_response
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect

from app.forms import LoginForm, RegisterForm

from app.models import Users, Messages

import json


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		if form.submit.data:			

			email = form.email.data
			password = form.password.data

			u = Users.query.filter_by(email=email, password_hash=password).all()
			if len(u) == 1:
				user = u[0]
				response = make_response(redirect('/chat'))
				response.set_cookie('user_id', str(user.id))				
				return response


		elif form.register.data:
			return redirect('/register')
	
	return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()

	if request.method == 'POST':
		if form.submit.data:
			name = form.name.data
			email = form.email.data
			password = form.password.data
			password_confirm = form.password_confirm.data

			u = Users(name=name, email=email, password_hash=password)
			db.session.add(u)
			db.session.commit()

			return redirect('/')


	return render_template('register.html', title='Sign Up', form=form)


@app.route('/chat')
def index():  	
	return render_template('index.html', async_mode=socketio.async_mode)