from functools import wraps
from flask import session, url_for, redirect, request
from src.app import app


def requires_login(func): # el decorator recibe como parametro la funcion que se le pasa
    @wraps(func)
    def decorated_funcion(*args, **kwargs): #llamate con los args que tengas
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))      # OJO creo que es login solo
        return func(*args, **kwargs) # func(...) args: func(5,6). kwargs: func(x=5, y=6) key word args
    return decorated_funcion

# next=request.path --> como se redirige  al login, despues de loguearsse vuelve a alerts - el path actual


def requires_admin_permissions(func): # el decorator recibe como parametro la funcion que se le pasa
    @wraps(func)
    def decorated_funcion(*args, **kwargs): #llamate con los args que tengas
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in app.config['ADMINS']:
            return redirect(url_for('users.login_user')) #, message="You need to be an admin to access that"))
        return func(*args, **kwargs)
    return decorated_funcion