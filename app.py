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

count = 0
name = ''
def getJoke():
    print('Getting a joke from web')
    url ='https://geek-jokes.sameerkumar.website/api?format=json'
    response = requests.get(url)
    json_body = response.json()
    translation = json_body["joke"]
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    db.session.add(models.Messages(translation, 'server',time));
    db.session.commit()
    
def getTranslation(text):
    print('Sending text to be translated')
    url = 'https://api.funtranslations.com/translate/valyrian.json?text='+text
    response = requests.get(url)
    json_body = response.json()
    print(response)
    if(response == '<Response [200]>'):
        translation = 'In Valyrian '+text+ ' is '+ json_body["contents"]["translated"]
    else:
        translation = "Sorry the translation api is down right now. Try again later."
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    db.session.add(models.Messages(translation, 'server',time));
    db.session.commit()
    
def getBotResponse(message):
    print('Getting bot response')
    hold = message.split(' ')
    
    if(len(message)>4):
        if(message[-4:] == '.jpg' or message[-4:] == '.gif' or message[-4:] == '.png'):
            response = message
            now = datetime.datetime.now()
            time = now.strftime("%H:%M:%S")
            db.session.add(models.Messages(response, 'image', time));
            db.session.commit()
        elif(message[:4] == 'http'):
            response = message
            now = datetime.datetime.now()
            time = now.strftime("%H:%M:%S")
            db.session.add(models.Messages(response, 'link', time));
            db.session.commit()
        elif(len(hold)==2):
            if(hold[0] == "!!" and hold[1] == "joke"):
                getJoke()
        elif(len(hold) >=3):
            if(hold[0] == "!!" and hold[1] == "funtranslate"):
                getTranslation(' '.join(map(str, hold[2:])))
    if(response == ''):
        response = db.session.query(models.Responses.response).filter_by(message=message).first()
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        db.session.add(models.Messages(response, 'server', time));
        db.session.commit()
    
def emit_all_messages(channel):
    all_messages = [ \
        [db_message.who, db_message.message, db_message.time,] for db_message in \
        db.session.query(models.Messages).all()
    ]
    socketio.emit(channel, {
        'allMessages': all_messages,
    })

@socketio.on('connect')
def on_connect():
    print('Someone connected! Waiting for them to login')
    
@socketio.on('new google user')
def on_new_google_user(data):
    global name 
    name = data["name"]
    global count
    count+=1
    print('Someone connected!')
    socketio.emit('connection', {
        'connection': 'connected',
        'count': count
    })
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    print("Got an event for new google user input with data:", data)
    
    
@socketio.on('disconnect')
def on_disconnect():
    global count
    count-=1
    print('Someone disconnected!')
    socketio.emit('connection', {
        'connection': 'disconnected',
        'count': count
    })

@socketio.on('new message input')
def on_new_message(data):
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    print("Got an event for new message input with data:", data["message"])
    print(time)
    db.session.add(models.Messages(data["message"], 'client', time));
    db.session.commit()
    getBotResponse(data["message"])
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@app.route('/')
def index():
    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
