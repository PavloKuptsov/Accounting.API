from functools import wraps
from flask import request, Response, g

from config import auth
from repository import Repository


def check_auth(username, password):
    repository = Repository()
    user = repository.search_user(username)
    return user and username == user.username and password == user.password


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

