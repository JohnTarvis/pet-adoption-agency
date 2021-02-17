from typing import AsyncGenerator
from flask import *
from flask_debugtoolbar import *
from models import *

from forms import *

from werkzeug.utils import *

import os

from config import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///postgres"#flask_wtforms"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

toolbar = DebugToolbarExtension(app)
app.debug = True

db.app=(app)
db.init_app(app)
db.create_all()

connect_db(app)

@app.route('/')
def home_page():
    pets = Pet.query.all()
    return render_template('pets/index.html',pets=pets)

@app.route('/pets/<int:pet_id>/delete', methods=['GET','POST'])
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    return redirect('/')


@app.route('/pets/<int:pet_id>/edit', methods=['GET','POST'])
def edit_pet(pet_id):
    form = EditPetForm()
    pet = Pet.query.get_or_404(pet_id)
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.age = form.age.data
        pet.notes = form.notes.data
        f = form.file.data
        if f:
            filename = secure_filename(f.filename)
            f.save('static/images/' + filename)
            pet.photo_name = filename
        else :
            filename = pet.photo_name
        db.session.add(pet)
        db.session.commit()
        flash(f'Edited Pet: {pet.name}')   
        return redirect('/')
    else:
        form.name.data = pet.name
        form.species.data = pet.species
        form.age.data = pet.age
        form.notes.data = pet.notes
        return render_template('/pets/add_pet_form.html',form=form,pet=pet)

@app.route('/pets/add', methods=['GET','POST'])
def show_pet_form():
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        age = form.age.data
        notes = form.notes.data
        f = form.file.data
        if f:
            filename = secure_filename(f.filename)
            f.save('static/images/' + filename)
        else :
            filename = 'image_unavailable.png'
        pet = Pet(name=name,species=species,age=age,notes=notes,photo_name=filename)
        db.session.add(pet)
        db.session.commit()
        flash(f'Added Pet: {name}')   
        return redirect('/')
    else:
        return render_template('/pets/add_pet_form.html',form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def big_print(message):
    print(f"""
    ===========================================================
                            {message}
    ===========================================================
        """)