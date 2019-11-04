from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Name", validators=[DataRequired(), Length(min=2, max=15)] )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=10)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")