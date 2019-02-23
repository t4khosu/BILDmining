import re

def removeWhitespaces(text):
    return " ".join(text.split())

def extractCleanedAuthors(text):
    text = text.replace('und', ',').title()
    text = text.replace('Und', ',').title()
    text = text.replace('&', ',').title()
    text = re.sub(r" ?\([^)]+\)", "", text)
    authors = text.split(',')
    authors = [a.strip() for a in authors]
    return authors

def isArticleUrlValid(url):
    if (url.count('http')) > 1:
        return False                        
    if 'video/clip/' in url:
        return False
    if 'startseite' in url:
        return False
    return True

def cleanContent(content):
    cleanedContent = ''
    for p in content.findAll('p'):
        cleanedContent += p.text
    return " ".join(cleanedContent.split())

def cleanDate(dateStr):
    if dateStr:
        return dateStr.split('+')[0]
    return None