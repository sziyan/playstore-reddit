#!/home/sziyan/bots/reddit/gplay/venv/bin python3

import logging
import re
import praw
from praw import exceptions
import markdown
import play_scraper as play
from config import Config
import requests
from app.models import Games,Apps
from app import session
from datetime import datetime
from sqlalchemy import exc
from bs4 import BeautifulSoup

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
    now = datetime.now()

    month = now.strftime('%b %Y')

    try:
        if subreddit.lower() == 'androidgaming' or subreddit.lower() == 'gachagaming':
            month_games = session.query(Games).filter_by(month=month)
            check_db = month_games.filter_by(title = title).first()
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
        elif subreddit.lower() == 'androidapps':
            month_apps = session.query(Apps).filter_by(month=month)
            check_db = month_apps.filter_by(title=title).first()
            if check_db is None:
                app = Apps(title=title, link=link,rating=rating,price=price,category=category,count=1,developer=developer,iap_range=iap_range, month=month)
                session.add(app)
                session.commit()
                logging.info("New app {} added to database.".format(title))
                return 1
            else: #apps already exists
                check_db.count+=1
                session.commit()
                return 1
        else:
            logging.warning("Invalid subreddit. This should no happen unless testing!")
            return 0
    except exc.DBAPIError as dberror:
        logging.error('Database Error: {} : {}'.format(dberror.statement, dberror.params))
        logging.error('Database code error: {}'.format(dberror.code))
        pass



def sendtelegram(message):
    token = Config.token
    chat_id = Config.chat_id
    path = 'https://api.telegram.org/bot{}/sendmessage?chat_id={}&parse_mode=html&text={}'.format(token,chat_id,message)
    r = requests.get(path)

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
            app_count += 1
    return app_count

def get_all_app_requests(linkme_requests):
    apps_list = []
    for rq in linkme_requests:
        for item in rq.split(","):
            apps_list.append(item)
    return apps_list

def get_gplay_url(app_id):
    return 'https://play.google.com/store/apps/details?id={}'.format(app_id)

logging.basicConfig(level=logging.INFO, filename='output.log', filemode='a', format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %I:%M:%S %p')
logging.info("Bot started successfully")
sendtelegram('Bot started successfully!')

reddit = praw.Reddit(client_id=Config.client_id, client_secret=Config.client_secret, username=Config.username, password=Config.password, user_agent=Config.user_agent)
subreddit = reddit.subreddit("+".join(Config.subreddit))
logging.info("Watching /r/{} ...".format((",/r/").join(Config.subreddit)))
logging.info("Waiting for comments...")



try:
    for comments in subreddit.stream.comments(skip_existing=True):
        if comments.author.name == Config.username: #this is to prevent looping comment bot replies to comment
        #if comments.author.name == 'test':
            print("Same username as bot.")
            continue
        else:
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
                    search_manual = 'https://play.google.com/store/search?q={}'.format(search)
                    if count > Config.max_apps:
                        continue
                    result = play.search(search,page=1, detailed=True)
                    if not result:
                        logging.info("{} search for {} returned no result.".format(comments.author.name,search))
                        message+= 'I am unable to find {} - [Search manually]({}) \n\n'.format(search, search_manual)
                        continue
                    result = result[0]
                    title = result.get('title')
                    if result.get('score') is None:
                        score = "Early Access"
                    else:
                        score = result.get('score') + ' rating'
                    #url = result.get('url')
                    url = get_gplay_url(result.get('app_id'))
                    # search_manual = 'https://play.google.com/store/search?q={}'.format(search)
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
                        msg = "**[{}]({})** - {} - {} - [Search manually]({}) \n\n".format(title,url,score,price,search_manual)
                    result_list.append(result)
                    count+=1
                    message+=msg
                if message != "":
                    message+="\n\n\n\n --- \n\n\n\n \n\n|[Feedback]({})|PunyDev|Lonerzboy|".format('https://www.reddit.com/message/compose?to=PunyDev&subject=Feedback%20about%20bot&message=')
                    comments.reply(message)
                    #sendtelegram('<b>{}</b> searched for {} app(s) in <b>/r/{}</b> successfully.'.format(comments.author.name,app_count,comments.subreddit.display_name))
                    logging.info('{} completed app search successfully.'.format(comments.author.name))
                    print('{} completed app search successfully.'.format(comments.author.name))
                else:
                    logging.info("{} searched for an empty game.".format(comments.author.name))
                    continue
                for result in result_list:
                    update_db_result = update_db(comments.subreddit.display_name, result)
                    if update_db_result != 1:
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
except praw.exceptions.PRAWException as e:
    logging.error("PRAW Error: {}".format(e))
    pass
except Exception as e:
    logging.error("Error: {}".format(e))
    pass

