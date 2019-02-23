import re, requests, json
from bs4 import BeautifulSoup
from util.DataCleaner import isArticleUrlValid

class Spider(object):
    """ Check for article URLs on bild.de """
    
    def __init__(self, parameters):
        self.mainUrl = parameters["spider"]["main-url"]
        self.navUrls = parameters["spider"]["nav-urls"]
        self.article_urls = set([])

    def extractAllArticleUrls(self):
        """ Extract all articles found on bild.de

        For every navigation link (politik, sport, ...) the given site looks for relevant URLs.
        Relevant URLs contain a `rel` with value `bookmark`.
        An URL is generated and checked, after it is stored in a set (article_urls)
        """
        for nav in self.navUrls:
            url = self.mainUrl + self.navUrls[nav]
            htmlResponse = requests.get(url)
            if htmlResponse.status_code == 200:
                soup = BeautifulSoup(htmlResponse.content, "lxml")
                articles = soup.findAll("a", {"rel": "bookmark"}, href=True)
                for a in articles:
                    fullUrl = url + a['href']
                    if isArticleUrlValid(fullUrl):
                        self.article_urls.add((nav, fullUrl))
            else:
                print("HTTP Exception: {}, URL: {}".format(htmlResponse.status_code, url))