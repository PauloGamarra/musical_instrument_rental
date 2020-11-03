from flask import Flask, render_template, request, redirect, url_for
from data.database import DatabaseConnector
from data.models import Users
from data.auth import Auth
from flask_login import LoginManager, login_required, login_user, logout_user
from sqlalchemy import or_


app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='segredo_hihi'
)

# Database Config
db = DatabaseConnector()
db.connect()
session_scope = db.get_session_scope()

# Login Config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"


# Necessary for flask-login, gives it the user using its id
@login_manager.user_loader
def load_user(user_id):
    user, err = Auth(session_scope).get_user(user_id=user_id)

    return user


# Login and Register page
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        postType = request.form["type"]

        if (postType == "register"):
            return register(request.form)
        elif (postType == "login"):
            return login(request.form)
    else:
        return render_template('index.html')


# Route which the user is directed to when they log-in, can only be seen when logged-in
@app.route('/logged', methods=["GET"])
@login_required
def logged_page():
    return render_template('login_success.html')


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/destacar-instrumentos', methods=["GET", "POST"])
@login_required
def feature_instruments():
    if request.method == 'POST':
        pass
    else:
        return render_template('feature-instruments.html')


@app.route('/anunciar-instrumento', methods=["GET", "POST"])
@login_required
def announce_instruments():
    if request.method == 'POST':
        pass
    else:
        return render_template('announce-instruments.html')


def register(form):
    auth = Auth(session_scope)

    username = form["username"]
    password = form["password"]
    email = form["email"]

    userQuery, err = auth.get_user(email=email)

    if userQuery:
        print("Usuario ja existe")
        return render_template('index.html', error_register="Usuário já existe")
    else:
        user, err = auth.create_user(name=username, email=email, password=password)

        if err:
            print(f"Alguma coisa deu errado: {err}")
            return render_template('index.html', error_login="Alguma coisa deu errado.")
        else:
            login_user(user, remember=True)
            return render_template('register_success.html')


def login(form):
    auth = Auth(session_scope)
    email = form["email"]
    password = form["password"]

    user, err = auth.get_user(email=email)

    if err:
        print(f"Alguma coisa deu errado: {err}")
        return render_template('index.html', error_login="Alguma coisa deu errado.")
    elif user:
        if user.password == password:
            login_user(user, remember=True)
            return redirect('/logged')
        else:
            return render_template('index.html', error_login="Senha Incorreta")
    else:
        return render_template('index.html', error_login="Usuário inexistente")

if __name__ == '__main__':
    app.run()
