from Crawler import Crawler
from WebpageProcessor import WebpageProcessor
from WebpageStore import WebpageStore
import asyncio



def get_initial_urls():
  """
    Reads the file with the starting URLs and returns
    a list of these
  """
  with open("config/urls.txt") as urls_file:
    url_list = urls_file.read().split("\n")
    url_list = [url.strip() for url in url_list]

    return url_list



async def main():
  webpage_store = WebpageStore()
  webpage_processor = WebpageProcessor(webpage_store)
  crawler = Crawler(webpage_processor, max_depth=3, verbose=True)
  # initial_urls = ["https://en.wikipedia.org/wiki/Web_scraping"] 
  initial_urls = [f"https://swapi.co/api/people/{i}" for i in range(1, 3)] 
  # initial_urls = get_initial_urls()
  await crawler.run(initial_urls)



if __name__ == "__main__":
  asyncio.run(main())