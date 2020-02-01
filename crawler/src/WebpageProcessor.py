from urllib.parse import urlparse
from bs4 import BeautifulSoup
import asyncio


class WebScraper:
    """
      Helper class for WeppageProcessor, it wraps around
      BeautifulSoup and provides WeppageProcessor the 
      functionality needed
    """

    def __init__(self, html):
        self.soup = BeautifulSoup(html, features="html.parser")

    def get_text(self):
        """
            Warning: This modifies the given HTML string!!
        """
        tags_to_remove = ["script", "head", "img", "figure", "style"]
        for tag in tags_to_remove:
            [el.extract() for el in self.soup.findAll(tag)]

        return self.soup.get_text()

    def get_title(self):
        return self.soup.title.get_text().strip()

    def get_internal_links(self, base_url):
        base = urlparse(base_url)

        def check_if_internal_link(link):
            link = urlparse(link)

            return base.scheme == link.scheme \
                and base.netloc == link.netloc

        return [a.get('href')
                for a in self.soup.find_all('a', href=check_if_internal_link)]


class WebpageProcessor:
    """
      The responsibility of this class is to process the
      response of the URL requests, delegate the store 
      responsibility to WebpageStore and return the internal 
      links found in the page so the Crawler keeps going.
    """

    def __init__(self, webpage_store):
        self.store = webpage_store

    async def process_success(self, url, status, html):
        scrapper = WebScraper(html)
        internal_links = scrapper.get_internal_links(url)
        title = scrapper.get_title()
        text = scrapper.get_text()

        await self.store.store_success_page(url, title, text)

        return internal_links

    async def process_error(self, url, status):
        await self.store.store_error_page(url, status)
