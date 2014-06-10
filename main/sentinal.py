#This is the main file to do things step by step
import dotraining
import argparse
import pandas as pd
import MySQLdb
from TweetClassifier import MultinomialNBTextClassifier
from utility import Timer
import matplotlib.pyplot as plt

def sentinal():
    """Step 1. Parse query argument """
    parser = argparse.ArgumentParser(description='Get input arguments')
    parser.add_argument('-q', nargs='*', type=str, )
    args = parser.parse_args()
    list_querystrings = args.q
    #print list_querystrings
    
    """Step 2. Search/Stream data from twitter for this query into SQL database """
    # currently done manually since we only have streaming function which has to be stopped manually
    # Change collector.config. Query terms are also given in this file. Currently query has to be done manually
    # by running Collector.py

    """Step 3. Get data from SQl into a data frame """
    db_con = MySQLdb.Connect('localhost', 'root', 'password1234', 'tweets')
    sql = "SELECT * FROM tweets"
    tweets_df = pd.io.sql.read_frame(sql, db_con)
    
    """Step 4. Train and get back a classifier """
    classifier = dotraining.getClassifier()
    
    """Step 5. Do analysis using the classifier """
    tweets = [ t for t in tweets_df['tweet_text'] ]
    with Timer() as t:
        pred_sentiment = classifier.predict_tweets(tweets, predict_log_p=False)
    print 'Elaspsed time for Predicting %s s'%t.secs
    
    groupedbydate = tweets_df.groupby('created_at').count()
    plt.figure()
    ts = groupedbydate['created_at']
    ts2 = ts.groupby(ts.index.date).count()
    ts3 = pd.TimeSeries(randn())
    ts2.plot()
    plt.show()

    
    """Step 7. Clear SQL database of the query """
    

if __name__ == "__main__":
    sentinal()