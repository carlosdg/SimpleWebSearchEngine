from urllib.parse import urlparse
import aiohttp
import asyncio


def check_if_internal_link(base, link):
  """
    Returns whether the given link is hosted in the same
    server as the base link and if they have the same 
    scheme (http, https, ftp...)
  """
  base = urlparse(base)
  link = urlparse(link)

  return base.scheme == link.scheme \
     and base.hostname == link.hostname


def get_initial_urls():
  """
    Reads the file with the starting URLs and returns
    a list of these
  """
  with open("config/urls.txt") as urls_file:
    url_list = urls_file.read().split("\n")
    url_list = [url.strip() for url in url_list]

    return url_list


async def fetch(session, url):
  """
    Tries to fetch the web page of the given URL and
    returns the status code and the content if the
    status is 200. If there is any connection error 
    it returns -1 as response status
  """
  try:
    async with session.get(url) as response:
      if response.status == 200:
        text = await response.text()
        return text, response.status
      else:
        return "", response.status
  except:
    return "", -1


async def main():
  urls = get_initial_urls()
  timeout = aiohttp.ClientTimeout(total=60)

  async with aiohttp.ClientSession(timeout=timeout) as session:
    response_promises = [fetch(session, url) for url in urls]
    responses = await asyncio.gather(*response_promises)

    print("\n\n\n")
    for text, status in responses:
      print("Body:", text[:15].strip(), "...", "Size:", len(text), "Status:", status)


if __name__ == "__main__":
  asyncio.run(main())