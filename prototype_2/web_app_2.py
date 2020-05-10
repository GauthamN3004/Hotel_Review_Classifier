from flask import Flask,redirect,render_template,request
import pickle
from nltk import sent_tokenize,word_tokenize
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings('ignore')
import re

app = Flask(__name__)

opposites = pickle.load(open("opposites.pkl","rb"))
opposites['great'] = 'ok'
contractions = pickle.load(open("contractions.pkl","rb"))
cv = pickle.load(open("count_vectorizer.sav","rb"))
mnb = pickle.load(open("classifier.sav","rb"))
opp_keys = list(opposites.keys())
con_keys = list(contractions.keys())


def handle_contractions(review):
    words = review.lower().split()
    for i in range(len(words)):
        if(words[i] in con_keys):
            words[i] = contractions[words[i]]
    sentence = " ".join(words)
    return sentence


def handle_negation(review):
    review = review.lower()
    review = handle_contractions(review)
    review = sent_tokenize(review)
    final_sent=""
    for sent in review:
        words = word_tokenize(sent)
        words = [x for x in words if x!='the']
        tags = nltk.pos_tag(words)
        i = 0
        while(i<len(words)):
            if(tags[i][0]=="not"):
                for j in range(i+1,len(tags)):
                    if(j>=len(words)):
                        i+=1
                        break
                    if(tags[j][1]=='JJ'):
                        if((tags[j][0] in opp_keys) and (opposites[tags[j][0]]!=None)):
                            words[j] = opposites[tags[j][0]]
                            print(" ".join(words))
                            try:
                                del(words[i])
                                del(tags[i])
                            except:
                                continue
                            break
                        else:
                            i+=1
                            break
                    else:
                        i+=1
                        continue
            else:
                i=i+1
        final_sent+=" ".join(words)
    return final_sent

def review_prepare(review):
    ps=PorterStemmer()
    review = handle_negation(review)
    review = re.sub('[^a-z]',' ',review)
    review = word_tokenize(review)
    stop_words = stopwords.words("english")
    stop_words.remove("not")
    stop_words.extend(["food","hotel","room"])
    review = [ps.stem(word) for word in review if word not in stop_words]
    review = ' '.join(review)
    return review

def predict(review):
    review = review_prepare(review)
    review  = cv.transform([review])
    ypred = mnb.predict(review)
    return ypred[0]

@app.route("/",methods = ['POST','GET'])
def home():
    if request.method == "POST":
        rev = request.form["text"]
        review = request.form["text"]
        if(len(review) < 10):
            return render_template("index_2.html", review = "len_issue",text = rev)
        else:
            ypred = predict(review)
            if(ypred == 0):
                return render_template("index_2.html", review = "negative",text = rev)
            else:
                return render_template("index_2.html", review="positive",text = rev)
    return render_template("index_2.html", review="no review",text = " ")



if __name__ == "__main__":
    app.debug = True
    app.run()