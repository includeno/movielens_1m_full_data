import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/chart/top/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

movie_titles = []
for movie in soup.select('td.titleColumn'):
    title = movie.select('a')[0].get_text()
    movie_titles.append(title)

print(movie_titles)
