import nltk
import utility as util
from TweetClassifier import MultinomialNBTextClassifier
from utility import Timer

def example_tweets():
    """ Positive and negattive tweets"""
    pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]

    neg_tweets = [('I do not like this car', 'negative'),
              ('This view is horrrrrrrible', 'negative'),
              ('I feel tired this morning', 'negative'),
              ('I am not looking forward to the concert', 'negative'),
              ('He is my enemy', 'negative')]
    train_tweets = pos_tweets+neg_tweets
    
    test_tweets= ['I feel happy this morning', 'I do not like that man', 'My house is not great', 'Your song is annoying']
#    test_tweets = ['My house is not great']
    classifier = MultinomialNBTextClassifier(classes=['positive','negative'])
    with Timer() as t:
        classifier.train(train_tweets)
    print 'Elaspsed time for Training %s s'%t.secs
    print classifier.predict_doc(test_tweets, predict_log_p=False)
   
def main():
    example_tweets()
    
    
if __name__ == "__main__":
    main()