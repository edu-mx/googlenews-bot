import feedparser
from log import Logger

log = Logger()

class RSSBot:
    def __init__(self, search, lang):
        self.search = search
        self.lang = lang

    def get_news(self):
        rss_entries = {}
        search_format = self.search.replace(' ', '%20')
        url = f'https://news.google.com/rss/search?q={search_format}&hl={self.lang}'
        try:
            feed = feedparser.parse(url)
            if feed.bozo == 0:
                for item in feed.entries:
                    properties = (item.link, item.published)
                    rss_entries[item.title] = properties
                return rss_entries
            else:
                return None
        except Exception as x:
            log.critical('Não foi possível buscar notícias no rss: %s' %x)