import os

from flask import Flask, render_template, flash, request
# from flask.ext.admin import Admin
# from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_wtf import Form
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email as EmailValidate


CWD = os.getcwd()
app = Flask('sprinkler', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{}/testing.db'.format(CWD)
db = SQLAlchemy(app)


# login_manager = LoginManager()
# login_manager.init_app(app)


class Email(db.Model):
    __tablename__ = "email"

    email = db.Column(db.String(120), primary_key=True)

    def __repr__(self):
        return self.email


db.create_all()


class EmailForm(Form):
    email = EmailField('email', validators=[DataRequired(), EmailValidate()])


# admin = Admin(app)
# admin.add_view(ModelView(Email, db.session))
limiter = Limiter(app, global_limits=["200 per day", "50 per hour"])


@app.route('/', methods=["GET", "POST"])
def index():
    form = EmailForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = Email(email=form.email.data)
            db.session.add(email)
            db.session.commit()
            flash('Sign up successful!')
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "KLDHSGKDHGSKDGHKSDGWEWGWE48289hf"
    app.run()
