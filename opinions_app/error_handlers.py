from flask import render_template

from . import app


@app.errorhandler(404)
def page_nor_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_nor_found(error):
    return render_template("500.html"), 500