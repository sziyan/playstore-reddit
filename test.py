import play_scraper as play

search='clash of clans'

result = play.search(search)[0]

score = result.get('score')
print(result)