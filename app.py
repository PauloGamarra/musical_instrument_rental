from flask import Flask, render_template, request, redirect, url_for
from data.database import DatabaseConnector
from data.models import Users
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
    with session_scope() as session:
        user = session.query(Users).get(int(user_id))
        session.expunge_all()
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


def register(form):
    username = form["username"]
    password = form["password"]
    email = form["email"]

    with session_scope() as session:
        nameQuery = session.query(Users).filter(or_(Users.name == username, Users.email == email)).first()
        if (nameQuery):
            print("Usuario ja existe")
            return render_template('index.html', error_register="Usuário já existe")
        else:
            user = Users(name=username, email=email, password=password)
            session.add(user)
            session.commit()
            login_user(user, remember=True)
            return render_template('register_success.html')


def login(form):
    username_email = form["username_email"]
    password = form["password"]

    with session_scope() as session:
        user_user = session.query(Users).filter_by(name=username_email).first()
        user_email = session.query(Users).filter_by(email=username_email).first()
        user = user_user or user_email
        if (user and user.password == password):
            login_user(user, remember=True)
            return redirect('/logged')
        elif (user):
            return render_template('index.html', error_login="Senha Incorreta")
        else:
            return render_template('index.html', error_login="Usuário inexistente")

if __name__ == '__main__':
    app.run()
