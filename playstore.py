#!/home/sziyan/bots/reddit/gplay/venv/bin python3

import logging
import re
import praw
import markdown
import html2text
import play_scraper as play
from config import Config

logging.basicConfig(level=logging.INFO, filename='output.log', filemode='a', format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.info("Bot started successfully")

reddit = praw.Reddit(client_id=Config.client_id, client_secret=Config.client_secret, username=Config.username, password=Config.password, user_agent=Config.user_agent)
subreddit = reddit.subreddit("+".join(Config.subreddit))
logging.info("Watching {} subreddit.".format((",").join(Config.subreddit)))
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
    if comments.author.name == Config.username:
        continue
    else:
        message = ""
        body = comments.body.lower()
        clean_text = get_clean_comment(body)
        link_me_requests = link_me_regex.findall(clean_text)
        app_count = get_no_apps(link_me_requests)
        app_list = get_all_app_requests(link_me_requests)
        count = 1
        if app_count > 0:
            logging.info("{} is searching for {} app(s): {}".format(comments.author.name, app_count, ",".join(app_list)))
            print("{} is searching for {} app(s): {}".format(comments.author.name, app_count, ",".join(app_list)))
            if app_count > Config.max_apps:
                msg = "You have searched for more then {} apps. I will only link to the first {} apps.\n\n".format(Config.max_apps, Config.max_apps)
                message +=msg
            for search in app_list:
                if count > Config.max_apps:
                    continue
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
                if app_count == 1:
                    developer = result.get('developer')
                    installs = result.get('installs')
                    description = result.get('description')
                    description = description.split(" ")
                    desc_output = " ".join(description[0:26]) + " ..."
                    msg = "**[{}]({})** by {} | {} | {} installs \n\n> {}".format(title,url,developer,price,installs,desc_output)
                else:
                    msg = "[{}]({}) - {} - [Search manually]({}) \n\n".format(title,url, price, search_manual)
                count+=1
                message+=msg
            if message != "":
                message+="\n\n\n\n --- \n\n\n\n \n\nI am a new bot. Please help me by private messaging me any bug reports you see. Thank You. \n\nBasic Google Play links bot by /u/lonerzboy"
                comments.reply(message)
                logging.info('{} completed app search successfully.'.format(comments.author.name))
                print('{} completed app search successfully.'.format(comments.author.name))
            else:
                logging.info("{} searched for an empty game.".format(comments.author.name))
                continue
        else:
            logging.info("{} searched for an empty game.".format(comments.author.name))
            continue


