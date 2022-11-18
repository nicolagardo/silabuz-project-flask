from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember_me = BooleanField("Recuérdame")
    submit = SubmitField("Ingresar")

class PostForm(FlaskForm):
    body = TextAreaField("¿En que estas pensando?", validators= [DataRequired()])
    submit = SubmitField('Postear')

