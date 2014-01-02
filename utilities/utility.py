import nltk
import re
import time
import tfidf
import numpy as np

def preprocess(tweet):
    """ remove punctuations has to be last to take care or URL and @ and # properly"""
    return removePunctuation(removeHashtag
                             (replaceRepitions
                              (replaceUsername
                               (replaceURL
                                (lowercase(tweet))))))
            
def lowercase(tweet):
    return tweet.lower()

def replaceURL(tweet):
    """ finds www.*, http://*, https://* and replaces with URL"""
    return re.sub(r'(www\.[^\s]+)|(https?://[^\s]+)','URL', tweet)

def replaceUsername(tweet):
    """ finds @username and replaces with AT_USER"""
    return re.sub(r'@[^\s]+','AT_USER',tweet)

def removeHashtag(tweet):
    """ finds #something and replaces with something"""
#     return re.sub(r'#([^\s]+)', r'\1', tweet)
    return re.sub(r'#([^\s]+)', r'', tweet)
            
def removePunctuation(tweet):
    return re.sub(r'[\'"!?,.$~:)(*+-]','',tweet)

def getStopWords():
    stopwordpaths = ['../Lists/StopWordsIDF.txt', '../Lists/StopWords2.txt']
    stop_words = []
    for stopwordpath in stopwordpaths:
        f = open(stopwordpath)
        for w in f.read().split():
            stop_words.append(w)

    stop_words.append('URL')
    stop_words.append('AT_USER')
    stop_words.append('RT')
    stop_words.append('twitter')
    return stop_words

def replaceRepitions(tweet):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", tweet)

def create_features(alltweets):
    """ 
    Takes a list of tuples of (tweet_string, label)
    and returns a tuple of (wordlist, label)
    All words of length < 3 are discarded
    """
    tweet_features = []
    stop_words = getStopWords()
    for (tweet,sentiment) in alltweets:
        tweet = preprocess(tweet)
        # only words with length greater than 2
        # words not in stop words
        # words starting with a alphabet not number
        words = [w for w in tweet.split() if (len(w)>=3 and w not in stop_words
                                               and re.search(r'^[a-zA-Z][a-zA-Z0-9]*$',w))]
        tweet_features.append((words,sentiment)) # tuple of (list,label_string)
    return tweet_features

def get_all_words(tweets):
    all_words = []
    for (w, s) in tweets:
        all_words.extend(w)
    return all_words

def get_freq_dist(word_list):
    word_list = nltk.FreqDist(word_list)
    return word_list


class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs
            
if __name__ == "__main__":
    getStopWords()
    
# if __name__ == "__main__":
#     tweet = 'Do loweR! _Case$ "woohoo" !!!http://www.giveup.cm/?query written by @bmishra @someone #checkingcode #metoo'
#     print preprocess(tweet) 