import nltk

def create_words(alltweets):
    """ 
    Takes a list of tuples of (tweet_string, label)
    and returns a tuple of (wordlist, label)
    All words of length < 3 are discarded
    """
    tweets = []
    for (tweet_words,sentiment) in alltweets:
        # only words with length greater than 2
        words = [w.lower() for w in tweet_words.split() if len(w)>=3]
        tweets.append((words,sentiment)) # tuple of (list,label_string)
    return tweets

def get_all_words(tweets):
    all_words = []
    for (w, s) in tweets:
        all_words.extend(w)
    return all_words

def get_freq_dist(word_list):
    word_list = nltk.FreqDist(word_list)
    return word_list