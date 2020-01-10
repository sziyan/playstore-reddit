# from app import session
# from app.models import Games
#
# game_1 = session.query(Games).filter_by(month='Jan 20').all()
# game_2 = session.query(Games).filter_by(month='Jan 20')
#
# print('1={}'.format(game_1))
# print('\n\n\n\n')
# print('2={}'.format(game_2))
# for games in game_2:
#     print(games.title)

from datetime import date,datetime

d = date(2020,2,25)
print(d)