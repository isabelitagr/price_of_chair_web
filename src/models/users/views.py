from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.users.errors as UserErrors
from src.models.users.user import User
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__) # (name, import_name, template_folders...) import name es unique a esta file cuando corre


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))  #url_for busca el archivo del metodo en el parametro .user_alerts --> el punto es porque es en est archivo
        except UserErrors.UserError as e:
            return e.message                # asi no tengo que hacer 2 excepts, uno para UserNotExistsError y otro para IncorrectPasswordError

    return render_template('users/login.html') #send the user an error if the login was invlid.


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/register.html')

@user_blueprint.route('/alerts') #como no vamos a querer ver las de otros no hace falta poner /alerts/<user_id>
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    alerts = user.get_alerts()
    return render_template('users/alerts.html', alerts=alerts) # el nombre de alerts izq es el nombre que se va a usar en el template


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))

@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass