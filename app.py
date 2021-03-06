# app.py
import os
from os.path import join, dirname
import datetime
from dotenv import load_dotenv
import flask
import flask_sqlalchemy
import flask_socketio
from flask import request
import requests
import models


MESSAGES_RECEIVED_CHANNEL = "messages received"
app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

database_uri = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()


def get_joke():
    """
        request random joke from api
    """
    print("Getting a joke from web")
    url = "https://geek-jokes.sameerkumar.website/api?format=json"
    response = requests.get(url)
    json_body = response.json()
    translation = json_body["joke"]
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    db.session.add(models.Messages(translation, "server", time))
    db.session.commit()


def get_translation(text):
    """
        request translation of a text into valyrian from api
    """
    print("Sending text to be translated")
    url = "https://api.funtranslations.com/translate/valyrian.json?text=" + text
    response = requests.get(url)
    json_body = response.json()
    translation = "In Valyrian " + text + " is " + \
        json_body["contents"]["translated"]
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    db.session.add(models.Messages(translation, "server", time))
    db.session.commit()


def get_bot_response(message):
    """
        parse message to check if a bot response is neccessary
        if so get response
    """
    print("Getting bot response")
    hold = message.split(" ")

    if message[:2] != "!!":
        if message[-4:] == ".jpg" or message[-4:] == ".gif" or message[-4:] == ".png":
            now = datetime.datetime.now()
            time = now.strftime("%H:%M:%S")
            db.session.add(models.Messages(message, "image", time))
        elif message[:4] == "http":
            now = datetime.datetime.now()
            time = now.strftime("%H:%M:%S")
            db.session.add(models.Messages(message, "link", time))
    elif message[:2] == "!!":
        if hold[1] == "joke":
            get_joke()
        elif hold[1] == "funtranslate":
            get_translation(" ".join(map(str, hold[2:])))
        else:
            response = (
                db.session.query(models.Responses.response)
                .filter_by(message=message)
                .first()
            )
            now = datetime.datetime.now()
            time = now.strftime("%H:%M:%S")
            db.session.add(models.Messages(response, "server", time))
    db.session.commit()


def emit_all_messages(channel):
    """
        emit messages to the client
    """
    sid = request.sid
    person = db.session.query(models.Authuser.name).filter_by(sid=sid).first()
    db.session.commit()
    print(person.name)
    all_messages = [
        [
            db_message.who,
            db_message.message,
            db_message.time,
        ]
        for db_message in db.session.query(models.Messages).all()
    ]
    socketio.emit(
        channel,
        {
            "allMessages": all_messages,
            "name": person.name
        },
    )


@socketio.on("connect")
def on_connect():
    """
        recognize user connection
    """
    print("Someone connected! Waiting for them to login")


@socketio.on("new google user")
def on_new_google_user(data):
    """
        once user google oAuth is successful
        log user into heroku database
    """
    name = data["name"]
    propic = data["propic"]
    sid = request.sid
    db.session.add(models.Authuser(name, propic, sid))
    db.session.commit()
    all_users = [
        [db_authuser.name, db_authuser.propic, db_authuser.sid]
        for db_authuser in db.session.query(models.Authuser).all()
    ]
    print("Someone connected!")
    socketio.emit(
        "connection", {
            "connection": "connected", "count": len(all_users)})
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    print("Got an event for new google user input with data:", data)


@socketio.on("disconnect")
def on_disconnect():
    """
        remove user from heroku database
        and update user count
    """
    sid = request.sid
    db.session.query(models.Authuser.sid).filter_by(sid=sid).delete()
    db.session.commit()
    all_users = [
        [db_authuser.name, db_authuser.propic, db_authuser.sid]
        for db_authuser in db.session.query(models.Authuser).all()
    ]
    print("Someone disconnected!")
    socketio.emit(
        "connection", {
            "connection": "disconnected", "count": len(all_users)})


@socketio.on("new message input")
def on_new_message(data):
    """
        recieve new mesage and log into database
    """
    sid = request.sid
    name = db.session.query(models.Authuser.name).filter_by(sid=sid).first()
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    print("Got an event for new message input with data:", data["message"])
    print(time)
    db.session.add(models.Messages(data["message"], name, time))
    db.session.commit()
    get_bot_response(data["message"])
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


@app.route("/")
def index():
    """
        specifiy what file to render
    """
    return flask.render_template("index.html")


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
