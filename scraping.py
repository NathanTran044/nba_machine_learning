import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium import webdriver


year = 2018

all_players_default_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"

all_players_url = all_players_default_url.format(year)

r = requests.get(all_players_url)

soup = BeautifulSoup(r.text, "html.parser")

test = soup.find(id="per_game_stats")

pattern = r'href="(/players[^"]*)"'

matches = re.findall(pattern, str(test))

matches = [*set(matches)] #removes duplicates

# for x in matches:
#     player_url = "https://www.basketball-reference.com/" + x
player_url = "https://www.basketball-reference.com/players/a/abrinal01.html"
r = requests.get(player_url)
soup = BeautifulSoup(r.text, "html.parser")
# get player's season statistics
player_data = soup.find(id="per_game")
player_table = pd.read_html(str(player_data), index_col="Season")[0]
season_str = str(year - 1) + "-" + str(year)[-2::]
player_table = player_table.loc[[season_str]]

# get player's season salary
# driver = webdriver.Chrome()
# title = driver.find_element_by_xpath('.//*[@id="all_salaries"]').text
# print(title)

soup.find("div", class_="section_heading assoc_all_salaries has_controls").decompose()
salary_data = soup.find(id="all_all_salaries")
print(salary_data)
# salary_table = pd.read_html(str(salary_data), index_col="Season")[0]
# print(salary_table)
# salary_table = pd.read_html(str(salary_data), index_col="Season")

# print(player_table.dtypes)
predictors = player_table.columns[~player_table.columns.isin(["Tm", "Lg", "Pos"])]
