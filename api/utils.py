import urllib.parse
from bs4 import BeautifulSoup
import requests
import jellyfish

def similar(a,b):
    return jellyfish.levenshtein_distance(a,b)


def get_app_link(search):
    search = search.lstrip().rstrip()
    url = 'https://play.google.com/store/search?q={}&c=apps'.format(urllib.parse.quote(search))
    index = 0
    search = search.lower()
    predicted_app = ''
    similarity_index = 99 #set to an arbituary high value so that prediction will start
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    app = soup.find_all('div', class_='WsMG1c nnK0zc') #obtain all app title on the page
    for i in range(0,3): #only list the first 3 apps
        app_name = app[i].contents[0]
        if search == app_name.lower() or search in app_name.lower():
            index = i
            break
        else:
            similarity = similar(app_name.lower(), search)
            if similarity < similarity_index:
                similarity_index = similarity
                index = i
                predicted_app = app_name
    if app_name.lower() != search and search not in app_name.lower():
        app_name = predicted_app
    url_div = soup.find_all('div', class_='b8cIId f5NCO')[index].contents[0]
    url = 'https://play.google.com' + url_div.get('href')
    return url



