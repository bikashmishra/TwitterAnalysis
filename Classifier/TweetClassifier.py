import numpy as np
from scipy import misc, sparse
from itertools import izip
import abc
import utility as util
from sklearn import metrics
import re

class BaseNaiveBayes():
    """ 
    Base class for Naive Bayes classfier
    Used by Discrete Naive Bayes for text processing 
    """
    __metaclass__ = abc.ABCMeta
     
    @abc.abstractmethod
    def log_likelihood(self, X):
        """
        Input:
            X: array_like [nexamples] x [nfeatures]
            output: array_like [nexamples] x [nlabels]
        """
    def predict(self,X):
        """
        Input:
            X: array_like [nexamples] x [nfeatures]
        Output:
            array_like [nexamples] with entry being label
        """
        class_prob = self.log_likelihood(X)
        #print class_prob
        return [self.classes_[i] for i in np.argmax(class_prob, axis=1)]
        
    def predict_logprob(self, X):
        """
        Input:
            X: array_like [nexamples] x [nfeatures]
        Output:
            array_like [nexamples] x [nclasses]
        """    
        """ Calculate p(f1,f2,..,fn)"""
        class_prob = self.log_likelihood(X)
        log_total_prob = misc.logsumexp(class_prob, axis=1)
        probarraylist= [class_prob[i] - log_total_prob[i] for i in range(log_total_prob.shape[0])]
        return np.asarray(probarraylist)
    
class MultinomialNBTextClassifier(BaseNaiveBayes):
    """
    This classifier takes in tweets in the form
    (tweet,label). Label eg: positive, negative, neutral - sentimentt
    The classifier can be trained in parts
    Hence, all the classes need to be known apriori
    """
    
    def __init__(self, classes, alpha=1.0):
        """ 
        alpha is the smoothing value
        classes is of type array_like
        """
        self.alpha_ = alpha
        self.classes_ = classes
        self.class_counts_ = self.alpha_*np.ones(len(self.classes_))
        self.features_ = []

    def add_feature(self, f):
        self.features_.append(f)
    
    def train(self, tweets):
        """ BEGIN TWEET PREPROCESS"""
        #--------------------------------------------------------------------------
        """ tweets is transformed in to a tuple of (word_list, sentiment)  """
        tweets = util.create_features(tweets)
        
        all_words = util.get_all_words(tweets)
        
        """ END TWEET PREPROCESS"""
        #--------------------------------------------------------------------------
        freq_dist = util.get_freq_dist(all_words)
        self.features_ = freq_dist.keys()
        
        labels = []
        for w,s in tweets:
            labels.append(s) 
#        self.feature_counts_ = sparse.csr_matrix((nclasses, nfeatures), dtype=np.float)
        nfeatures = len(self.features_)
        nclasses = len(self.classes_)
 #       feature_counts = sparse.lil_matrix((nclasses, nfeatures), dtype=np.float)
        self.feature_counts_ = np.zeros((nclasses, nfeatures), dtype=np.float)
                            
        self.count_class(labels)
        self.update_class_log_prior(self.class_counts_)

        self.count_feature(tweets)
        self.update_feature_prob(self.feature_counts_)
        
    def count_class(self, labels):
      #  class_list = self.classes_.tolist()
        for c in labels:
            self.class_counts_[self.classes_.index(c)] += 1
        
    def update_class_log_prior(self, class_count=None):
        if class_count is not None:
            self.class_log_prior_ = np.log(class_count) - np.log(sum(class_count))
             
    def count_feature(self, tweets):
        for entry, c in tweets:
            class_index = self.classes_.index(c)
            for f in entry:
                self.feature_counts_[class_index][ self.features_.index(f)] += 1
                
 #       self.feature_counts_ = feature_counts.tocsr()
                
    def update_feature_prob(self, feature_count=None):
        """ feature_count is of type csr"""
        feature_count_smooth = feature_count + self.alpha_
        class_count_smooth = feature_count_smooth.sum(axis=1)
        self.feature_log_likelihood_ = np.log(feature_count_smooth) - np.log(class_count_smooth.reshape(-1,1))
        
    def log_likelihood(self, X):
        """
        Input:
            X: array_like or sparse matrix [nexamples] x [nfeatures]
            output: array_like [nexamples] x [nlabels]
        """
        _,nfeatures = X.shape
        
        if nfeatures != len(self.features_):
            raise ValueError("Expecting input with %d features" % len(self.features_))
        out = (X*self.feature_log_likelihood_.T + self.class_log_prior_)
        return out
    
    def predict_tweets(self, docs, predict_log_p=False):
        """ 
        Take in a list of docs and cerate a feature array
        of size [nexamples]x[nfeatures]. This can be a sparse matrix
        This matrix/array is then sent to predict and log_likelihood
        """
        nfeatures = len(self.features_)
        nexamples = len(docs)
        X = sparse.lil_matrix((nexamples,nfeatures), dtype=np.float)
        
        stop_words = util.getStopWords()

        iexample = -1
        for tweet in docs:
            iexample += 1
            tweet = util.preprocess(tweet)
            words = [w for w in tweet.split() if (len(w)>=3 and w not in stop_words
                                               and re.search(r'^[a-zA-Z][a-zA-Z0-9]*$',w))]
            for f in words:
                if f in self.features_:
                    X[iexample,self.features_.index(f)] += 1
                
        if not predict_log_p:
            return self.predict(X)
        else:
            return self.predict_logprob(X)
        
    def accuracy(self,tweets):
        """This function takes in tweets as tuples in the form(tweet,label)"""
        test_tweets = []
        test_sentiments = []
        for (t,s) in tweets:
            test_tweets.append(t)
            test_sentiments.append(s) 
        predicted_sentiment = self.predict_tweets(test_tweets, predict_log_p=False)
        score = metrics.accuracy_score(test_sentiments, predicted_sentiment)
        return score
        
    def top_features(self,n=None):
        if not n:
            n = len(self.features_)
        for c in range(len(self.classes_)):
            top_features = dict(zip(self.features_,self.feature_log_likelihood_[c]))
            print 'Top features for class %s :'%self.classes_[c]
            sorted_features = [(k,v) for v,k in sorted([(v,k) for k,v in top_features.items()], reverse=True)]
            for i in range(n):
                print '%s'%(sorted_features[i][0],)
            print '\n'
            
    def add_stop_words(self):
        pass
    
    def number_of_features(self):
        return len(self.features_)
        