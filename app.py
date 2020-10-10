from flask import Flask, render_template, request, redirect, url_for
from data.database import DatabaseConnector
from data.models import Users


app = Flask(__name__)

db = DatabaseConnector()
db.connect()

session_scope = db.get_session_scope()

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

def register(form):
    username = form["username"]
    password = form["password"]
    email = form["email"]

    with session_scope() as session:
        nomeQuery = session.query(Users).filter_by(name=username).first()
        if (nomeQuery):
            print("Usuario ja existe")
            return render_template('index.html', error_register="Usuário já existe")
        else:
            user = Users(name=username, email=email, password=password)
            session.add(user)
            session.commit()
            return render_template('register_success.html')


def login(form):
    username = form["username"]
    password = form["password"]
    email = form["email"]

    with session_scope() as session:
        nomeQuery = session.query(Users).filter_by(name=username, email=email, password=password).first()
        if (nomeQuery):
            return render_template('login_success.html')
        else:
            return render_template('index.html', error_login="Usuário inexistente")

if __name__ == '__main__':
    app.run()
