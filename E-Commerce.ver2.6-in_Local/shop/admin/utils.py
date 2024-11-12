from functools import wraps
from flask import flash, redirect, session, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session or 'admin' not in session:
            flash('Vui lòng đăng nhập tại đây!', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

