from django.shortcuts import render
import nltk
import re

from nltk.corpus import stopwords
stop = stopwords.words('english')

from nltk.stem import WordNetLemmatizer
wn = WordNetLemmatizer()

import pickle
import os
from django.conf import settings

model_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'Naive_model.pkl')
vector_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'vectorizer.pkl')

print(model_path)

model = pickle.load(open(model_path, 'rb'))
vector = pickle.load(open(vector_path, 'rb'))


def decontracted(st):
    st = re.sub(r"won\'t", "will not", st)
    st = re.sub(r"can\'t", "can not", st)

    st = re.sub(r"n\'t", " not", st)
    st = re.sub(r"\'re", " are", st)
    st = re.sub(r"\'s", " is", st)
    st = re.sub(r"\'d", " would", st)
    st = re.sub(r"\'ll", " will", st)
    st = re.sub(r"\'ve", " have", st)
    st = re.sub(r"\'m", " am", st)
    return st
def clear_punctuation(st):
    word = re.sub(r'[^\w\s]', '',st)

    return word
def clear_noise(word):
    word = word.lower()         
    word = decontracted(word)
    word = clear_punctuation(word)
    return word

def clear_stopwords(st):
    word = " ".join(st for st in st.split() if st not in stop)
    return word

def fun_stemlem(word):
    list_word_clean = []
    for w1 in word.split(" "):
        word_lemma =  wn.lemmatize(w1,  pos="v")
        list_word_clean.append(word_lemma)

  #Cleaning, lowering and remove whitespaces
    word = " ".join(list_word_clean)
    return word 

def prepare_data(word):
    word = clear_noise(word)       
    word = clear_stopwords(word)    
    word = fun_stemlem(word)        
    return word


def check_spam(request):
    result = None
    email_text = ""

    if request.method == "POST":
        email_text = request.POST.get('email', '')

        if email_text:
  
            email_processed = prepare_data(email_text) 
            email_vectorized = vector.transform([email_processed])  
            
            # Dự đoán
            prediction = model.predict(email_vectorized)
            result = "Spam" if prediction == 1 else "Not Spam"

    return render(request, 'index.html', {'result': result, 'email_text': email_text})
