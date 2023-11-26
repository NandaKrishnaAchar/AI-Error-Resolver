from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
import pandas as pd
import tokenize
import io
import nltk 
import re
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet 
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize 
import joblib    

stop_words = set(stopwords.words('english'))

lemmatizer = WordNetLemmatizer() 
     
def get_cosine_sim(strs):
    vectors = [t for t in get_vectors(strs)]
    k=cosine_similarity(vectors)
    return k[0][1]
     
def pos_tagger(nltk_tag): 
    if nltk_tag.startswith('J'): 
        return wordnet.ADJ 
    elif nltk_tag.startswith('V'): 
        return wordnet.VERB 
    elif nltk_tag.startswith('N'): 
        return wordnet.NOUN 
    elif nltk_tag.startswith('R'): 
        return wordnet.ADV 
    else:
        return None

def lemmatize_sentence(sentence): 
    tokens=[w for w in nltk.word_tokenize(sentence)]
    word=[]
    for i in tokens:
        if i not in stop_words:
            word.append(i)
    pos_tagged = nltk.pos_tag(word) 
    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged)) 
    result = [] 
    for word, tag in wordnet_tagged: 
        if tag is None: 
            continue
        else: 
            result.append(lemmatizer.lemmatize(word, tag)) 
    return result

def get_vectors(strs):
    text = [t for t in strs]
    try:
        vectorizer = CountVectorizer(tokenizer=lemmatize_sentence)
        k=vectorizer.fit_transform(text).toarray()
    except:
         return [[1,1],[1,1]]
    return k
 
def get_code_cosine_sim(strs):
    temp=strs[:]
    n=len(strs)
    #55 - comment
    stops=[55,4,0]
    d=dict()
    k=[]
    try:
        for i in temp:
             for token in tokenize.generate_tokens(io.StringIO(i).readline):
                if token.type not in stops and not(token.type== 3 and (token.string.startswith('"""') or token.string.startswith("'''"))):
                    space=token.string.replace(' ','')
                    if(len(space)==0):
                        continue
                    index=token.string.find('\n')
                    index1=token.string.find('\r')
                    if(index==-1 and index1==-1):
                        k.append(token.string)
                    elif(index>0 and index1==-1):
                        if(token.string[index-1]=='\''):
                            k.append(token.string)
                    elif(index1==-1 and index1>0):
                        if(token.string[index1-1]=='\''):
                            k.append(token.string)
                    elif(index1>0 and index>0):
                        k.append(token.string)
                        
        for j in k:
            d[j]=[0]*n
        count=0
        for i in temp:
            for token in tokenize.generate_tokens(io.StringIO(i).readline):
                if token.string in k:
                    d[token.string][count]+=1
            count+=1
        a=[]
        b=[]
        for key, val in d.items():
                 a.append(val[0])
                 b.append(val[1])
        vectors=[]
        vectors.append(a)
        vectors.append(b)
        try:
            k=cosine_similarity(vectors)
            return k[0][1]
        except:
            #no code segment
            return 1
    except:
        vectorizer = CountVectorizer(tokenizer=word_tokenize)
        vectors=vectorizer.fit_transform(temp).toarray()
        k=cosine_similarity(vectors)
        return k[0][1]
        
