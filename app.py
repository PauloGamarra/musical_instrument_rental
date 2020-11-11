from flask import Flask, render_template, request, redirect, url_for
from data.database import DatabaseConnector
from data.models import Users
from data.auth import Auth
from data.business import SubPackageInstruments
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import or_
from backend.featuring import SubPackageFeaturing
from backend.announcement import SubPackageAnnouncements
from backend.records import RecordsBackend

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
        instrumentos = request.form.getlist("selecionados")
        sb = SubPackageFeaturing(session_scope)
        sb.saveNew10PopularIntruments(instrumentos)
        return redirect('/destacar-instrumentos')
    else:
        databaseSubsystem = SubPackageInstruments(session_scope)
        allIntruments = set(map(lambda i: i.instrument, databaseSubsystem.get_all_instruments()[0]))

        return render_template('feature-instruments.html', instrumentos=allIntruments)


@app.route('/anunciar-instrumento', methods=["GET", "POST"])
@login_required
def announce_instruments():
    if request.method == 'POST':
        precolist = list(map(lambda x: (float(x.split(",")[0]), int(x.split(",")[1])), request.form.getlist("preco")))

        sp = SubPackageAnnouncements(session_scope)
        sp.saveNewAdvert(
            precolist,
            current_user.email,
            request.form["classe"],
            request.form["tipo"],
            request.form["marca"],
            request.form["modelo"],
            request.form["numero_serie"])
        return redirect('/anunciar-instrumento')
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

@app.route("/vitrine", methods=["POST","GET"])
def vitrine():
    sp = SubPackageAnnouncements(session_scope)
    featured_instruments= [instrument[0] for instrument in sp.loadInstrumentsAndItsPopularitySortedByPopularityAndByAlphabetics()[:10]]
    non_featured_instruments= [instrument[0] for instrument in sp.loadInstrumentsAndItsPopularitySortedByPopularityAndByAlphabetics()[10:]]
    return render_template('vitrine.html', featured_instruments=featured_instruments, non_featured_instruments=non_featured_instruments)

@app.route("/vitrine-tipo-instrumento/<tipo_instrumento>")
def vitrine_tipo_instrumento(tipo_instrumento):
    sp = SubPackageAnnouncements(session_scope)
    adverts_ids = sp.loadActiveAdvertsIdsByInstrument(tipo_instrumento)

    locatorUsernames = [username for username in [sp.loadAdvertLocatorUsernameById(id) for id in adverts_ids]]
    prices = [prices for prices in [sp.loadListOfPricesInBRLByDurationInDaysBrandById(id) for id in adverts_ids]]
    brands = [brand for brand in [sp.loadAdvertInstrumentBrandById(id) for id in adverts_ids]]
    models = [model for model in [sp.loadAdvertInstrumentModelById(id) for id in adverts_ids]]

    adverts = zip(locatorUsernames, prices, brands, models)
    return render_template('vitrine_tipo_instrumento.html', anuncios=adverts)


@app.route("/locacao/<id>", methods=["POST", "GET"])
def locacao(id):
    if request.method == "GET":
        return render_template("locacao.html", user=current_user.name, email=current_user.email,id=id)
    else:
        print(
         request.form["retirada_instrumento"],
         request.form["devolucao_instrumento"],
)       
        return redirect('/locacao/'+id)

@app.route("/historico/<username>")
def historico(username):
    rb = RecordsBackend(session_scope)
    lesseRecords = rb.loadLesseRecords()
    locatorRecords = rb.loadLocatorRecords()
# [{'advert': {'locator': {'id': x, 'name': x, 'email': x}, 
#             'instrument': {'instrument_class': x, 'instrument': x, 'brand': x, 'model': x, 'registry': x}}, 
#             'loan': {'withdrawal': datetime.date(2020, 11, 30), 'devolution': datetime.date(2020, 12, 15), 
#             'lessee': {'id': x, 'name': x, 'email': x}}, 
#             'rating': x}]
    print(records)
    return render_template('historico.html', lesseRecords=lesseRecords, locatorRecords=locatorRecords)

if __name__ == '__main__':
    app.run()
