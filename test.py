import play_scraper as play

result = play.search('another eden',page=1, detailed=True)[0]

print(result.get('score'))