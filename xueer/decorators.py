# coding:utf-8

from functools import wraps
from flask import abort, request, g
from flask_login import current_user
from xueer.models import User
import base64


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    # "Basic Base64("token:")"
    @wraps(f)
    def decorated(*args, **kwargs):
        token_header = request.headers.get('authorization', None)
        if token_header:
            token_hash = token_header[6:]
            token_8 = base64.b64decode(token_hash)
            token = token_8[:-1]
            g.current_user = User.verify_auth_token(token)
            if not g.current_user.is_administrator():
                abort(403)
            return f(*args, **kwargs)
    return decorated


def admin_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_administrator():
             abort(403)
        return f(*args, **kwargs)
    return decorated
