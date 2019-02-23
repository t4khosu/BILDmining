dropTablesSQL = """
    DROP TABLE IF EXISTS articles_authors
    DROP TABLE IF EXISTS articles
    DROP TABLE IF EXISTS publishers
    DROP TABLE IF EXISTS authors
"""

createTablesSQL = """
    CREATE TABLE authors (
        id INT NOT NULL AUTO_INCREMENT,
        type VARCHAR(255),
        name VARCHAR(255),
        PRIMARY KEY (id)
    )

    CREATE TABLE publishers (
        id INT NOT NULL AUTO_INCREMENT,
        type VARCHAR(255),
        name VARCHAR(255),    
        PRIMARY KEY (id)
    )

    CREATE TABLE articles (
        id INT NOT NULL AUTO_INCREMENT,
        document_id INT NOT NULL,
        article_type VARCHAR(255),
        article_url TEXT,
        headline TEXT,
        description TEXT,
        content MEDIUMTEXT,
        key_words TEXT,
        published_at TIMESTAMP,
        modified_at TIMESTAMP NOT NULL,
        publisher_id INT,
        family_friendly TINYINT(1),
        permanent TINYINT(1),
        premium TINYINT(1),
        stored_at TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (publisher_id) REFERENCES publishers(id)
    )

    CREATE TABLE articles_authors (
        id INT NOT NULL AUTO_INCREMENT,
        author_id INT NOT NULL,
        article_id INT NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (author_id) REFERENCES authors(id),
        FOREIGN KEY (article_id) REFERENCES articles(id)
    )
"""

def initTables(DB):
    """ Remove old tables (if exists) and create new ones """
    DB.runSqlFromString(dropTablesSQL, ())
    DB.runSqlFromString(createTablesSQL, ())
    print("New Tables initialized...")