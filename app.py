import requests
from api import utils as util
from api import GooglePlay
from bs4 import BeautifulSoup
import praw
from config import Config
import re
import markdown
import logging

logging.basicConfig(level=logging.INFO, filename='output.log', filemode='a', format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %I:%M:%S %p')
logging.info("Bot started successfully")
print('Bot started successfully')

reddit = praw.Reddit(
    client_id=Config.client_id,
    client_secret=Config.client_secret,
    password=Config.password,
    user_agent="GooglePlayLinks_Bot by u/PunyDev",
    username=Config.username,
)

link_me_regex = re.compile("\\blink[\s]*me[\s]*:[\s]*(.*?)(?:\.|;|$)", re.M | re.I)

def get_clean_comment(text):
    htmltext = markdown.markdown(text)
    soup = BeautifulSoup(htmltext, features="lxml")
    output = soup.get_text()
    return output

def get_no_apps(linkme_requests):
    app_count = 0
    for rq in linkme_requests:
        for item in rq.split(','):
            if item != '': #if not empty
                app_count += 1
    return app_count

def get_all_app_requests(linkme_requests):
    apps_list = []
    for rq in linkme_requests:
        for item in rq.split(","):
            if item != '': #if not empty
                apps_list.append(item)
    return apps_list

link_me_regex = re.compile("\\blink[\s]*me[\s]*:[\s]*(.*?)(?:\.|;|$)", re.M | re.I)

subreddit = reddit.subreddit(("+").join(Config.subreddit))

try:
    for comments in subreddit.stream.comments(skip_existing=True):
        if comments.author.name == Config.username:
            continue
        else:
            message = "" # creating blank message
            body = comments.body.lower()
            clean_text = get_clean_comment(body)
            link_me_requests = link_me_regex.findall(clean_text)
            app_count = get_no_apps(link_me_requests) #number of apps in the linkme request
            app_list = get_all_app_requests(link_me_requests) #list of apps in the linkme request
            count = 1 #number of apps to search
            if app_count > 0:
                logging.info("{} is searching for {} app(s) in /r/{}: {}".format(comments.author.name, app_count,comments.subreddit.display_name, ",".join(app_list)))
                print("{} is searching for {} app(s): {}".format(comments.author.name, app_count, ",".join(app_list)))
            else: #no app being searched
                continue
            if app_count > Config.max_apps:
                msg = "You have searched for {} apps. I will only link to the first {} apps.\n\n".format(app_count, Config.max_apps)
                message +=msg
                count = Config.max_apps #if exceed max number of apps, will only count 15
            else:
                count = app_count
            for i in range(0, count):
                app_search = app_list[i]
                url = util.get_app_link(app_search) #obtain store url
                if url is not None:
                    app = GooglePlay.App(url)
                    if app.get_rating is not None:  #obtain app rating
                        rating = app.get_rating
                    else:
                        rating = 'NA'
                    price = app.get_price
                    installs = app.get_installs
                    if app.get_iap is True: #contains IAP, change the output of price
                        price = '{} with IAP'.format(str(price))
                    size = app.get_size
                    if app.get_playpass is True:
                        play_pass = '▶️'
                    else:
                        play_pass = ''
                    if app.get_family is True:
                        family = '🏠'
                    else:
                        family = ''
                    if count == 1:
                        desc = app.get_desc
                        desc = desc.split(" ")
                        desc = " ".join(desc[0:35]).replace("\n"," ") + " ..."
                        msg = "**[{}]({})** | {} ⭐️ | {} | {} | {} | {} {} \n\n> {}".format(app.get_name,url,rating,price,installs, size, play_pass,family, desc)
                    else:
                        msg = "**[{}]({})** - {} ⭐️ - {} - {} - {} {} {}\n\n".format(app.get_name,url,rating,price, installs, size, play_pass, family)
                    message+=msg
            if message != "":
                message+="\n\n --- \n\n**Legend:** \n\n ▶️: Available in Play Pass \n\n 🏠: Eligble for Family Library \n\n |[Feedback]({})|PunyDev|".format('https://www.reddit.com/message/compose?to=PunyDev&subject=Feedback%20about%20AppStore%20bot&message=')
                comments.reply(message)
                logging.info('{} completed app search successfully.'.format(comments.author.name))
                print('{} completed app search successfully.'.format(comments.author.name))
            else:
                logging.info("{} searched for an empty game.".format(comments.author.name))
except praw.exceptions.APIException as api_exception:
    logging.error(
        "API Error: {} - {} - {}".format(api_exception.error_type, api_exception.field, api_exception.message))
    print(
        "API Error: {} - {} - {}".format(api_exception.error_type, api_exception.field, api_exception.message))
    pass
except praw.exceptions.ClientException:
    logging.error("Client Error: Client exception")
    pass
except praw.exceptions.PRAWException as e:
    logging.error("PRAW Error: {}".format(e))
    pass
except Exception as e:
    logging.error("Error: {}".format(e))
    pass