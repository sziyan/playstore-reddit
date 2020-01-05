# import play_scraper as play
# import praw
# from config import Config
#
# reddit = praw.Reddit(client_id=Config.client_id, client_secret=Config.client_secret, username=Config.username, password=Config.password, user_agent=Config.user_agent)
# subreddit = reddit.subreddit('sziyan_testing')
#
# for comments in subreddit.comments(limit=100):
#     print(comments.author.name)
#     comments.delete()
#
# print("deleted")
#
# for comments in subreddit.comments():
#     print(comments.author)

#!/home/sziyan/bots/reddit/gplay/venv/bin python3

import logging
import re
import praw
from praw import exceptions
import markdown
import html2text
import play_scraper as play
from config import Config

logging.basicConfig(level=logging.INFO, filename='output.log', filemode='a', format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %I:%M:%S %p')
logging.info("Bot started successfully")

reddit = praw.Reddit(client_id=Config.client_id, client_secret=Config.client_secret, username=Config.username, password=Config.password, user_agent=Config.user_agent)
subreddit = reddit.subreddit("+".join(Config.subreddit))
logging.info("Watching /r/{} ...".format((",/r/").join(Config.subreddit)))
logging.info("Waiting for comments...")


link_me_regex = re.compile("\\blink[\s]*me[\s]*:[\s]*(.*?)(?:\.|;|$)", re.M | re.I)

def get_clean_comment(text):
    text_maker = html2text.HTML2Text()
    text_maker.ignore_emphasis = True
    text_maker.IGNORE_ANCHORS = True
    text_maker.IGNORE_IMAGES = True
    htmltext = markdown.markdown(text)
    output = text_maker.handle(htmltext)
    return output

def get_no_apps(linkme_requests):
    app_count = 0
    for rq in linkme_requests:
        for item in rq.split(','):
            app_count += 1
    return app_count

def get_all_app_requests(linkme_requests):
    apps_list = []
    for rq in linkme_requests:
        for item in rq.split(","):
            apps_list.append(item)
    return apps_list

for comments in subreddit.stream.comments(skip_existing=True):
    print(comments)



