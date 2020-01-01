import praw
import time
import play_scraper as play

reddit = praw.Reddit(client_id='kn_3nXzENsvUjQ', client_secret='1CLsrd4FIdoUEC0ga0tU4vuP-CM', username='lonerzboy', password='Flaming906', user_agent='PLaystore Bot')

subreddit = reddit.subreddit('sziyan_testing')
start_time = time.time()




for comments in subreddit.stream.comments():
    if comments.created_utc < start_time:
        continue
    else:
        body = comments.body
        if 'linkme:' in body:
            tosplit = body.split('linkme:')
            after_linkme = tosplit[1]
            search_terms = after_linkme.split('\n')[0]
            print(search_terms)
            result = play.search(search_terms,page=1)[0]
            title = result.get('title')
            price = result.get('price')
            score = result.get('score')
            url = result.get('url')
            if result.get('free') is True:
                price = 'Free'
            else:
                price = result.get('price')
            print(url)
            message = "**Title:**{}\n\n**Price:** {}\n\n[Google Play](https://play.google.com{})".format(title,price,url)
            comments.reply(message)
            print("Comment added successfully.")
            continue
        else:
            print("nothing to search")
