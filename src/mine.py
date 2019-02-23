import json, argparse, sys
from components.ArticleCollector import ArticleCollector
from components.DatabaseManager import DatabaseManager
from sql.initSQL import *
import datetime

actual_time = datetime.datetime.now()

with open("parameters.json") as fIn:
	    parameters = json.load(fIn)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect articles from bild.de')
    parser.add_argument('-n', '--new', dest='new', action='store_true', help='Drop existing tables and create new ones')
    parser.add_argument('-l', '--light', dest='light', action='store_true', help='Only look for new articles. Don\'t check for updated ones!')
    args = parser.parse_args()

    # Connect to DB
    db = DatabaseManager(parameters, actual_time)
    db.startConnection()

    # Drop tables and create new ones, if parameter is set
    if args.new:
        initTables(db)

    # Extract articles and fill tables
    articleCollector = ArticleCollector(parameters, db)
    articles_collected = articleCollector.collectArticles(light=args.light)

    # Print results
    print("Articles found: {}".format(articles_collected["found"]))
    print("Articles stored: {}".format(articles_collected["stored"]))

    # Close connection
    db.closeConnection()