from flask import Flask, render_template

from src.common.database import Database


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = '123' # para asegurar la cookie
# generalmente se usan 32 caracteres random de letrs y numeros un numero random de 32 bits
#  cuando un browser pide a nuestra aplicacion una pag, Flask va a poner una cookie con un session_id.
# este cookie(session_id) se va a usar para linkear el browser con una session especifica en nuestro server.
# la session en el server va a tener info como el session['email],que usamos para identificar si el usuario esta logueado o no.

@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def home():
    return render_template('home.html')


# para que jinja reconozca las rutas. se aclara que todoo lo del user blueprint esta precedido por /users, por ejemplo
from src.models.users.views import user_blueprint
from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(alert_blueprint, url_prefix='/alerts')
app.register_blueprint(store_blueprint, url_prefix='/stores')

