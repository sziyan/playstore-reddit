import play_scraper as play

game = 'war and order'
result = play.search(game,detailed=True,page=1)[0]
print(result['score'])
