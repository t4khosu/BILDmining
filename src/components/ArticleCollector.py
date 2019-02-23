import requests, json, sys, time
from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup
from components.Article import Article
from components.Publisher import Publisher
from components.Spider import Spider
from util.DataCleaner import removeWhitespaces, extractCleanedAuthors, cleanContent

class ArticleCollector(object):
    def __init__(self, parameters, databaseManager):
        self.url = parameters['url']
        self.src = parameters['src']
        self.apiKey = parameters['apiKey']
        self.spider = Spider(parameters)
        self.databaseManager = databaseManager

    def collectArticles(self, light=False):
        """Collect all Articles with a spider

        The spider returns a list of possible article URLs.
        These are going to be further processed after having checked if the URL is valid (Status: 200)

        Args:
            light (bool) : if set, only articles with new URLs are considered new.
                            Modified articles are ignored, which results in much faster computing time.
        Returns:
            article_count (int) : Amount of new articles, that were added to the DB
        """
        self.spider.extractAllArticleUrls() # [(type, article_url), ...]
        stored = 0
        found = 0

        for articleTuple in tqdm(self.spider.article_urls):
            type = articleTuple[0]
            url = articleTuple[1]

            # light shortcut
            if light and self.databaseManager.articleURLInStore(url):
                continue

            try:
                found += 1
                response = requests.get(url)
                if response.status_code == 200:
                    if self.storeArticle(type, url, response.text):
                        stored += 1
                else:
                    raise("Error Code {} occured.".format(response.status_code))
            except requests.exceptions.ConnectionError as e:
                raise("Connection Error: {}".format(e))
        return {"found" : found, "stored" : stored}

    def storeArticle(self, articleType, articleUrl, htmlContent):
        """Extract information from a given article URL

        Args:
            articles (json) : List of articles with meta data
        """
        metaList, content = self.extractTxtFromHtmlContent(htmlContent)
        if not content or not metaList:
            return False # Nothing relevant to store

        publisher_id = self.databaseManager.addPublisher(Publisher(metaList[0]))
        article = Article(metaList, content, articleType, articleUrl)
        article_id = self.databaseManager.addArticle(article, publisher_id)
        if article_id == -1:
            return False # Entry already exists in Table

        if article.hasAuthors():
            author_ids = self.databaseManager.addAuthors(article.authors)
            self.databaseManager.addAuthorsArticles(author_ids, article_id) 
        return True # Successfully stored

    def extractTxtFromHtmlContent(self, content):
        """Extract meta data and content from a given BILD article

        First check, if website exists. If it is the case, a div container with class 'txt'
        is searched for. Those contain main-content. 
        Also a script of type `application/ld+json` and a json-file `pageTracking` is searched for. These contain meta data.
        Found data is cleaned (spaces and escape sequences)
        
        Args:
            htmlResponse (response): request response to an url

        Returns:
            meta (list(json)): all meta data , there can be multiple metas, but all of them will be formatted as json
            paragraphs (list): list of all paragraphs. If a paragraph is in a <strong>-tag, 
            it is an important paragraph. Otherwise it is a normal paragraph
        """
        try:
            soup = BeautifulSoup(content, "lxml")
            rawContent = soup.findAll("div", {"class": "txt"})
            meta1 = soup.findAll("script", {"type": "application/ld+json"})
            
            content = ''
            if rawContent:
                content = cleanContent(rawContent[0])
            
            meta1 = json.loads(meta1[0].text, strict=False) if meta1 else []

            # extract json from JS without soup
            pageTracking = "pageTracking = {"
            meta2_start = str(soup).find(pageTracking) + len(pageTracking)-1
            meta2_end = str(soup).find("};", meta2_start) + 1
            meta2 = json.loads(str(soup)[meta2_start:meta2_end])
            return [meta1, meta2], content
        except:
            print('Error while extraction data from html content')
            return None, None