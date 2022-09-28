# What is this?
This is supposed to produce [tachiyomi](https://tachiyomi.org) compatible manga https://tachiyomi.org/help/guides/local-manga/#folder-structure

I haven't tested yet
# Requirements
```cmd
pip install beautifulsoup4
```
# Running
The following commands will download 300 chapters of vagabond in different directories
```cmd
python scraper.py https://vagabond-chapters.com/manga/vagabond-chapter- 300
python scraper.py https://vagabond-chapters.com/manga/vagabond-chapter- 300 C:\Manga\Vagabond\
python scraper.py https://vagabond-chapters.com/manga/vagabond-chapter- 300 Manga\Vagabond\
```