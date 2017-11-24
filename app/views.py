from flask.templating import render_template

from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rand_element')
def rand_elem():
    # TODO implement this
    randed_values = {
        'fiche_hidden': 'Klebsiella',
        'fiche_main': 'K. pneumoniae subsp. pneumoniae',
        'selected': 'element'
    }
    return render_template('rand_element.html', randed_values=randed_values)


@app.route('/list_everything')
def list_everything():
    # TODO implement this
    return render_template('list_everything.html')


@app.route('/manage')
def manage():
    # TODO implement this
    return 'Not implemented yet'


