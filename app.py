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
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        print("username:" + username)
        print("senha:" + password)
        print("email:" + email)

        with session_scope() as session:
            user = Users(name=username, email=email, password=password)

            session.add(user)

            session.commit()

        return redirect('/login-feito')
    else:
        return render_template('index.html', nome="Marcos")

@app.route('/login-feito', methods=["GET"])
def login_feito():
    return render_template('login-feito.html')


if __name__ == '__main__':
    app.run()
