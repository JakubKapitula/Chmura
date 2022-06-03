from flask import Flask, render_template, abort, make_response, request, redirect, url_for
from flask_mail import Mail, Message
from AzureDB import AzureDB
from flask_dance.contrib.github import make_github_blueprint, github
import secrets
import os
import requests

app = Flask(__name__)
mail = Mail(app)

app.secret_key = secrets.token_hex(16)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
github_blueprint = make_github_blueprint(
    client_id="56c4b15e6784fa925efb",
    client_secret="6dd8a3181fbb39fa4bb26769d6ecea4fbc0f62ca",
)
app.register_blueprint(github_blueprint, url_prefix='/login')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jakub.kapitula.priv@gmail.com'
app.config['MAIL_PASSWORD'] = '12345'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

@app.route('/')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
    if account_info.ok:
        return render_template('index.html')
    return '<h1>Request failed!</h1>'

@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/index2')
def index2():
    return render_template('index2.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/rock')
def rock():
    return render_template('rock.html')


@app.route('/gallery2')
def gallery2():
    return render_template('gallery2.html')


@app.route("/Baza", methods=['GET', 'POST'])
def Baza():
    with AzureDB() as a:
        if request.method == 'POST':
            a.azureAddData(imie=request.form['imie'], text=request.form['text'])
        data = a.azureGetData()
    return render_template("baza.html", data=data)

@app.route('/rest', methods=['GET', 'POST'])
def rest():
    if request.method == 'GET':
        return render_template('rest.html')
    if request.method == 'POST':
        info = requests.get('http://localhost:5000')
        dane = info.json()
        nr = request.form['Nr']
        Wykonawca = dane[nr]['Wykonawca']
        Tytul = dane[nr]['Tytul']
        Format = dane[nr]['Format']
        T1 = "Wykonawca: %s " % (Wykonawca)
        T2 = "Tytuł: %s " % (Tytul)
        T3 = "Format : %s " % (Format)
        return render_template('rest.html', data1=T1, data2=T2, data3=T3)
    return render_template('rest.html')

@app.route('/sendmail')
def sendmail():
    msg = Message('Hello', sender='yourId@gmail.com', recipients=['someone1@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return render_template('send_mail.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.route('/error_not_found')
def error_not_found():
    response = make_response(render_template('404.html', name='ERROR 404'), 404)
    response.headers['X-Something'] = 'A value'
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
