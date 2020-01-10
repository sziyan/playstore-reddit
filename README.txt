## Google Play Links Bot for Reddit

This reddit bot monitors the configured subreddit(s) for any comments with `linkme` in the content.
Any contents after `linkme` will be queried with Play Store for useful information.

Supports sending of searches to configured Telegram user.

# Database support

This bot has a built in feature of adding new games that was queried with `linkme` and add it to a database.
With the database, users are able to provide useful information such as top 5 games/apps that was queried for the month.
Right now, database seperates AndroidGaming and AndroidApps into 2 different tables.


Check `post_monthly.py` for 1 such uses.

# Configuration

To get the bot up and running, make sure to create a `config.py` and place it in the same path as `playstore.py`:

```python

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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'mydb.db') #sqlalchemy URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    token = 'token' #telegram bot token
    chat_id = 'chat_id' #telegram chat id
    max_monthly = 5

```
Check `config_sample.py` for reference.