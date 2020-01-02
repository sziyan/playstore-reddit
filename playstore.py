#!/home/sziyan/bots/reddit/gplay/venv/bin python3

import praw
import time
import play_scraper as play
from config import Config

reddit = praw.Reddit(client_id=Config.client_id, client_secret=Config.client_secret, username=Config.username, password=Config.password, user_agent=Config.user_agent)

subreddit = reddit.subreddit(Config.subreddit)
start_time = time.time()

for comments in subreddit.stream.comments():
    if comments.created_utc < start_time or comments.author == 'GooglePlay_Links':
        continue
    else:
        body = comments.body
        if 'linkme:' in body:
            message = ""
            tosplit = body.split('linkme:')
            after_linkme = tosplit[1]
            search_terms = after_linkme.split('.')[0]
            for search in search_terms.split(','):
                result = play.search(search,page=1, detailed=True)
                if not result:
                    continue
                result = result[0]
                title = result.get('title')
                score = result.get('score')
                url = result.get('url')
                search_manual = 'https://play.google.com/store/search?q={}'.format(search)
                if result.get('free') is True:
                    price = 'Free'
                else:
                    price = result.get('price')
                if result.get('iap') is True:
                    price+= ' with IAP'
                if len(search_terms.split(',')) == 1:
                    developer = result.get('developer')
                    installs = result.get('installs')
                    description = result.get('description')
                    description = description.split(" ")
                    desc_output = " ".join(description[0:26]) + " ..."
                    msg = "**[{}]({})** by {} | {} | {} installs \n\n> {}".format(title,url,developer,price,installs,desc_output)
                else:
                    msg = "[{}]({}) - {} - [Search manually]({}) \n\n".format(title,url, price, search_manual)
                message+=msg
            if message != "":
                message+="\n\n\n\n---\n\n\n\nBasic Google Play links bot by /u/lonerzboy"
                comments.reply(message)
                print("{} searched for app successfully.".format(comments.author.name))
            else:
                continue
        else:
            continue
