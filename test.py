import play_scraper as play
import praw
from config import Config

result =play.search('the quest',detailed=False,page=1)[0]
print(result['title'])

