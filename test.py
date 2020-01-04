import play_scraper as play
import praw
from config import Config

reddit = praw.Reddit(client_id=Config.client_id, client_secret=Config.client_secret, username=Config.username, password=Config.password, user_agent=Config.user_agent)
subreddit = reddit.subreddit('sziyan_testing')

for comments in subreddit.comments(limit=100):
    print(comments.author.name)
    comments.delete()

print("deleted")

for comments in subreddit.comments():
    print(comments.author)
