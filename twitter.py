import os
import tweepy
import configparser
import datetime


class Twitter():

    def __init__(self, path):
        try:    # authentication
            config = configparser.ConfigParser()
            config.read(path)
            auth = tweepy.OAuthHandler(config.get("auth", "consumer_key"), config.get("auth", "consumer_secret"))
            auth.set_access_token(config.get("auth", "access_token"), config.get("auth", "access_secret"))
            # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            # auth.set_access_token(access_token, access_secret)

            self.api = tweepy.API(auth, wait_on_rate_limit=True)

        except tweepy.error.TweepError:
            print("Authentication failed")

    def get_tweets(self, username):
        # Retrieve 20 most recent tweets
        try:
            tweets = self.api.user_timeline(screen_name=username, count=20, include_rts=1, exclude_replies=True)
            today_tweets = []
            for tweet in tweets:
                # Checks if tweet was from the last day
                if (datetime.datetime.now() - tweet.created_at).days < 1:
                    today_tweets.append(tweet)
            return today_tweets

        except tweepy.error.TweepError as error:
            print("Error: ", end='')
            print(error)
            return -1
