import requests
from bs4 import BeautifulSoup
import csv

url = "https://store.steampowered.com/search/?filter=topsellers"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

games = soup.select("a.search_result_row")

data = []

for game in games:
    
    title = game.select_one("span.title").text.strip()
    
    release_tag = game.select_one(".search_released")
    release_date = release_tag.text.strip() if release_tag else "N/A"
    
    review_tag = game.select_one(".search_reviewscore span")
    review = review_tag['data-tooltip-html'].split('<br>')[0] if review_tag and 'data-tooltip-html' in review_tag.attrs else "N/A"

    data.append([title, review, release_date])

with open("static.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["遊戲名稱", "評價", "發售日"])
    writer.writerows(data)

print("已儲存為 static.csv")
