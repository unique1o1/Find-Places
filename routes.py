from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from models import db, User, Places, Token

from sendNoti import send_push_message
from forms import SignupForm, LoginForm, AddressForm
import os
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0@localhost:5432/learningflask'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = "thisisyunik"
# db.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "thisisyunik"
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/notification", methods=['GET', 'POST'])
def notification():

    if request.method == "POST":
        token = request.get_json()

        db.create_all()
        print(token['token'])
        obj = Token(tokenID=token['token'])
        db.session.add(obj)
        db.session.commit()
        return jsonify(sucess=True)
    return render_template("notification.html")


@app.route("/api/notification", methods=['GET'])
def notificationAPI():
    send_push_message(request.args['token'], request.args['msg'])
    return jsonify(message=request.args['msg'], token=request.args['token'])


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:

            newuser = User(form.first_name.data, form.last_name.data,
                           form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email

            return redirect(url_for('home'))

    elif request.method == "GET":
        if 'email' in session:
            return redirect(url_for('home'))
        return render_template('signup.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if form.validate() == False:
            return render_template("login.html", form=form)
        elif user is None:
            return render_template("login.html", form=form, error="It looks like you haven't signed up")

        else:

            password = form.password.data

            if user.check_password(password):

                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return render_template('login.html', form=form, pass_error="Password invalid")

    elif request.method == 'GET':
        if 'email' not in session:
            return render_template('login.html', form=form)
        else:
            return redirect(url_for('home'))


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route("/home", methods=["GET", "POST"])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))

    form = AddressForm()
    places = []
    geoloc = []
    if request.method == 'POST':
        place = Places()
        address = form.address.data

        geoloc = place.address2geo(address)
        places = place.query(address)
        return render_template('home.html', form=form, places=places, my_coordinates=geoloc)

    return render_template("home.html", form=form, places=places, my_coordinates=geoloc)


if __name__ == "__main__":
    app.run(debug=True)
