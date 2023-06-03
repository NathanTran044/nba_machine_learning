import requests
from bs4 import BeautifulSoup, Comment
import re
import pandas as pd
import time
from collections import OrderedDict

def get_player_names(year):
    url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.find(id="per_game_stats")

    pattern = r'<td class="left" csk=".*?">.*?>(.*?)</a>'
    names = re.findall(pattern, str(text))
    names = list(OrderedDict.fromkeys(names))

    return names

def get_data():
    year = range(1980, 1985)

    for year in year:
        file_path = "/Users/nathantran/Documents/VSCode/salary_predictor/{}.csv".format(year)

        all_players_default_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"

        all_players_url = all_players_default_url.format(year)

        r = requests.get(all_players_url)

        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.find(id="per_game_stats")

        pattern = r'href="(/players[^"]*)"'

        matches = re.findall(pattern, str(text))

        matches = list(OrderedDict.fromkeys(matches)) #removes duplicates

        all_players_table = pd.DataFrame()

        counter = 1

        for x in matches:
            time.sleep(3)
            print("trying", x)
            player_url = "https://www.basketball-reference.com/" + x
            r = requests.get(player_url)
            soup = BeautifulSoup(r.text, "html.parser")

            # get player's season statistics
            player_data = soup.find(id="per_game")
            player_table = pd.read_html(str(player_data), index_col="Season")[0]
            season_str = str(year - 1) + "-" + str(year)[-2::]
            first_row = player_table.loc[season_str] #chooses first season statistic if a player played for multiple teams
            if type(first_row) == pd.DataFrame:
                first_row = first_row.iloc[0]
            player_table = pd.DataFrame.from_records([first_row]) 

            if "Team" in player_table.columns:
                player_table.rename(columns={"Team": "Tm"}, inplace=True)

            # get player's season salary
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            salaries_comment = None

            for comment in comments:
                if "all_salaries" in comment:
                    salaries_comment = comment
                    break
            
            if salaries_comment is None:
                print("No salary data")
                continue

            salaries_soup = BeautifulSoup(salaries_comment, "html.parser")
            salary_data = salaries_soup.find(id="all_salaries")
            salary_table = pd.read_html(str(salary_data), index_col="Season")[0]
            try:
                index = salary_table.index.get_loc(season_str)
            except KeyError:
                print("No salary year")
                continue
            if type(index) == slice: # chooses first salary if a player has multiple salaries in one year
                index = index.start
            salary_table = salary_table.iloc[[index]]
            column_to_append = salary_table["Salary"]
            cleaned_values = column_to_append.str.replace('[^\d.]', '', regex=True)
            numeric_values = pd.to_numeric(cleaned_values, errors='coerce')
            player_table.at[0, "Salary"] = numeric_values.iloc[0] # sets the salary in the player_table
            player_table = player_table.fillna(0)

            if numeric_values.dtype == int: # makes sure a valid salary
                all_players_table = pd.concat([all_players_table, player_table])
            else:
                print("Not a valid salary")

            print("finish " + str(counter) + " " + x)
            counter += 1

        all_players_table = all_players_table.reset_index(drop=True)
        all_players_table = all_players_table.rename_axis("Player")
        all_players_table.to_csv(file_path)
        print("finish year ", year)