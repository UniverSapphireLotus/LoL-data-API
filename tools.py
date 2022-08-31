# -*- coding: utf-8 -*-
from pandas.io.json import json_normalize
import json
import requests
import pandas as pd



my_api='your api'
rank= ['IV', 'III', 'II', 'I']

def get_puuid(summoner_id):
    
    try:
        call_puuid='https://la1.api.riotgames.com/lol/summoner/v4/summoners/'+summoner_id+'?api_key='+my_api
        request= json.loads(requests.get(call_puuid).text)
        print(type(request))
        return request['puuid']
    
    except:
        print('estoy fallando ids... kill me')

def get_ranked_matches(puuid, count):
    ranked_matches=[]
    try:
        call_ranked_match='https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/'+puuid+ '/ids?type=ranked&start=0&count='+count+'&api_key='+my_api
        request= requests.get(call_ranked_match)
        ranked_matches+= json.loads(request.text)
        print(ranked_matches)
        return ranked_matches
    except:
        print('estoy muriendo matches... :c')
        return []

    
def get_ranked_matches_PD(elo, page,count):
    ranked_matches= pd.DataFrame()
    for r in rank:
        call_summonerID= 'https://la1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/'+elo+'/'+r+'?page='+page+'&api_key='+my_api
        #call= 'https://americas.api.riotgames.com/lol/match/v5/matches/LA1_1293749723?api_key=RGAPI-ffb91676-bd92-4e31-8ea6-762d7adff5f9'
        request= requests.get(call_summonerID)
        dt_summoners= pd.DataFrame(json_normalize(request.json()))
        dt_summoners['puuis']= dt_summoners['summonerId'].apply(get_puuid)
        
        r_tempo=[]
        for index, row in dt_summoners.iterrows():
            r_tempo+= get_ranked_matches(row['puuis'], count) 
        
        r_tempo= pd.DataFrame({'matchId': r_tempo})
        
        r_tempo['rank']=r
        ranked_matches= pd.concat([ranked_matches, r_tempo], ignore_index=True, sort=False)
        
    ranked_matches['elo']=elo
    ranked_matches.to_csv('{}_matches.csv'.format(elo), sep='\t')

def get_data_ranked_match(elo):
    data_match= pd.DataFrame()
    match_id= pd.read_csv('{}_matches.csv'.format(elo), sep='\t')
    match_id.drop('Unnamed: 0', axis=1, inplace=True)
    
    for index, row in match_id.head(5).iterrows():
        call_match= 'https://americas.api.riotgames.com/lol/match/v5/matches/'+row['matchId']+'/?api_key='+my_api
        request= requests.get(call_match)
        tempo= json.loads(request.text)
        data_match= pd.concat([data_match, pd.DataFrame(tempo)], ignore_index=True)
        print(request.status_code)
        
    return pd.DataFrame(tempo), tempo
