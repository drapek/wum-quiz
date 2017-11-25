from app import db


association_table = db.Table('element__element_type__association', db.Model.metadata,
    db.Column('element_id', db.Integer, db.ForeignKey('element.id')),
    db.Column('element_type_id', db.Integer, db.ForeignKey('element_type.id'))
)


class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('elements', lazy=True))
    element_type = db.relationship('ElementType', secondary=association_table)

    def __repr__(self):
        return '<Element %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    category_type_id = db.Column(db.Integer, db.ForeignKey('category_type.id'))
    category_type = db.relationship('CategoryType', backref=db.backref('categories', lazy=True))

    def __repr__(self):
        return '<Category %r>' % self.name


class CategoryType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))

    def __repr__(self):
        return '<CategoryType %r>' % self.name


class ElementType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))

    def __repr__(self):
        return '<ElementType %r>' % self.name


def get_or_create(session, model, **kwargs):
    instance = get(session, model, **kwargs)
    if instance:
        return instance
    else:
        return create(session, model, **kwargs)


def get(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance


def create(session, model, **kwargs):
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance
