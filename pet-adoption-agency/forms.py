from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from re import *

from flask_wtf.file import * 

def validate_name(form, field):
    if len(field.data) > 50:
        raise ValidationError('Name must be less than 50 characters')

class AddPetForm(FlaskForm):
    '''form for adding a pet'''

    name = StringField('Pet Name', validators=[InputRequired()])
    species = StringField('Pet Species', validators=[InputRequired(),AnyOf(['cat','dog','porcupine'])])
    age = IntegerField('Age', validators=[InputRequired(),NumberRange(0,30)])
    notes = StringField('Notes',validators=[Optional()])
    file = FileField('Photo', validators=[FileAllowed(['txt', 'jpg', 'jpeg', 'png'], 'Images only!')])

    
class EditPetForm(FlaskForm):
    '''edit pet form'''

    name = StringField('Pet Name', validators=[InputRequired()])
    species = StringField('Pet Species', validators=[InputRequired(),AnyOf(['cat','dog','porcupine'])])
    age = IntegerField('Age', validators=[InputRequired(),NumberRange(0,30)])
    notes = StringField('Notes',validators=[Optional()])
    file = FileField('Photo', validators=[FileAllowed(['txt', 'jpg', 'jpeg', 'png'], 'Images only!')])
