TwitterAnalysis
===============
-----------------------
CREATING SQL DATABASE
-----------------------
1. Change line 
	db_con = MySQLdb.Connect(<hostname-typically localhost>, <user-typically root>, <password>, 'tweets')
2. Run sqlscript.py
This will create a database tweets with different tables

-----------------------
CREATING STOP WORDS
-----------------------
1. utility/create_stop_words.py is run stand alone to generate stop words using idf
2. This script has the training dataset hard coded. Can be changed for a new dataset
3. Produces file Lists/StopWordsIDF.txt (don't have to recreate if it exists)
 
-----------------------
RUNNING THE CODE
-----------------------
1. Change collector.config. Query terms are also given in this file. Currently query has to be done manually
by running Collector.py

-----------------------
TO DO
-----------------------
1. Stemming
2. Pivoting
3. Bi-grams
4. Confidence of prediction
5. Neutral class
6. Max entropy classifier
7. MI of feature (and feature selection based on this)