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
        return self.soup.get_text()

    def get_title(self):
        title = self.soup.find("h1")

        if title is None:
            title = self.soup.title
        if title is not None:
            title = title.get_text()

        return title

    def get_internal_links(self, base_url):
        base = urlparse(base_url)

        def check_if_internal_link(link):
            link = urlparse(link)

            return base.scheme == link.scheme \
                and base.hostname == link.hostname

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
        title = scrapper.get_title()
        text = scrapper.get_text()
        internal_links = scrapper.get_internal_links(url)

        await self.store.store_success_page(url, title, text)

        return internal_links

    async def process_error(self, url, status):
        await self.store.store_error_page(url, status)
