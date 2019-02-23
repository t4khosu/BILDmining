distinctArticlesSQL = """
    (SELECT a1.document_id FROM `articles` AS a1
        WHERE a1.modified_at = 
        (
            SELECT MAX(a2.modified_at) 
                FROM `articles` AS a2 
                WHERE a1.document_id = a2.document_id
        )
    )
"""

countAverageArticleLengthsSQL = """
    (SELECT article_type, AVG(LENGTH(content)) c_count FROM `articles`
        WHERE premium = %s
        AND document_id IN """ + distinctArticlesSQL + """
        GROUP BY article_type
        ORDER BY c_count
    )
"""

countAmountArticleTypesSQL = """
    (SELECT article_type, COUNT(document_id) as c FROM `articles`
        WHERE document_id IN """ + distinctArticlesSQL + """
        GROUP BY article_type
        ORDER BY c
    )
"""


countArticlesByTypeSQL = """
    (SELECT article_type, COUNT(article_type) as cat FROM `articles`
        GROUP BY article_type
        ORDER BY cat
    )
"""

def countAverageArticleLengths(DB, premium=False):
    """ Calculate average content-length for each article type 
    
    Args:
        premium (bool) : check all premium articles or only non-premium articles
    """
    return DB.runSqlFromString(countAverageArticleLengthsSQL, (premium))

def countAmountArticleTypes(DB):
    """ Calculate how many articles for each article_type exists """
    return DB.runSqlFromString(countAmountArticleTypesSQL, ())

def countArticlesByType(DB):
    return DB.runSqlFromString(countArticlesByTypeSQL, ())
