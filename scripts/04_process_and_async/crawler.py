import asyncio
from concurrent.futures.process import ProcessPoolExecutor
from dataclasses import dataclass
from multiprocessing.pool import Pool

import aiohttp
import bloom_filter
import bs4
from bs4 import ResultSet, Tag
from urllib.parse import urljoin


@dataclass
class Page:
    url: str
    title: str
    body: str
    links: list[str]


def parse(url: str, html: str) -> Page:
    soup = bs4.BeautifulSoup(html, 'html.parser')
    all_links: ResultSet[Tag] = soup.find_all("a")
    final_links: list[str] = []

    for link in all_links:
        href = link.attrs.get("href", None)
        href = urljoin(url, href)
        if "http" in href:
            final_links.append(str(href))

    page = Page(url, str(soup.title),
                str(soup.body.get_text()) if soup.body else '', final_links)
    return page


class Crawler:

    def __init__(self, pool: ProcessPoolExecutor):
        self.queue = asyncio.Queue()  # Input
        self.history = set()
        self.pool = pool
        self.loop = asyncio.get_running_loop()

    async def fetch(self, url: str) -> Page:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                html = await response.text()

                # Parse the HTML in an executor
                page = await self.loop.run_in_executor(self.pool, parse, url, html)
                return page

    async def worker(self):
        while True:
            print("Waiting for work")
            url = await self.queue.get()
            if url in self.history:
                continue
            self.history.add(url)
            print("Work to do", url)
            page = await self.fetch(url)
            for link in page.links:
                await self.queue.put(link)


async def start(pool: Pool):
    crawler = Crawler(pool)
    await crawler.queue.put("https://fr.wikipedia.org/")
    await asyncio.gather(*[crawler.worker() for _ in range(10)])


if __name__ == '__main__':
    with ProcessPoolExecutor(4) as pool:
        asyncio.run(start(pool))
