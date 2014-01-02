import nltk
import utility as util
from TweetClassifier import MultinomialNBTextClassifier
from utility import Timer
import pandas as pd
import numpy as np
from math import ceil

def getClassifier():
    # 1. Training set 2 - Sentiment tweets from 
    # http://thinknook.com/twitter-sentiment-analysis-training-corpus-dataset-2012-09-22/    
    # Only positive and negative tweets are used
    # This set has ~1million tweets. Only 1000 are used initially for POC
    df2 = pd.io.parsers.read_csv('../TrainingData/Sentiment_Analysis_Dataset.csv', header=0, delimiter='\t', nrows=100)

    sentiment = {0:'negative', 1:'positive'}
    tweets = []
    for idx, row in df2.iterrows():
        tweets.append(((row['SentimentText'],sentiment[row['Sentiment']])))
        
    classifier = MultinomialNBTextClassifier(classes=['negative','positive'])
    with Timer() as t:
        num_train = int(len(tweets))
        num_test = len(tweets)-num_train
        classifier.train(tweets[:num_train])
    print 'Elaspsed time for Training %s s'%t.secs
    return classifier