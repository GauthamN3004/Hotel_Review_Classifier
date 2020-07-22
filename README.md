# Hotel_Review_Classifier
a text classifier that computationally identifies and categorizes opinions (sentiment analysis) expressed in a hotel review. It classifies the review as a positive review or a 
negative review.

### Requirements
* pandas
```
pip install pandas
```
* nltk
```
pip install nltk
```
* flask
```
pip install flask
```
* pickle
```
pip install pickle
```
* sklearn
```
pip install sklearn
```

### How it works
The first step is to build a classification model. We need to first prepare the review by eliminating punctuation marks, redundant spaces, etc.
Then we have to remove the stopwords (stop words are words which are filtered out before or after processing of natural language data. Some examples of stop words are: "a," "and," "but," "how," "or," and "what.")
Once the stopwords are eliminated, we take the root word for each word (for eg. root word of "amazing" is "amaze"). Now our text cleaning process is complete.

The next step is to create a matrix of all words (or the top N words if the number of words is too large). CountVectorizer is used for this purpose. Once we have the matrix
all that's left to do is train the classification model.

Now for every review that should be tested, the above cleaning process should be done and converted into a matrix. Then use the classification model to predict the sentiment of the result.

One challenge that you may face is **handling contractions** and **negations** like "food was not good" and "food wasn't good". 
To handle such sentences, a dictionary of contractions is provided in the program which can be used to convert contractions such as "wasn't" to "was not".
Now to handle the negation, the first adjective after the negating word "not" can be replaced with its synonym, and the word "not" can be removed.
So a review like "food was not good" will become "food was bad". The latter sentence is classified accurately.
