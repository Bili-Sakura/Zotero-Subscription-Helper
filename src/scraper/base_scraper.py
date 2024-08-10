import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get_page(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch page {url}: {e}")

    def parse_html(self, html):
        return BeautifulSoup(html, "html.parser")

    @abstractmethod
    def scrape(self):
        """This method should be implemented by subclasses to scrape specific data."""
        pass
