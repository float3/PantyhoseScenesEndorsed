# What is this?
This is supposed to produce [tachiyomi](https://tachiyomi.org) compatible manga https://tachiyomi.org/help/guides/local-manga/#folder-structure

# Please report manga sites that don't work!

- vagabond-chapters.com doesn't work anymore, it looks like they added some anti bot measures, potentially because I used them for testing

# Requirements
```cmd
pip install beautifulsoup4
pip install aiohttp
```
# Running
The following commands will download 300 chapters of vagabond in different directories
```cmd
python scraper.py "https://vagabond-chapters.com/manga/vagabond-chapter-{chapter}" 1 300
python scraper.py "https://vagabond-chapters.com/manga/vagabond-chapter-{chapter}" 1 300 C:\Manga\Vagabond\
python scraper.py "https://vagabond-chapters.com/manga/vagabond-chapter-{chapter}" 1 300 Manga\Vagabond\
```

If no `{chapter}` tag is available in the given url the scraper tries to find the **next** button, and crawl along it instead.
```cmd
python scraper.py "https://vagabond-chapters.com/manga/vagabond-chapter-1" 300
```
