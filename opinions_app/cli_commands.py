import csv
import click

from .models import Opinion
from . import app, db


@app.cli.command("load_opinions")
def load_opinions_command():
    with open("opinions.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        counter = 0
        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            db.session.commit()
            counter += 1
        click.echo(f"Загружено мнений: {counter}")
