#My application

from decouple import config
from flask import Flask, render_template, request, url_for, redirect
from .models import DB, User
from .twitter import add_or_update_user

#make our own app factory
def create_app():
    #create server
    app = Flask(__name__)
    #add config here later:
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    #stop tracking modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #add in database init later
    DB.init_app(app)

    # create the route
    @app.route('/')
    #define the function
    def root():
        users = User.query.all()
        return render_template('base.html', title = 'Home', users=users)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None):
        # if there is a name, the name = name
        # if not, then request username
        name = name or request.values['user_name']
        try:
            # checks for private account
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)



    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])

    return app
