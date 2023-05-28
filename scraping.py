import requests
from bs4 import BeautifulSoup
import re



year = 2018

players_default_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"

players_url = players_default_url.format(year)

r = requests.get(players_url)

players_data = r.text

soup = BeautifulSoup(players_data, "html.parser")

test = soup.find(id="per_game_stats")

pattern = r'href="(/players[^"]*)"'

matches = re.findall(pattern, str(test))



print(type(matches))