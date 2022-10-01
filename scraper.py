import argparse
import asyncio
from pathlib import Path

import aiohttp
from bs4 import BeautifulSoup


# Download all images from a given URL and save them to a folder asynchonously
async def download_images(url, folder):
    if not folder.exists():
        folder.mkdir(parents=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            images = soup.find_all('img')
            for index, image in enumerate(images):
                src = image['src']
                filename = f'{index}.jpg'
                async with session.get(src) as response:
                    with open(f'{folder}/{filename}', 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                print(f'Downloaded {filename}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL to download images from')
    parser.add_argument('max_chapters', help='Maximum number of chapters to download')
    parser.add_argument('folder', help='Folder to save images to', nargs='?')
    args = parser.parse_args()

    outpath = Path(args.folder) if args.folder else Path(__file__).parent / "Manga"

    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(1, int(args.max_chapters) + 1):
        tasks.append(download_images(args.url.format(chapter=i), outpath / f"ch{i}"))
    loop.run_until_complete(asyncio.wait(tasks))
