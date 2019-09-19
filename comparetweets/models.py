from flask_sqlalchemy import SQLAlchemy

# Import database
DB = SQLAlchemy()

class User(DB.Model):
    # Twitter users that we analyze
    id = DB.Column(DB.BigInteger, primary_key = True)
    name = DB.Column(DB.String(15), nullable = False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '<User {}'.format(self.name)

class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key = True)
    text = DB.Column(DB.Unicode(500))
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet {}'.format(self.text)
