# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models
import requests
import datetime

MESSAGES_RECEIVED_CHANNEL = 'messages received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

def getBotResponse(received):
    response = db.session.query(models.Responses.response).filter_by(message=received)
    db.session.add(models.Messages(received, response));
    db.session.commit()
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

def emit_all_messages(channel):
    all_messages = [ \
        [db_message.response, db_message.message] for db_message in \
        db.session.query(models.Messages).all()
    ]
    print(all_messages)
    socketio.emit('display', {
        'allMessages': all_messages
    })

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('new message input')
def on_new_message(data):
    print("Got an event for new message input with data:", data["message"])
    
    getBotResponse(data["message"])

@app.route('/')
def index():
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
