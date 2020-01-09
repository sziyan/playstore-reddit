import play_scraper as play

game = 'clash of clans'
result = play.search(game,detailed=True,page=1)[0]
print(result['iap_range'])
