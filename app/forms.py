from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User # used for validating fields

class LoginForm(FlaskForm):
    username = StringField("Name", validators=[DataRequired(), Length(min=2, max=15)] )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=10)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    """I have also added two methods to this class called validate_username() andvalidate_email(). 
        When you add any methods that match the pattern validate_<field_name>, 
        WTForms takes those as custom validators and invokes them in addition to the stock validators. 
        In this case I want to make sure that the username and email address entered by
        the user are not already in the database,so these two methods issue database queries 
        expecting there will be no results. In the event a result exists, a validation 
        error is triggered by raising ValidationError. The message included as the argument 
        in the exception will be the message that will be displayed next to the 
        ﬁeld for the user to see. """ 

    #custom validator wtform docs
    #class MyForm(Form):
    #    name = StringField('Name', [InputRequired()])
#
 #       def validate_name(form, field):
  #          if len(field.data) > 50:
   #             raise ValidationError('Name must be less than 50 characters')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username")


    # comments on privacy
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address")
            # to hide who is registered on the website, another option is not showing an error message
            # and inform the user that they have to confirm the email belongs to them, send an email to
            # the owner of the eamil and inform them that you tried to re-register if you forgot username
            # here it is, if forgot password go to password reset page
            # if you did not try to register with us ignore the email.
            # if the email is not registered, in the backend create a random one time use token in a url 
            # and send to the new e-mail and ask them to confirm the new account 

