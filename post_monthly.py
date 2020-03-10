import logging
import praw
from config import Config
from app.models import Games
from app import session
import datetime
import requests

logging.basicConfig(level=logging.INFO, filename='monthly.log', filemode='a', format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %I:%M:%S %p')
current_month = datetime.datetime.now()
month = current_month.strftime('%b %Y')
month_game = session.query(Games).filter_by(month=month)
more1games = month_game.filter(Games.count > 1)
games = more1games.order_by(Games.count.desc())

number_of_games = more1games.count()
#number_of_games = month_game.count()
msg = ""
top_games = []
other_games = []
reddit = praw.Reddit(client_id=Config.client_id, client_secret=Config.client_secret, username=Config.username, password=Config.password, user_agent=Config.user_agent)
subreddit = reddit.subreddit(Config.monthly_subreddit)


def sendtelegram(message):
    token = Config.token
    chat_id = Config.chat_id
    path = 'https://api.telegram.org/bot{}/sendmessage?chat_id={}&parse_mode=html&text={}'.format(token, chat_id,
                                                                                                  message)
    r = requests.get(path)

if number_of_games > Config.max_monthly: # if number of games more than configure max
    for i in range(0,Config.max_monthly):
        top_games.append(games[i])
else:
    for i in range(0,number_of_games): # if number of games less than configure max
        top_games.append(games[i])

##introduction message
msg += 'Hello /r/AndroidGaming! \n\n' \
       'This is a list of top {} games that was found using linkme. \n\n' \
       'Any feedbacks are greatly appreciated! \n\n'.format(Config.max_monthly)

##table header
msg += '\n\n'
msg += '| Count | Title | URL | Ratings | Price | Category | Developer | IAP |\n'
msg += '| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |\n' # seperate header and body

## Generate top games
for i in top_games:
    if i.rating is None:
        i.rating = 'Early Access'
    msg += '| {} | {} | [Google Play]({}) | {} | {} | {} | {} | {} |\n'.format(i.count, i.title, i.link, i.rating, i.price, i.category, i.developer, i.iap_range)

## Generate rest of the games
for i in range(Config.max_monthly, number_of_games):
    print(games[i].id, games[i].title, games[i].count)
    other_games.append(games[i])

if other_games:
    msg += '\n\nOther games that were searched this month(with searches more than 1) \n\n'

    for game in other_games:
        if game.rating is None:
            game.rating = 'Early Access'
        msg += '[{}]({}) - {} - {} searches \n\n'.format(game.title, game.link, game.rating, game.count)


msg += '\n\nThis post is automated at the end of every month. \n\n ' \
       'Any feedback is greatly appreciated.'

submission = subreddit.submit(title='Top {} linkme games for {}!'.format(Config.max_monthly, month), send_replies=False, selftext=msg)
log_message = '{}  top games posted: {}'.format(month, submission.url)
logging.info(log_message)
sendtelegram(log_message)

