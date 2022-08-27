from flask import render_template

from . import app, db


@app.errorhandler(404)
def oage_nor_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def oage_nor_found(error):
    return render_template("500.html"), 500