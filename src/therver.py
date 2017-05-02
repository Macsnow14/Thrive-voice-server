# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-02 23:48:34
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-03 00:59:50
from flask import Flask, session, request
from flask_script import Manager
from flask.ext.restful import Api, abort, reqparse, Resource


app = Flask(__name__)
app.secret_key = b'\xda\xc6\xeb:\xc6t\xba\xdf\xf6\x06\xbb\x9b\xd5\xb0p\x89\xe2\x9cK\x88K\x04\xe7\x0b\xa2?\x7f\xa7\xa8#-\xfd7'
manager = Manager(app)
api = Api(app)
userOnline = {}
parser = reqparse.RequestParser()
parser.add_argument('username', type=str)


def abortIfUserUnauthenticated(request):
    if 'username' not in session:
        abort(404, message="user not online.")


def abortIfUserNotOnline(username):
    if username not in userOnline:
        abort(403, message="Unauthenticated, you need to login first.")


def abortIfUsernameDuplicate(username):
    if username in userOnline:
        abort(400, message="Duplicate username, pick another one.")


class UserOnline(Resource):
    """to check who's one the line.

    treat online users as a resource and use restful design pattern.

    Extends:
        Resource

    Methods:
        get -- get user list.
        post -- user log in.
        delete -- user log out.
    """

    def get(self):
        abortIfUserUnauthenticated(request)
        return userOnline.keys(), 200

    def post(self):
        username = parser.parse_args()['username']
        abortIfUsernameDuplicate(username)
        user = {'host': request.remote_addr, 'port': request.environ.get('REMOTE_PORT')}
        userOnline[username] = user
        session['username'] = username
        return userOnline[username], 201

    def delete(self):
        abortIfUserUnauthenticated(request)
        username = session['username']
        session.pop('username')
        userOnline.pop(username)
        return '', 204


api.add_resource(UserOnline, '/', '/userOnline')


if __name__ == '__main__':
    manager.run()
