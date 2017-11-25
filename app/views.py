import random

from flask.templating import render_template
from flask import request, redirect, url_for
from sqlalchemy.orm import joinedload

from app import app
from app.models import Category, Element
from app.functions import db_create, db_migrate, import_csv_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rand_element')
def rand_elem():
    what_to_rand = request.args.get('what', None)
    if not what_to_rand or (what_to_rand != 'category' and what_to_rand != 'element'):
        return redirect(url_for('index'))

    fiche_main = None
    fiche_hidden = []

    if what_to_rand == 'category':
        categories = Category.query.options(joinedload('elements')).all()
        fiche_main = categories[random.randint(0, len(categories) - 1)]
        fiche_hidden = fiche_main.elements

    if what_to_rand == 'element':
        elements = Element.query.all()
        fiche_main = elements[random.randint(0, len(elements) - 1)]
        fiche_hidden = fiche_main.category

    randed_values = {
        'fiche_hidden': fiche_hidden,
        'fiche_main': fiche_main,
        'selected': what_to_rand
    }
    return render_template('rand_element.html', randed_values=randed_values)


@app.route('/list_everything')
def list_everything():
    # TODO implement this
    return render_template('list_everything.html')


@app.route('/manage')
def manage():
    command = request.args.get('command', None)
    if command == 'db_create':
        db_create()
    if command == 'db_migrate':
        db_migrate()
    if command == 'init_db':
        import_csv_data('example_data/import_data.csv')
    return 'Runned command {}'.format(command)


