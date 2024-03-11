from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField('Quel est votre nom ?', validators=[DataRequired()])
    submit = SubmitField('Envoyer')
