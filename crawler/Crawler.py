import aiohttp
import asyncio


class Crawler:
    """ 
      The responsibility of this class is to fetch the content of the given
      URLs and delegate the responsibility of processing the content to a 
      `WebpageProcessor` instance. And also keep fetching the links returned
      by the processor instance until a maximum depth.

      Of course, we do this without processing the same URL more than once
      (unless the starting list of URLs has some duplicates)
    """

    def __init__(self, page_processor, max_depth=1, timeout=60, verbose=False):
        self.page_processor = page_processor
        self.max_depth = max_depth
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.verbose = verbose

    async def run(self, initial_urls):
        """
          Starts the crawler with the given URLs
        """
        self.processed_urls = set()

        return await self.__process_all_urls(initial_urls)

    async def __process_all_urls(self, urls, depth=1):
        """
          Somewhat recursive method. It starts all the promises
          to process the given URLs calling __process_url for each 
          one and waits for all the promises to finish
        """
        if depth > self.max_depth:
            return

        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            promises = [self.__process_url(
                session, url, depth) for url in urls]
            await asyncio.gather(*promises)

    async def __process_url(self, session, url, depth):
        """
          If the given URL has not been processed yet, this
          method fetches the content, delegates the processing
          to the WebpageProcessor instance and calls __process_all_urls
          with the returned URLs from the processor
        """
        if url in self.processed_urls:
            return
        else:
            self.processed_urls.add(url)
            if self.verbose:
                print(f"New URL. Depth={depth}. URL={url}")

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    links = await self.page_processor.process_success(url, response.status, html)
                    links = [
                        link for link in links if link not in self.processed_urls]
                    await self.__process_all_urls(links, depth + 1)
                else:
                    await self.page_processor.process_error(url, response.status)
        except:
            await self.page_processor.process_error(url, -1)
