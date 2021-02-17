from flask_sqlalchemy import *

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Pet(db.Model):
    '''Pet'''

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)

    photo_name = db.Column(db.Text)    

    age = db.Column(db.Text)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True, nullable=False)



