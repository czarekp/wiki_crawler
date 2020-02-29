import urllib.parse
import time

import requests
from bs4 import BeautifulSoup

wikipedia = {
    "base_url": "https://en.wikipedia.org",
    "random_url": "https://en.wikipedia.org/wiki/Special:Random",
    "target_url": "https://en.wikipedia.org/wiki/Philosophy"
}
article_chain = []
next_url = wikipedia["random_url"]


def continue_crawl(search_history, max_steps=25):
    """Crawling should be finished when crawler:
        - reaches target
        - reaches a page it has already visited
        - goes on for too long (max. 25 steps)"""
    if wikipedia["target_url"] in search_history:
        print("The target article has been found!")
        return False
    elif len(search_history) > max_steps:
        print("The search has gone too long. Aborting search...")
        return False
    elif len(search_history) > len(set(search_history)):
        print("This article has been already visited. Aborting search...")
        return False
    else:
        return True


def find_first_link(url):
    """Finds first anchor tag and returns its href attribute parsed with Wikipedia base URL."""
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # This div contains the article's body (nested in two div tags)
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    # Find all the direct children of content_div that are paragraphs
    for element in content_div.find_all("p", recursive=False):
        # Find the first anchor tag which is a direct child of a paragraph
        # This must be a direct child due to other types which also can be anchors (e.g. footnotes)
        if element.find("a", recursive=False):
            anchor_tag = element.find("a", recursive=False)
            href_attr = anchor_tag.get("href")
            anchor_title = anchor_tag.get("title")
            print(anchor_title)
            return urllib.parse.urljoin(wikipedia["base_url"], href_attr)


while continue_crawl(article_chain):
    first_link = find_first_link(next_url)
    if not first_link:
        print("An article has no links. Aborting search...")
        break
    article_chain.append(first_link)
    next_url = first_link
    time.sleep(1)
