import play_scraper as play

result = play.search('sword of ditto',page=1, detailed=True)[0]

print(result.get('title'))