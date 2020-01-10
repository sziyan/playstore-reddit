import praw
from config import Config

reddit = praw.Reddit(client_id=Config.client_id, client_secret=Config.client_secret, username=Config.username, password=Config.password, user_agent=Config.user_agent)
subreddit = reddit.subreddit('sziyan_testing')

for comments in subreddit.comments():
    comments.delete()
    print('Deleted {} comments'.format(comments.author))