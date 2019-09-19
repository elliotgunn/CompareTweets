import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
config('TWITTER_CONSUMER_SECRET'))

TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
config('TWITTER_ACCESS_TOKEN_SECRET'))

TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

def add_or_update_user(username):
    """add or update a user and their tweets, error if no/private user"""
    try:
        twitter_user = TWITTER.get_user(username)  # Fetch twitter user handle
        # Create SQLAlchemy User db instance
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        # then add user to database
        DB.session.add(db_user)

        # we want as many recent non-RT/reply statuses as we can get
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_user.newest_tweet_id)

        # return the most recent tweet id IF there was a new or recent tweet
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # for loop: just retrieved tweets
        for tweet in tweets:
            # get embedding for tweet, and store in db
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')
            # get tweet
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500],
                            embedding=embedding)
            # add tweet to user
            db_user.tweets.append(db_tweet)
            # finally, add tweet to database
            DB.session.add(db_tweet)

    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()
