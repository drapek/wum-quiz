#!flask/bin/
import imp
import os.path
from migrate.versioning import api
import csv

from sqlalchemy.exc import InvalidRequestError

from app.config import SQLALCHEMY_DATABASE_URI
from app.config import SQLALCHEMY_MIGRATE_REPO
from app import db
from app.models import CategoryType, get_or_create, Category, ElementType, Element, get, create


def db_create():
    db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))


def db_migrate():
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v + 1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    exec(old_model, tmp_module.__dict__)
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta,
                                              db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('New migration saved as ' + migration)
    print('Current database version: ' + str(v))


def import_csv_data(file):
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for i, row in enumerate(reader):
            if row[0] == 'category_type':
                continue  # Omit the header row
            if not row[1]:
                continue  # This column is required - for empty values omit the row
            try:
                category_type = category = element = elem_types = None

                if row[0]:
                    category_type = get_or_create(db.session, CategoryType, name=row[0].strip())

                if row[1]:
                    category = get_or_create(db.session, Category, name=row[1].strip(), category_type=category_type)

                if row[2]:
                    elem_types = []
                    for elemtype in row[2].split(','):
                        elem_types.append(get_or_create(db.session, ElementType, name=elemtype.strip()))

                if row[3]:
                    kwargs = {'name': row[3].strip(), 'category': category}
                    if elem_types:
                        element = get(db.session, Element, **kwargs)
                        if not element:
                            kwargs['element_type'] = elem_types
                            element = create(db.session, Element, **kwargs)
                    else:
                        element = get_or_create(db.session, Element, **kwargs)

                print(i, category_type, category, elem_types, element)
            except InvalidRequestError as e:
                db.session.rollback()
                raise e







