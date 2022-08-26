from datetime import datetime
from random import randrange

from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "MY_SECRET_KEY"
db = SQLAlchemy(app)

class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class OpinionForm(FlaskForm):
    title = StringField(
        "Введите название фильма",
        validators=(
            DataRequired(message="Обязательное поле"),
            Length(1, 128)
        )
    )
    text = TextAreaField(
        "Напишите мнение",
        validators=(DataRequired(message="Обязательное поле"),)
    )
    source = URLField(
        "Добавьте ссылку на подробный обзор фильма",
        validators=(
            Length(1, 256),
            Optional()
        )
    )
    submit = SubmitField("Добавить")


@app.route('/')
def index_view():
    quantity: int = Opinion.query.count()
    if not quantity:
        return 'Совсем скоро тут будет случайное мнение о фильме!'
    ofsset_value = randrange(quantity)
    opinion = Opinion.query.offset(ofsset_value).first()
    context = {
        "opinion": opinion,

    }
    return render_template("opinion.html", **context)


@app.route('/add/', methods=("GET", "POST"))
def add_opinion_view():
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first():
            flash('Такое мнение уже было оставлено ранее!', 'same-text')
            return render_template("add_opinion.html", form=form)
        opinion=Opinion(
            title=form.title.data,
            text=text,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for("share_link", id=opinion.id))
    context ={
        "add": "Заглушка",
        "form": form
    }
    return render_template("add_opinion.html", **context)



@app.route('/opinion/<int:id>/')
def share_link(id):
    film_id = Opinion.query.get_or_404(id)
    context = {
        "opinion": film_id
    }
    return render_template("opinion.html", **context)


if __name__ == '__main__':
    app.run()