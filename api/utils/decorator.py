from functools import wraps
from ..models.users import Admin
from http import HTTPStatus
from flask_jwt_extended import get_jwt, verify_jwt_in_request


# A function that returns the type of user based on the id
def user_type(id:int):
    user = Admin.query.filter_by(id=id).first()
    if user:
        return user.admin
    else:
        return None


# A custom decorator that verifies that the JWT is present in the request,
# and insures that the owner of this JWT is an administrator

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if user_type(claims['sub']) == 'admin':
                return fn(*args, **kwargs)
            else:
                return {"message": "Administration access required"}, HTTPStatus.FORBIDDEN

        return decorator
        
    return wrapper