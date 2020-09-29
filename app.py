from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        print("username:" + request.form["username"])
        print("senha:" + request.form["password"])
        print("email:" + request.form["email"])
        return redirect('/login-feito')
    else:
        return render_template('index.html', nome="Marcos")

@app.route('/login-feito', methods=["GET"])
def login_feito():
    return render_template('login-feito.html')


if __name__ == '__main__':
    app.run()
