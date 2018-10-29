from threading import Lock

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

import redis


async_mode = None

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
redis_store=redis.from_url(app.config.get('REDIS_URL'))

migrate = Migrate(app, db)

socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()

from app import routes, models, socket