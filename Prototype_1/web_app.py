from flask import Flask,redirect,render_template,request
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

app = Flask(__name__)

@app.route("/",methods = ['POST','GET'])
def home():
    if request.method == "POST":
        ps = PorterStemmer()
        review = request.form["text"]
        if(len(review) < 10):
            return render_template("index.html", review = "len_issue")
        else:
            cleaned = []
            review = review.lower()
            review = re.sub('[^a-z]', ' ', review)
            review = review.split()
            review = [ps.stem(word) for word in review if word not in stopwords.words("english")]
            review = ' '.join(review)
            cleaned.append(review)
            cv = pickle.load(open("preprocessor.sav","rb"))
            classifier = pickle.load(open("review_classifier.sav","rb"))
            xtest = cv.transform(cleaned)
            ypred = classifier.predict(xtest)
            if(ypred[0] == 0):
                return render_template("index.html", review = "negative")
            else:
                return render_template("index.html", review="positive")
    return render_template("index.html", review="no review")



if __name__ == "__main__":
    app.debug = True
    app.run()