import requests

from bs4 import BeautifulSoup


class User:

    def __init__(self, name):
        self.url = 'https://twitter.com/{name}'.format(name=name)

    def location(self, proxies=None, headers=None):
        response = requests.get(self.url, headers=headers, proxies=proxies, timeout=10)
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        location = soup.find_all('span', {'class': 'ProfileHeaderCard-locationText'})
        return location[0].get_text().strip() if location else ''
