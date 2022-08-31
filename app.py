from tools import get_ranked_matches_PD, get_data_ranked_match

import os
dir_path = os.path.dirname(os.path.realpath(__file__))


#elo=['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']
#rank= ['IV', 'III', 'II', 'I']
elo= 'IRON'

if '{}_matches.csv'.format(elo) not in os.listdir(dir_path):
    print('comensando cosecha...')
    get_ranked_matches_PD(elo, '1','20')

else:
    a, b= get_data_ranked_match(elo)
    