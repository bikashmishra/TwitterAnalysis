import math

def tfidf(word, tweet, alltweets):
    return tf(word,tweet)*idf(word,alltweets)
    
def tf(word, tweet,log=False):
    freq = tweet.split().count(word)
    totalwordcount = len(tweet.split())
    if not log:
        vtf = freq/float(totalwordcount)
    else:
        vtf = log(freq/float(totalwordcount)+1)
    return vtf

def idf(word,alltweets):
    return math.log(len(alltweets)/numTweetsContainingWord(word,alltweets))

def numTweetsContainingWord(word,alltweets):
    count = 0
    for tweet in alltweets:
        if word in tweet.split():
            count += 1
    return count
    
