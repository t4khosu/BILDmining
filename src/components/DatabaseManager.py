import pymysql, time, datetime
from util.DataCleaner import removeWhitespaces, extractCleanedAuthors
from os import path
from components.SQLManager import fileToStatements

pymysql.install_as_MySQLdb()

class DatabaseManager:

    def __init__(self, parameters, stored_at):
        mysql = parameters['mysql']
        self.host = mysql['host']
        self.user = mysql['user']
        self.password = mysql['password']
        self.db = mysql['db']
        self.connection = None
        self.stored_at = stored_at

    def startConnection(self):
        """ Start a new connection to a given DB """
        try:
            self.connection = pymysql.connect(host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        charset='utf8mb4',
                                        db=self.db)
            # Text connection
            cursor = self.connection.cursor()
            cursor.execute("SELECT VERSION()")
            print("DB successfully loaded! Version: {}".format(cursor.fetchone()[0]))

            # Set connection to UTF8
            cursor.execute("SET NAMES 'utf8'")
            cursor.execute("SET CHARACTER SET utf8")
            
        except pymysql.err.InternalError as e:
            print("Error occured: {}".format(e))
    
    def closeConnection(self):
        """ Close DB Connection """
        if self.connection:
            self.connection.close()
    
    def runSqlFromFile(self, file):
        """ Run all SQL Statements by reading a file """
        statements = fileToStatements(file)
        if self.connection:
            with self.connection.cursor() as cursor:
                for stmt in statements:
                    cursor.execute(stmt)
                self.connection.commit()
        else:
            raise('No existing connection...')

    def runSqlFromString(self, sqlString, parameters=()):
        """ Run SQL stament from String """
        if not self.connection:
            raise('No connection...')
        with self.connection.cursor() as cursor:
            cursor.execute(sqlString, parameters)
            result = cursor.fetchall()
        self.connection.commit()
        return result

    def addAuthorsArticles(self, author_ids, article_id):
        if not self.connection:
            raise('No connection...')

        sql = "INSERT INTO `articles_authors` (`author_id`, `article_id`) VALUES (%s, %s)"
        with self.connection.cursor() as cursor:
            for author_id in author_ids:
                cursor.execute(sql, (author_id, article_id))
        self.connection.commit()

    def articleURLInStore(self, articleURL):
        sql = "SELECT count(*) FROM `articles` WHERE `article_url` LIKE %s"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (articleURL))
            result = cursor.fetchone()[0]
        self.connection.commit()
        return True if result != 0 else False

    def addArticle(self, article, publisher_id):
        """ Store a new article in table `articles` """
        if self.articleAlreadyStored(article):
            return -1

        with self.connection.cursor() as cursor:
            sql = """INSERT INTO `articles` (`document_id`, `headline`, `content`, `article_url`, `family_friendly`, `key_words`, `published_at`, `permanent`, `premium`, `description`, `article_type`, `modified_at`, `stored_at`, `publisher_id`) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (article.id, article.headline, 
                                    article.content, article.url, 
                                    article.family_friendly, article.key_words,
                                    article.published_at, article.permanent,
                                    article.premium, article.description, 
                                    article.articleType, article.modified_at, 
                                    self.stored_at, publisher_id))
            last_id = cursor.execute("SELECT LAST_INSERT_ID() FROM `articles`")
        self.connection.commit()
        return last_id
    
    def addPublisher(self, publisher):
        if not self.connection:
            raise('No connection...')

        if not publisher:
            return None

        sql = "SELECT id from `publishers` where name = %s"
        sqlAdd = "INSERT INTO `publishers` (`type`, `name`) VALUES (%s, %s)"

        publisher_id = -1

        with self.connection.cursor() as cursor:
            cursor.execute(sql, (publisher.name))
            result = cursor.fetchone()
            if not result:
                cursor.execute(sqlAdd, (publisher.type, publisher.name))
                last_id = cursor.execute("SELECT LAST_INSERT_ID() FROM `publishers`")
                publisher_id = last_id
            else:
                publisher_id = result[0]
        self.connection.commit()
        return publisher_id

    def articleAlreadyStored(self, article):
        """ Check if an article is already stored

        Use `document_id` and `modified_at` for making a decision 
        
        Args:
            article (Article)
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM `articles` WHERE `document_id` = %s AND `modified_at` = %s"
                cursor.execute(sql, (article.id, article.modified_at))
                result = cursor.fetchone()[0]
            self.connection.commit()
            if result != 0:
                return True
            return False
        except:
            raise("No existing connection...")

    def addAuthors(self, authors):
        if not self.connection:
            raise('No connection...')

        type = authors['@type']
        authors = extractCleanedAuthors(authors['name'])
        sql = "SELECT id from `authors` where name = %s"
        sqlAdd = "INSERT INTO `authors` (`type`, `name`) VALUES (%s, %s)"

        author_ids = []
        for author in authors:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (author))
                result = cursor.fetchone()
                if not result:
                    cursor.execute(sqlAdd, (type, author))
                    last_id = cursor.execute("SELECT LAST_INSERT_ID() FROM `authors`")
                    author_ids.append(last_id)
                else:
                    author_ids.append(result[0])
            self.connection.commit()
        return author_ids