import play_scraper as play

search='sjfhskjbfwekrjhuisdyfs'

result = play.search(search)
if result:
    print(result[0])
else:
    print("error")