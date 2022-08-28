from random import randrange

from flask import render_template, url_for

from . import app, db
from .models import Opinion
from .forms import OpinionForm


def get_random_opinion():
    quantity: int = Opinion.query.count()
    if quantity:
        ofsset_value = randrange(quantity)
        opinion = Opinion.query.offset(ofsset_value).first()
        return opinion

@app.route('/')
def index_view():
    opinion = get_random_opinion()
    if not opinion:
        abort(404)
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