import Setup
import feedparser
import gc


def loadNews():
    items = []
    del items[:]
    for url in Setup.feeds:
        feed = feedparser.parse(url)
        posts = feed["items"]
        for post in posts:
            word_check = str(post)
            if not any(word in word_check for word in Setup.excludeList):
                items.append(post['published'] + " " + post['title'])
                gc.collect()
    return items
