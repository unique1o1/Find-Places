from flask import Flask, render_template, request
import forms
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'

app.secret_key = 'testingforsimething'


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
        return "sucess"
    elif request.method == 'GET':
        return render_template("signup.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
