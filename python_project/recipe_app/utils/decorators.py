from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import redirect, url_for, flash

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            # Accede a "role" dentro de "sub"
            if claims.get("sub", {}).get("role") != role:
                flash("Permission denied.", "danger")
                return redirect(url_for('index'))
            return fn(*args, **kwargs)
        return decorator
    return wrapper