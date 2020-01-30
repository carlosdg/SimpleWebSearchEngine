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



processed_urls = set()

async def process_url(session, url, depth):
  if url in processed_urls: 
    return
  else:
    processed_urls.add(url)
    print(f"New URL. Depth={depth}. URL={url}")

  try:
    async with session.get(url) as response:
      if response.status == 200:
        html = await response.text()
        scrapper = WebScraper(html)
        title = scrapper.get_title()
        text = scrapper.get_text()
        internal_links = scrapper.get_internal_links(url)
        internal_links = [link for link in internal_links if link not in processed_urls]

        with open("test.txt", "a") as file:
          file.write(f"URL: {url}. Status: {response.status}. Title: {title}.\n")
        
        await process_all_urls(internal_links, depth + 1)
      
      else:
        with open("test_error.txt", "a") as file:
          file.write(f"URL: {url}. Status: {response.status}.\n")

  except:
    with open("test_error.txt", "a") as file:
      file.write(f"URL: {url}. Status: -1.\n")



async def process_all_urls(urls, depth=1):
  if depth > 3: return

  timeout = aiohttp.ClientTimeout(total=60)

  async with aiohttp.ClientSession(timeout=timeout) as session:
    promises = [process_url(session, url, depth) for url in urls]
    await asyncio.gather(*promises)



async def main():
  # initial_urls = ["https://en.wikipedia.org/wiki/Web_scraping"] 
  # initial_urls = [f"https://swapi.co/api/people/{i}" for i in range(1, 3)] 
  initial_urls = get_initial_urls()
  await process_all_urls(initial_urls)



if __name__ == "__main__":
  asyncio.run(main())