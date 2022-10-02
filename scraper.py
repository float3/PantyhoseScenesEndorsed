import argparse
import asyncio
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup


def extract_next_link(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")
    next_button = [link for link in links if "next" or "continue" in link.text.lower()]
    if next_button:
        return next_button[0]["href"]


def get_referer(url):
    parsed = urlparse(url)
    return {"Referer": f"{parsed.scheme}://{parsed.hostname}"}


# Download all images from a given URL and save them to a folder asynchonously
async def download_images(url, folder):
    if not folder.exists():
        folder.mkdir(parents=True)
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            images = soup.find_all("img")
            for index, image in enumerate(images):
                src = image["src"]
                filename = f"{index}.jpg"
                async with session.get(src) as response:
                    if response.ok:
                        with open(f"{folder}/{filename}", "wb") as f:
                            while True:
                                chunk = await response.content.read(1024)
                                if not chunk:
                                    break
                                f.write(chunk)
                            print(f"Downloaded {filename}")
                    else:
                        print(f"Failed to download {src}. Status {response.status}: {response.reason}")


# Crawl from a start site via the "next" button and download all images
async def crawl(start_url, folder, max_steps=10):
    url = start_url
    index = 0
    tasks = []
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while url:
            index += 1
            tasks.append(asyncio.create_task(download_images(url, Path(folder) / f"ch{index}")))
            async with session.get(url) as response:
                print(f"Downloading {url}")
                html = await response.text()
                url = extract_next_link(html)
                if index >= max_steps:
                    break
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to download images from")
    parser.add_argument("max_chapters", help="Maximum number of chapters to download")
    parser.add_argument("folder", help="Folder to save images to", nargs="?")
    args = parser.parse_args()

    outpath = Path(args.folder) if args.folder else Path(__file__).parent / "Manga"

    HEADERS = {}
    HEADERS.update(get_referer(args.url))

    loop = asyncio.get_event_loop()
    tasks = []
    if r"{chapter}" not in args.url:
        tasks.append(crawl(args.url, outpath, int(args.max_chapters)))
    else:
        for i in range(1, int(args.max_chapters) + 1):
            tasks.append(download_images(args.url.format(chapter=i), outpath / f"ch{i}"))
    loop.run_until_complete(asyncio.wait(tasks))
