from urllib.parse import urlparse
from bs4 import BeautifulSoup
import aiohttp
import asyncio


class WebScraper:
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



def get_initial_urls():
  """
    Reads the file with the starting URLs and returns
    a list of these
  """
  with open("config/urls.txt") as urls_file:
    url_list = urls_file.read().split("\n")
    url_list = [url.strip() for url in url_list]

    return url_list



class WebpageProcessor:
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



class WebpageStore:
  async def store_success_page(self, url, title, text):
    with open("test.txt", "a") as file:
      file.write(f"URL: {url}. Title: {title}.\n")
  
  async def store_error_page(self, url, status):
    with open("test_error.txt", "a") as file:
      file.write(f"URL: {url}. Status: {status}.\n")



class Crawler:
  def __init__(self, page_processor, max_depth=1, timeout=60, verbose=False):
    self.page_processor = page_processor
    self.max_depth = max_depth
    self.timeout = aiohttp.ClientTimeout(total=timeout)
    self.verbose = verbose


  async def run(self, initial_urls):
    self.processed_urls = set()

    return await self._process_all_urls(initial_urls)


  async def _process_all_urls(self, urls, depth=1):
    if depth > self.max_depth: 
      return

    async with aiohttp.ClientSession(timeout=self.timeout) as session:
      promises = [self._process_url(session, url, depth) for url in urls]
      await asyncio.gather(*promises)

    
  async def _process_url(self, session, url, depth):
    if url in self.processed_urls: 
      return
    else:
      self.processed_urls.add(url)
      if self.verbose: print(f"New URL. Depth={depth}. URL={url}")

    try:
      async with session.get(url) as response:
        if response.status == 200:
          html = await response.text()
          links = await self.page_processor.process_success(url, response.status, html)
          links = [link for link in links if link not in self.processed_urls]
          await self._process_all_urls(links, depth + 1)
        else:
          await self.page_processor.process_error(url, response.status)
    except:
      await self.page_processor.process_error(url, -1)



async def main():
  webpage_store = WebpageStore()
  webpage_processor = WebpageProcessor(webpage_store)
  crawler = Crawler(webpage_processor, max_depth=3, verbose=True)
  # initial_urls = ["https://en.wikipedia.org/wiki/Web_scraping"] 
  # initial_urls = [f"https://swapi.co/api/people/{i}" for i in range(1, 3)] 
  initial_urls = get_initial_urls()
  await crawler.run(initial_urls)



if __name__ == "__main__":
  asyncio.run(main())