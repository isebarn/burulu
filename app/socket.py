from app import app, socketio, db, redis_store

from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect

from app.forms import LoginForm, RegisterForm

from app.models import Users, Messages

import json


# Message sent through client
# REFACTOR - 'message'
@socketio.on('client_send_message_to_server', namespace='/test')
def client_send_message_to_server(message):
	user_id = str(request.cookies.get('user_id'))
	friend_id = redis_store.hget('active_chat', user_id).decode('utf-8')

	room_id = '-'.join([friend_id, user_id])	

	message = Messages(body=message['data'], receiver=friend_id, sender=user_id)
	db.session.add(message)
	db.session.commit()

	emit('server_send_message_to_client',
		 {'message': message.body},
		 room=room_id) 		
	

# Fetch all users
@socketio.on('message', namespace='/test')
def handle_message():
	user_id = request.cookies.get('user_id')
	users = Users.query.filter(Users.id != user_id).all()
	emit('users',
		 {'users': json.dumps([{'name': user.name, 'id': user.id} for user in users])},
		 broadcast=False) 


# Fetch chat data from-to user and selected user
@socketio.on('request_chat', namespace='/test')
def request_chat(message):	

	user_id = str(request.cookies.get('user_id'))
	friend_id = str(message['friend_id'])

	room_id = '-'.join([user_id, friend_id])
	redis_store.hset('active_chat', user_id, friend_id)

	join_room(room_id)

	received = Messages.query.filter_by(sender=friend_id, receiver=user_id).all()
	sent = Messages.query.filter_by(sender=user_id, receiver=message['friend_id']).all()
	all_messages = received + sent
	all_messages.sort(key=lambda x: x.id, reverse=False)

	emit('chat', 
		{'chat': json.dumps([{'message': message.body, 'sender': message.sender} for message in all_messages])}, 
		broadcast=False)
