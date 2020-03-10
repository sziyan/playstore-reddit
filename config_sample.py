import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    client_id =  'reddit client id '#reddit client id
    client_secret =  'reddit client secret' #reddit client secret
    username = 'reddit username'
    password = 'reddit password'
    user_agent = 'user_agent'
    subreddit = ['google_play'] #subreddit to monitor
    max_apps = 15 #max number of apps to list in 1 single comment
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'mydb.db') #sqlalchemy URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    token = 'token' #telegram bot token
    chat_id = 'chat_id' #telegram chat id
    max_monthly = 5
    monthly_subreddit = 'testing'