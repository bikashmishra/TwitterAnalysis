import tfidf
import utility as util
import re
import numpy as np
import pandas as pd

def idf_stop_words():
    df2 = pd.io.parsers.read_csv('../TrainingData/Sentiment_Analysis_Dataset.csv', header=0, delimiter='\t', nrows=10000)

    sentiment = {0:'negative', 1:'positive'}
    alltweets = []
    for idx, row in df2.iterrows():
        alltweets.append(((row['SentimentText'],sentiment[row['Sentiment']])))
        
    stop_words = []
    cleantweets = []
    tweet_features = []
    for (tweet,sentiment) in alltweets:
        tweet = util.preprocess(tweet)
        cleantweets.append(tweet)
        words = [w for w in tweet.split() if (len(w)>=3 and re.search(r'^[a-zA-Z][a-zA-Z0-9]*$',w))]
        tweet_features.append((words,sentiment)) # tuple of (list,label_string)
    all_words = util.get_all_words(tweet_features)
    word_idf = {}
    for word in all_words:
        word_idf[word]=tfidf.idf(word,cleantweets)
    sorted_idf = [k for v,k in sorted([(v,k) for k,v in word_idf.items()], reverse=False)]
    nstopwords= int(np.ceil(0.75*(len(sorted_idf))))
    f = open('../Lists/StopWordsIDF.txt','w')
    for w in sorted_idf[int(np.ceil(0.5*nstopwords)):nstopwords]:
        f.write('%s \n'%w)
    f.close()

if __name__ == "__main__":
    with util.Timer() as t:
        idf_stop_words()
    print 'Elaspsed time for creating stop words %s s'%t.secs
