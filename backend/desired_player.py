import requests
from bs4 import BeautifulSoup, Comment
import re
import pandas as pd

# get_desired_player("Tom Brady", 1988)

def get_desired_player(name, year):
    url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)

    split_name = name.split()
    desired_player = split_name[-1] + "," + " ".join(split_name[:-1])

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    found = False
    row = soup.find('tr', class_='full_table')
    while not found:
        if row:
            if desired_player in str(row):
                found = True
                break
            row = row.find_next('tr', class_='full_table')
        else:
            break

    pattern = r'data-stat="([^"]*)">([^<]*)<'
    matches = re.findall(pattern, str(row))

    change_name(matches)

    column_names = ['Player', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 
                    'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 
                    'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 
                    'BLK', 'TOV', 'PF', 'PTS', 'Salary']
    
    stats = []

    for value in matches:
        stats.append(value[1])

    result = {}

    for name in column_names:
        found = False
        for key, value in matches:
            if key == name:
                result[name] = value
                found = True
        if not found:
            result[name] = 0

    return(result)

def change_name(matches):
    name_map = {"player": "Player", "pos": "Pos", "age": "Age", "team_id": "Tm", "g": "G", "gs": "GS", 
                "mp_per_g": "MP", "fg_per_g": "FG", "fga_per_g": "FGA", "fg_pct": "FG%", "fg3_per_g": "3P", 
                "fg3a_per_g": "3PA", "fg3_pct": "3P%", "fg2_per_g": "2P", "fg2a_per_g": "2PA", "fg2_pct": "2P%", 
                "efg_pct": "eFG%", "ft_per_g": "FT", "fta_per_g": "FTA", "ft_pct": "FT%", "orb_per_g": "ORB", 
                "drb_per_g": "DRB", "trb_per_g": "TRB", "ast_per_g": "AST", "stl_per_g": "STL", "blk_per_g": "BLK",
                  "tov_per_g": "TOV", "pf_per_g": "PF", "pts_per_g": "PTS"}

    for i, value in enumerate(matches):
        value_list = list(value)
        value_list[0] = name_map.get(value[0])
        if value_list[1] == '':
            value_list[1] = 0
        matches[i] = tuple(value_list)