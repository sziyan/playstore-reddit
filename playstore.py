#!/home/sziyan/bots/reddit/gplay/venv/bin python3

import logging
import re
import praw
from praw import exceptions
import markdown
import html2text
import play_scraper as play
from config import Config
import requests
from app.models import Games,Apps
from app import session
import datetime

logging.basicConfig(level=logging.INFO, filename='output.log', filemode='a', format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %I:%M:%S %p')
logging.info("Bot started successfully")

reddit = praw.Reddit(client_id=Config.client_id, client_secret=Config.client_secret, username=Config.username, password=Config.password, user_agent=Config.user_agent)
subreddit = reddit.subreddit("+".join(Config.subreddit))
logging.info("Watching /r/{} ...".format((",/r/").join(Config.subreddit)))
logging.info("Waiting for comments...")


def update_db(subreddit, result):
    title = result['title']
    link = result['url']
    rating = result['score']
    if result['free']is True:
        price = 'Free'
    else:
        price = result['price']
    if result['iap'] is True:
        price += ' with IAP'
    category_list_types = result['category']
    category_list = []
    for i in category_list_types:
        if '_' in i:
            in_list = i.split('_')
            category_list.append(in_list[1].capitalize())
        else:
            category_list.append(i.capitalize())
    category = ", ".join(category_list)
    developer = result['developer']
    if result['iap_range'] is None:
        iap_range = 'NA'
    else:
        iap_range = " - ".join(result['iap_range'])
    now = datetime.datetime.now()
    month = now.strftime('%b %y')

    if subreddit == 'AndroidGaming' or subreddit == 'sziyan_testing':
        check_db = session.query(Games).filter_by(title = title).first()
        if check_db is None: #game does not exist
            game = Games(title=title, link=link,rating=rating,price=price,category=category,count=1,developer=developer,iap_range=iap_range, month=month)
            session.add(game)
            session.commit()
            logging.info('New game {} added to database.'.format(title))
            return 1
        else: #game already exist
            check_db.count += 1
            session.commit()
            return 1
    elif subreddit == 'AndroidApps':
        check_db = session.query(Apps).filter_by(title=title).first()
        if check_db is None:
            app = Apps(title=title, link=link,rating=rating,price=price,category=category,count=1,developer=developer,iap_range=iap_range, month=month)
            session.add(app)
            session.commit()
            logging.info("New app {} added to database.".format(title))
            return 1
        else:
            check_db.count+=1
            session.commit()
            return 1
    else:
        logging.warning("Invalid subreddit. This should no happen unless testing!")
        return 0

def sendtelegram(message):
    token = Config.token
    chat_id = Config.chat_id
    path = 'https://api.telegram.org/bot{}/sendmessage?chat_id={}&parse_mode=html&text={}'.format(token,chat_id,message)
    r = requests.get(path)

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
    #if comments.author.name == Config.username:
    if comments.author.name == 'test':
        print("Same username as bot.")
        continue
    else:
        try:
            message = ""
            body = comments.body.lower()
            clean_text = get_clean_comment(body)
            link_me_requests = link_me_regex.findall(clean_text)
            app_count = get_no_apps(link_me_requests)
            app_list = get_all_app_requests(link_me_requests)
            count = 1
            result_list = []
            if app_count > 0:
                logging.info("{} is searching for {} app(s) in /r/{}: {}".format(comments.author.name, app_count,comments.subreddit.display_name, ",".join(app_list)))
                print("{} is searching for {} app(s): {}".format(comments.author.name, app_count, ",".join(app_list)))
                if app_count > Config.max_apps:
                    msg = "You have searched for more than {} apps. I will only link to the first {} apps.\n\n".format(Config.max_apps, Config.max_apps)
                    message +=msg
                for search in app_list:
                    if count > Config.max_apps:
                        continue
                    result = play.search(search,page=1, detailed=True)
                    if not result:
                        logging.info("{} search for {} returned no result.".format(comments.author.name,search))
                        continue
                    result = result[0]
                    title = result.get('title')
                    if result.get('score') is None:
                        score = "No rating"
                    else:
                        score = result.get('score') + ' rating'
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
                        desc_output = " ".join(description[0:35]) + " ..."
                        msg = "**[{}]({})** | {}  | {} | {} downloads | [Search manually]({}) \n\n> {}".format(title,url,score,price,installs,search_manual,desc_output)
                    else:
                        msg = "[{}]({}) - {} - {} - [Search manually]({}) \n\n".format(title,url,score,price,search_manual)
                    result_list.append(result)
                    count+=1
                    message+=msg
                if message != "":
                    message+="\n\n\n\n --- \n\n\n\n \n\nI am a new bot. Please help me by private messaging me any bugs you see. Thank You."
                    comments.reply(message)
                    sendtelegram('<b>{}</b> searched for {} app(s) in <b>/r/{}</b> successfully.'.format(comments.author.name,app_count,comments.subreddit.display_name))
                    logging.info('{} completed app search successfully.'.format(comments.author.name))
                    print('{} completed app search successfully.'.format(comments.author.name))
                else:
                    logging.info("{} searched for an empty game.".format(comments.author.name))
                    continue
                for result in result_list:
                    update_db_result = update_db(comments.subreddit.display_name, result)
                    if update_db_result is not 1:
                        logging.warning('Updating of database failed.')
            else:
                continue
        except praw.exceptions.APIException as api_exception:
            logging.error(
                "API Error: {} - {} - {}".format(api_exception.error_type, api_exception.field, api_exception.message))
            print(
                "API Error: {} - {} - {}".format(api_exception.error_type, api_exception.field, api_exception.message))
            pass
        except praw.exceptions.ClientException:
            logging.error("Client Error: Client exception")
            pass



