import click
from flask.cli import with_appcontext

from src.ext import db
from src.models.book import Book


@click.command('init_db')
@with_appcontext
def init_db():
    click.echo('initializing...')

    db.drop_all()
    db.create_all()

    click.echo('Done!')


@click.command('populate_db')
@with_appcontext
def populate_db():

    books = []
    

    for book in books:
        book.create()

    click.echo("Done!")