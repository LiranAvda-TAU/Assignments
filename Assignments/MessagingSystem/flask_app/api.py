from flask import Flask, request, session, g, abort, jsonify

from MessagingSystem.Backend.Message import Message
from MessagingSystem.flask_app import db
import os
from marshmallow import Schema, fields


class UserQuerySchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class MessageQuerySchema(Schema):
    receiver_name = fields.Str(required=True)
    subject = fields.Str(required=True)
    body = fields.Str(required=True)


class MessageIdQuerySchema(Schema):
    message_id = fields.Int(required=True)


app = Flask(__name__)
app.config.from_object(__name__)  # load config from this file , api.py
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flask_app.db'),
    SECRET_KEY='development key',
    USERNAME='liran',
    PASSWORD='12345'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

user_schema = UserQuerySchema()
message_schema = MessageQuerySchema()
message_id_schema = MessageIdQuerySchema()

db.init_app(app)


@app.route("/")
def home():
    return "Welcome to my messaging system!"


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method != 'POST':
        error = 'Request method should be POST.'
    else:
        error = user_schema.validate(request.args)
        if not error:
            username = request.args['username']
            password = request.args['password']
            app_db = db.get_db()

            if app_db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(username)

            if not error:
                app_db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, password)
                )
                app_db.commit()
                return "OK"

    abort(400, str(error))


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method != 'POST':
        error = 'Request method should be POST.'
    else:
        error = user_schema.validate(request.args)
        if not error:
            username = request.args['username']
            password = request.args['password']
            app_db = db.get_db()
            user = app_db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

            if user is None:
                error = 'Incorrect username.'
            elif user['password'] != password:
                error = 'Incorrect password.'

            if not error:
                session.clear()
                session['user_id'] = user['id']
                print(session['user_id'])
                return "OK"

    abort(400, str(error))


@app.route('/logout', methods=('GET', 'POST'))
def logout():
    if request.method != 'POST':
        error = 'Request method should be POST.'
        abort(400, str(error))
    session.clear()
    return "OK"


@app.route('/send', methods=('GET', 'POST'))
def send_message():
    if request.method != 'POST':
        error = 'Request method should be POST.'
    else:
        error = message_schema.validate(request.args)
        if not error:
            receiver_name = request.args['receiver_name']
            subject = request.args['subject']
            body = request.args['body']

            if 'user_id' not in session:  # not logged in
                error = 'You need to login before performing this request.'

            if not error:
                app_db = db.get_db()
                receiver = app_db.execute(
                    'SELECT * FROM user WHERE username = ?', (receiver_name,)
                ).fetchone()

                if receiver is None:
                    error = 'Incorrect username for receiver.'

                if not error:
                    app_db.execute(
                        'INSERT INTO message (sender_id, receiver_id, subject, body, new)'
                        ' VALUES (?, ?, ?, ?, ?)',
                        (session['user_id'], receiver['id'], subject, body, True,)
                    )
                    app_db.commit()
                    return "OK"
    abort(400, str(error))


@app.route('/get_all')
def get_messages():
    if not session.get('logged_in'):  # not logged in
        return 'You need to login before performing this request.'
    messages = db.get_db().execute(
        'SELECT m.id, m.sender_id, m.subject, m.body, m.created'
        'FROM message m'
        'WHERE m.sender_id = ?',
        (session['user_id'],))
    return messages


def get_new_messages():
    if not session.get('logged_in'):  # not logged in
        return 'You need to login before performing this request.'
    messages = db.get_db().execute(
        'SELECT m.id, m.sender_id, m.subject, m.body, m.created'
        'FROM message m'
        'WHERE m.sender_id = ? AND m.new IS TRUE',
        (session['user_id'],))
    return messages


@app.route('/read')
def read_message():
    if 'user_id' not in session:
        error = 'You need to login before performing this request.'
    else:
        error = message_id_schema.validate(request.args)
        if not error:
            message_id = request.args['message_id']
            app_db = db.get_db()
            message = app_db.execute('SELECT * FROM message WHERE id = ? AND receiver_id = ?',
                                          (message_id, session['user_id'],)).fetchone()
            if message is None:
                error = 'Message id {0} does not exist or was not sent to you.'.format(message_id)
                abort(404, str(error))
            else:
                app_db.execute(
                    'UPDATE message SET new = ? WHERE id = ?', (message_id)
                )
                db.commit()
                return str(Message.from_db_to_message(message))
    abort(400, str(error))


def delete_message():
    error = None
    if not session.get('logged_in'):
        error = 'You need to login before performing this request.'
    message_id = request.form['message_id']
    if not error:
        app_db = db.get_db()
        app_db.execute('DELETE FROM message WHERE id = ?', (message_id,))
        app_db.commit()
        return "OK"
    return error


if __name__ == "__main__":
    app.run(debug=True)
