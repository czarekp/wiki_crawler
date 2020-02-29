import requests
from bs4 import BeautifulSoup
import time

wikipedia = {
    "base_url": "https://en.wikipedia.org",
    "random_url": "https://en.wikipedia.org/wiki/Special:Random",
    "target_url": "https://en.wikipedia.org/wiki/Philosophy"
}
article_chain = []
next_url = wikipedia["random_url"]


def continue_crawl(search_history):
    """Crawling should be finished when crawler:
        - reaches target
        - reaches a page it has already visited
        - goes on for too long (max. 25 steps)"""
    if wikipedia["target_url"] in search_history:
        print("The target article has been found!")
        return False
    elif len(search_history) > 25:
        print("The search has gone too long. Aborting search...")
        return False
    elif len(search_history) > len(set(search_history)):
        print("This article has been already visited. Aborting search...")
        return False
    else:
        return True


while continue_crawl(article_chain):
    response = requests.get(next_url)
    soup = BeautifulSoup(response.text, "html.parser")
    page_title = soup.title.string.split(" - ")[0]
    print(page_title)
    first_link = soup.find("div", id="mw-content-text").p.a
    if first_link is None:
        print("This article has no links. Aborting search...")
        break
    next_url = wikipedia["base_url"] + first_link.get("href")
    article_chain.append(next_url)
    time.sleep(1)
