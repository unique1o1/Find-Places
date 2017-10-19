from flask import Flask, render_template, request
import forms
from models import db, User
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0@localhost:5432/learningflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'testingforsimething'
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/abouts")
def about():
    return render_template("about.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = forms.SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template("signup.html", form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data,
                           form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            return "sucess"
    elif request.method == 'GET':
        return render_template("signup.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
