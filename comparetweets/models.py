from flask_sqlalchemy import SQLAlchemy

# Import database
DB = SQLAlchemy()

class User(DB.Model):
    # Twitter users that we analyze
    id = DB.Column(DB.Integer, primary_key = True)
    name = DB.Column(DB.String(15), nullable = False)

class Tweet(DB.Model):
    id = DB.Column(DB.Integer, primary_key = True)
    text = DB.Column(DB.Unicode(280))
