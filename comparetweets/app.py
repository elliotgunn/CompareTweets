#My application

from decouple import config
from flask import Flask, render_template
from .models import DB, User

#make our own app factory
def create_app():
    #create server
    app = Flask(__name__)

    #add config here later:
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')

    #stop tracking modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['ENV'] = config('ENV')

    #add in database init later
    DB.init_app(app)

    #create the route
    @app.route('/')

    #define the function
    def root():
        users = User.query.all()
        return render_template('base.html', title = 'Home', users=users)

    return app
