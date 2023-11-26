#!/usr/bin/env python
# coding: utf-8
import bs4
from bs4 import BeautifulSoup
import requests
import numpy as np
import AImodel as a
import pandas as pd
import joblib

def qasim(csv_input):
    l=[]
    for i,j in zip(csv_input['qBody'], csv_input['aBody']):
        i=str(i)
        j=str(j)
        soup = BeautifulSoup(i,"html.parser")
        ans=""
        ans1=""
        soup1 = BeautifulSoup(j,"html.parser")
        que=""
        que1=""
        qsim=0
        csim=0

        c_qtags=soup.findAll('pre')
        remove1=soup.findAll('a')
        c_atags=soup1.findAll('pre')
        remove2=soup1.findAll('a')
        for node in c_qtags:
            que1+=node.get_text()
            node.extract()
        for node in remove1:
            node.extract()
        que=soup.get_text()
        for node in c_atags:
            ans1+=node.get_text()
            node.extract()
        for node in remove2:
            node.extract()
        ans=soup1.get_text()
        qsim=a.get_cosine_sim([que,ans])
        csim=a.get_code_cosine_sim([que1,ans1])
        l.append([qsim,csim ])

    df = pd.DataFrame(l, columns = ['QAsim','QAcodesim'])
    csv_input['QAsim']=df['QAsim']
    csv_input['QAcodesim ']=df['QAcodesim']
    return csv_input

def aasim(csv_input):
    simt=[]
    simc=[]
    f=0
    text=[]
    code=[]
    anst=""
    ansc=""
    for j in csv_input['aBody']:
        f+=1
        j=str(j)
        soup = BeautifulSoup(j,"html.parser")
        to_remove = soup.find_all("pre") 
        to_remove1=soup.find_all("a")
        for node in to_remove:
            ansc+=node.get_text()
            node.extract()
        for node in to_remove1:
            node.extract()
        anst=soup.get_text()
        text.append(anst)
        code.append(ansc)
    for j in range(0,len(code)):
        sum1=0
        sum2=0
        for k in range(0,len(code)):
            if(j!=k and (text[j]!='' or text[k]!='')):
                sum1+=a.get_cosine_sim([text[j],text[k]])
            elif j!=k:
                sum1+=1
            if(j!=k and (code[j]!="" or code[k]!="")):
                sum2+=a.get_code_cosine_sim([code[j],code[k]])
            elif j!=k:
                sum2+=1
        simt.append(sum1/(len(code)-1))
        simc.append(sum2/(len(code)-1))
        
    df = pd.DataFrame(simt, columns = ['AAsim'])
    csv_input['AAsim']=df['AAsim']
    df = pd.DataFrame(simc, columns = ['AAcodesim'])
    csv_input['AAcodesim']=df['AAcodesim']
    csv_input=csv_input.drop(['qBody'],axis=1)
    return csv_input

def preprocess(csv_input):
    csv_input=qasim(csv_input)
    csv_input=aasim(csv_input)
    for i in csv_input.columns:
        if i!='aorder' and i!='aBody' and min(csv_input[i])!=max(csv_input[i]):
                csv_input[i]=(csv_input[i]-min(csv_input[i]))/(max(csv_input[i])-min(csv_input[i]))
    model = joblib.load('b.txt') 
    # Use the loaded model to make predictions
    answers=csv_input['aBody']
    csv_input=csv_input.drop(['aBody'],axis=1)
    csv_input=csv_input.iloc[:,:]
    res=model.predict(csv_input)
    prob=model.predict_proba(csv_input)
    probab=[]

    for i in range(0,len(res)):
        if res[i]==True:
            res[i]=1
        else:
            res[i]=0
        probab.append(max(prob[i]))
    if(sum(res)==0):
        return answers.loc[prob.find(min(prob))]
    elif(1 in res):
        max1=0
        c=0
        for i in range(0,len(res)):
            if res[i]==1 and probab[i]>max1:
                c=i
        return answers.loc[c]

