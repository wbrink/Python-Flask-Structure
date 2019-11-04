from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

# in flask_sqlalchmey the table name is the same as the class name converted to lower case and camel_case
# there is no need to explicitly define it as flask_sqlalchemy does this for you


class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(64), index=True, unique=True) 
    email = db.Column(db.String(120), index=True, unique=True) 
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self): 
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id")) # you use the User table (remember converted to lowercase) 
    
    def __repr__(self):
        return "Post {} from {}".format(self.body, self.author.username)


@login.user_loader
def load_user(id): 
    # part of flask-login 
    # Flask-Login keeps track of the logged in user by storing its unique identiﬁer in Flask’s user session, 
    # a storage space assigned to each user that connects to the application. 
    # Each time the a logged in user navigates to a new page, Flask-Login retrieves the ID of the user from the session, and then loads that user into memory. 
    # BecauseFlask-Loginknows nothing about databases,it needs the application’s help in loading a user. 
    # For that reason, the extension expects that the application will conﬁgure a user loader function, 
    # that can be called to load a user given the ID. This function can be added in the app/models.py module:
    return User.query.get(int(id))


"""
Flask_Sqlalchemy docs:
So what do backref and lazy mean? backref is a simple way to also declare a new property on the Post class. 
You can then also use my_post.person to get to the person at that address. lazy defines when SQLAlchemy will load the data from the database:
"""