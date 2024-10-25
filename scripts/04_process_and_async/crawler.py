import asyncio
from dataclasses import dataclass
from multiprocessing.pool import Pool
from typing import Any

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


class Crawler:

    def __init__(self, pool: Pool):
        self.queue = asyncio.Queue()  # Input
        self.history = set()

    async def parse(self, url: str, html: str) -> Page:
        soup = bs4.BeautifulSoup(html)
        all_links: ResultSet[Tag] = soup.find_all("a")
        final_links: list[str] = []

        link: Tag
        for link in all_links:
            href = link.attrs.get("href", None)
            href = urljoin(url, href)
            final_links.append(str(href))

        return Page(url, soup.title, soup.body, final_links)

    async def fetch(self, url: str) -> Page:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                html = await response.text()
                print("Body:", html[:15], "...")
                return await self.parse(url, html)

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
    await crawler.worker()


if __name__ == '__main__':
    pool = Pool(4)
    asyncio.run(start(pool))
