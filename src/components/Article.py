from util.DataCleaner import cleanDate

class Article(object):
    def __init__(self, metas, content, articleType, url):
        self.articleType = articleType
        self.content = content
        self.url = url
        
        self.id = metas[1]['documentId']
        self.headline = metas[0]['headline'] if 'headline' in metas[0] else None
        self.family_friendly = metas[0]['isFamilyFriendly'] == 'true' if 'isFamilyFriendly' in metas[0] else None
        self.key_words = metas[0]['keywords'] if 'keywords' in metas[0] else None
        self.permanent = metas[1]['permanenterInhalt'] != "0" if 'permanenterInhalt' in metas[1] else None
        self.premium = metas[1]['premium'] if 'premium' in metas[1] else None
        self.description = metas[0]['description'] if 'description' in metas[0] else None
        self.authors = metas[0]['author'] if 'author' in metas[0] else None

        self.published_at = cleanDate(metas[0]['datePublished'] if 'datePublished' in metas[0] else None)
        self.modified_at = cleanDate(metas[0]['dateModified'] if 'dateModified' in metas[0] else None)

    def hasAuthors(self):
        if self.authors:
            return True
        return False