import readability
from langdetect import detect
from newspaper import Article, fulltext
from selenium import webdriver

from memory_copilot.tools import register_meta
from memory_copilot.utils import WebCrawlError


@register_meta('Crawl web page and return main content', returns={'text': 'str'})
def crawl_web(url: str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        raw_html = driver.page_source
    html = readability.Document(raw_html).summary()
    language = detect(html)[:2]
    try:
        text = fulltext(html, language=language)
        if not text:
            raise ValueError('Empty text')
    except Exception as e:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text
    if not text:
        raise WebCrawlError('Could not crawl web page, returned empty text')
    return text