def return_answer(data):
    
    soup = bs4.BeautifulSoup(data.text, "html.parser")
 
    name=soup.find('div', attrs={'id':'answers'})
    print(data)
    try:
        name2=name.find_all('div', attrs={'class':'user-info'})
    except:
        name2=name.find_all('div', attrs={'class':'user-info user-hover'})
    name3=name.find_all('div', attrs={'class':'js-vote-count flex--item d-flex fd-column ai-center fc-black-500 fs-title','itemprop':'upvoteCount'})
    #name3=name.find_all('div', attrs={'class':'js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center','itemprop':'upvoteCount'})
    name6 = soup.find('div', attrs={'id':'question'})
    name7 = name6.find('div', attrs={'class':'s-prose js-post-body'})
    name5=name.find_all('div', attrs={'class':'s-prose js-post-body','itemprop':'text'})
    name8= name.find_all( 'div', attrs={'class':'post-layout--right js-post-comments-component'})
    if(len(name5)==0):
        return "No related answer"
    if(len(name5)==1):
        return name5[0]
    reputation=[]
    votes=[]
    badges=[]
    upvotes_links = []
    upvotes=[]
    downvotes=[]
    answers=[]
    total_person_answered=[]
    time=[]
    commentcount=[]
    for i in range(len(name5)):
        total_person_answered.append(name5[i])                
    for i in name8:
        temp=len(i.find_all('li'))
        temp1=i.find('a',attrs={'title':'Expand to show all comments on this post'})
        if temp1!=None:
            m=temp1.find('b')
            if m!=None:
                temp+=int(m.get_text())
        commentcount.append(temp)
                    
    for i in name2:
        c = i.find('div', attrs={'class':'user-action-time'})
        q = c.find('a', attrs={'href':True})  
        if(q is not None):
            continue
        u = i.find('span', attrs={'title':True}) 
        t = i.find('span', attrs={'class':'reputation-score'})
        if(t is None):
            reputation.append(0)
        else:
            if(len(t['title'])>17):
                reputation.append(int(t['title'][17:].replace(',','')))
            else:
                reputation.append(int(t.get_text().replace(',','')))
        if(u is None):
            time.append("0")
        else:
            time.append(u['title'])
        
    for i in range(len(name3)):
        votes.append(int(name3[i].text))

    question=[name7]*len(votes)
    order=list(range(1,len(votes)))
    
    temp=time[:]
    time.sort()
    print(temp,votes,time)
    for i in range(0,len(time)):
        j=temp.index(time[i])
        a=temp[j]
        temp[j]=temp[i]
        temp[i]=a
        a=reputation[j]
        reputation[j]=reputation[i]
        reputation[i]=a
        a=total_person_answered[j]
        total_person_answered[j]=total_person_answered[i]
        total_person_answered[i]=a
        a=votes[j]
        votes[j]=votes[i]
        votes[i]=a
        a=commentcount[j]
        commentcount[j]=commentcount[i]
        commentcount[i]=a
    csv_input=pd.DataFrame(data=list(zip(reputation,order,votes,commentcount,total_person_answered,question)),columns=['Reputation','aorder','anewScore','anewCommentCount','aBody','qBody'])
    return preprocess(csv_input)

def stackoverflow(err):
    website = "stack overflow"
    url = "https://www.google.com/search?q="+err+website
    res = []
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, "html.parser")
    for links in soup.find_all("a"):
        link = links.get("href")
        if link[0:7]=="/url?q=":
            res.append(link[7:len(link)])
    main_link = res[0]
    #print(main_link)
    code = main_link[36:]
    q_code = ""
    #print(code)
    for i in  range(0, len(code)):
        if  code[i] == "/":
            break
        else:
            q_code = q_code + code[i]

    url = "https://stackoverflow.com/questions/" + q_code
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, "html.parser")
    name=soup.find('div', attrs={'class':'answer accepted-answer'})
    if(name!=None):
        return name.find('div', attrs={'class':'s-prose js-post-body'})
    else:
        return return_answer(data)

#stackoverflow('print multiple arguments in python')





