import pickle
import numpy as np
import re
import pandas as pd
from nltk.corpus import stopwords
import numpy as np
import sklearn
import nltk
from sklearn.naive_bayes import MultinomialNB
import warnings
warnings.filterwarnings('ignore')
from lime import lime_text
from sklearn.pipeline import make_pipeline
from lime.lime_text import LimeTextExplainer
from nltk.stem import PorterStemmer, WordNetLemmatizer
import datetime as datetime
import os 
lemmetizer = WordNetLemmatizer()
stemmer = PorterStemmer()

class_names = np.asarray([u'ARTS', u'ARTS & CULTURE', u'BLACK VOICES', u'BUSINESS', u'COLLEGE',
 u'COMEDY', u'CRIME', u'EDUCATION', u'ENTERTAINMENT', u'FIFTY', u'GOOD NEWS',
 u'GREEN', u'HEALTHY LIVING', u'IMPACT', u'LATINO VOICES', u'MEDIA', u'PARENTS',
 u'POLITICS', u'QUEER VOICES', u'RELIGION', u'SCIENCE', u'SPORTS', u'STYLE',
 u'TASTE', u'TECH', u'THE WORLDPOST', u'TRAVEL', u'WEIRD NEWS', u'WOMEN', u'WORLD NEWS', u'WORLDPOST'])

model_filename = 'interests_classifier.sav'
vect_filename = 'vectorize_interests_classifier.sav'
input_val = np.asarray([u"Cricket is a beatiful sport. Baseball, hockey. Dhoni is the best!!!",
       u'Jenna Amatulli'])

def load_models(model_filename, vect_filename):    
    pwd = os.getcwd()
    if pwd.find('model') < 0:
    	model_filename = "{}/models/{}" .format(pwd, model_filename)
    	vect_filename = "{}/models/{}" .format(pwd, vect_filename)

    loaded_model = pickle.load(open(model_filename, 'rb'))
    vectorize = pickle.load(open(vect_filename, 'rb'))
    return loaded_model, vectorize


def get_words(headlines_list):
    headlines = headlines_list[0]   
    author_names = [x for x in headlines_list[1].lower().replace('and',',').replace(' ', '').split(',') if x != '']
    headlines_only_letters = re.sub('[^a-zA-Z]', ' ', headlines)
    words = nltk.word_tokenize(headlines_only_letters.lower())
    stops = set(stopwords.words('english'))
    meaningful_words = [lemmetizer.lemmatize(w) for w in words if w not in stops]
    return ' '.join(meaningful_words + author_names)


def clean_input_and_vectorize(input_val, vectorize):
    cleanHeadlines_list = []
    cleanHeadline = get_words(input_val) #Processing the data and getting words with no special characters, numbers or html tags
    cleanHeadlines_list.append( cleanHeadline )
    tfidwords_input = vectorize.transform(cleanHeadlines_list)
    return tfidwords_input, cleanHeadlines_list


def predict(tfidwords_input, loaded_model):
    return loaded_model.predict(tfidwords_input)[0]


def get_explainer(class_names, loaded_model, vectorize, cleanHeadlines_list, tfidwords_input):
    explainer = LimeTextExplainer(class_names=class_names)
    c = make_pipeline(vectorize, loaded_model)
    exp = explainer.explain_instance(cleanHeadlines_list[0], c.predict_proba, labels=range(class_names.shape[0]))
    return exp


def explain_all(exp, class_names):
    print 'Predicted class =', loaded_model.predict(tfidwords_input_test).reshape(1,-1)[0,0]
    for i in range(class_names.shape[0]):
        try:
            print("i: {}".format(class_names[i]))
            print ('\n'.join(map(str, exp.as_list(label=i))))
        except:
            print("Error for {}".format(i))


def get_class_name_index(class_names, class_name):
    return list(class_names).index(class_name)


def explain_class(exp, idx):
    try:
        return exp.as_list(label=idx)
    except:
        print("Error for {}".format(i))
        return None

def get_interests(input_val):
	input_val = np.asarray(input_val)
	loaded_model, vectorize = load_models(model_filename, vect_filename)
	tfidwords_input, cleanHeadlines_list = clean_input_and_vectorize(input_val, vectorize)
	pred_category = predict(tfidwords_input, loaded_model)
	exp = get_explainer(class_names, loaded_model, vectorize, cleanHeadlines_list, tfidwords_input)
	idx = get_class_name_index(class_names, pred_category)
	# all_explainers = explain_all(exp, class_names)
	explainer = explain_class(exp, idx)
	return pred_category, explainer

if __name__ == '__main__':
	input_val = [u"Cricket is a beatiful sport. Baseball, hockey. Dhoni is the best!!!", u'steve']
	print(get_interests(input_val))
