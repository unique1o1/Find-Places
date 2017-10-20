from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from forms import SignupForm, LoginForm

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0@localhost:5432/learningflask'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = "thisisyunik"
# db.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gbfmdypfbudmrc:    f9d75356ba080c2b57cc297159e74826ea56f5cef26f1cc2ee7237df7ae07d9e@gbfmdypfbudmrc:f9d75356ba080c2b57cc297159e74826ea56f5cef26f1cc2ee7237df7ae07d9e@ec2-50-19-113-219.compute-1.amazonaws.com:5432/df4d0ti0rf7akb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "thisisyunik"
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


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
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return render_template('login.html', form=form)

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
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
