import requests as r
from bs4 import BeautifulSoup
from pprint import pprint

soup = lambda x: BeautifulSoup(x, 'html.parser')

class Komikcast:
    url = 'https://komikcast.cz/'
    def __init__(self):
        self.homepage = soup(r.get(self.url).text)

    def hot_update(self):
        series_list = [html.find('a')['href'] for html in self.homepage.find('div', class_='bixbox hothome').find_all('div', class_='swiper-slide splide-slide')]
        series_data = [response for response in [self.series_scrapper(url) for url in series_list]]
        return series_data

    def update(self):
        series_list = [html.find('a', class_='series data-tooltip')['href'] for html in self.homepage.find('div', class_='postbody').find_all('div', class_='uta')]
        series_data = [response for response in [self.series_scrapper(url) for url in series_list]]
        return series_data

    def series_scrapper(self, series_url):
        parser = soup(r.get(series_url).text)
        series_information = parser.find('div', class_='komik_info-content-meta')

        result = {
            'cover': parser.find('div', class_='komik_info-cover-image').find('img')['src'],
            'title': parser.find_all('h3')[1].text.replace('Chapter', ''),
            'series_url': series_url,
            'genre': [{'text': html.text, 'url': html['href']} for html in parser.find('span', class_='komik_info-content-genre').find_all('a')],
            'release': series_information.find('span').text.strip().split(':')[1],
            'author': series_information.find_all('span')[1].text.strip().split(':')[1],
            'status': series_information.find_all('span')[2].text.strip().split(':')[0],
            'description': parser.find('div', class_='komik_info-description-sinopsis').text.strip(),
            'chapter': [{'number': chapter.find('a').text.split('\n')[1], 'url': chapter.find('a')['href'], 'time': chapter.find('div', class_='chapter-link-time').text.strip()} for chapter in parser.find_all('li', class_='komik_info-chapters-item')],
            'rating': parser.find('div', class_='data-rating')['data-ratingkomik']
        }

        return result


