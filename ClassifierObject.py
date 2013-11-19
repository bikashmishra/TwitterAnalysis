from TweetClassifier import MultinomialNBTextClassifier

def classify(train_tweets, test_tweets):
    classifier = MultinomialNBTextClassifier(classes=['positive','negative'])
    classifier.train(train_tweets)
    print classifier.predict_doc(test_tweets, predict_log_p=True)
        