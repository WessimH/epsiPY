import asyncio
from dataclasses import dataclass
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

async def parse(url: str, html: str) -> Page:
    soup = bs4.BeautifulSoup(html)
    all_links: ResultSet[Tag] = soup.find_all("a")
    final_links: list[str] = []

    link: Tag
    for link in all_links:
        href = link.attrs.get("href", None)
        href = urljoin(url, href)
        final_links.append(str(href))

    return Page(url, soup.title, soup.body, final_links)

async def fetch(url: str) -> Page:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")
            return await parse(url, html)


queue = asyncio.Queue() # Input
history = set()

async def worker():
    while True:
        print("Waiting for work")
        url = await queue.get()
        if url in history:
            continue
        history.add(url)
        print("Work to do", url)
        page = await fetch(url)
        for link in page.links:
            await queue.put(link)

async def start():
    await queue.put("https://fr.wikipedia.org/")
    await worker()

if __name__ == '__main__':
    asyncio.run(start())
