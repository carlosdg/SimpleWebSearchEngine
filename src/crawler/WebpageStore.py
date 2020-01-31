import asyncio



class WebpageStore:
  """
    The responsibility of this class is to store the
    responses of the URL requests. Right now it is
    implemented to store the requests in a file.
  """
  async def store_success_page(self, url, title, text):
    with open("test.txt", "a") as file:
      file.write(f"URL: {url}. Title: {title}.\n")
  
  async def store_error_page(self, url, status):
    with open("test_error.txt", "a") as file:
      file.write(f"URL: {url}. Status: {status}.\n")