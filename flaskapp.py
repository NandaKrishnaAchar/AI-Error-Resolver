
import bs4
import requests
from flask import Flask, request, jsonify
import json
import Script as s
import dbConnect as db

app = Flask(__name__)

def module_error(err):
    url = "https://pypi.org/search/?q=" + err
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, "html.parser")
    name=soup.find('div', attrs={'class':'left-layout__main'})
    sol = name.find('h3', attrs={'class':'package-snippet__title'})

    sol2 = name.find('span', attrs={'class':'package-snippet__name'})
    key = str(sol2.text)
    
    url = "https://pypi.org/project/" + key
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, "html.parser")
    name=soup.find('div', attrs={'class':'banner'})
    sol = name.find("span")
    answer=[]
    answer.append(sol.text)
    answer.append('2')
    
    return answer 
    
    
def stackoverflow(err):
   
    error_parameter = err.split(":",1)
    if(len(error_parameter)>1):
        ans = db.search(error_parameter[0],error_parameter[1])
    else:
        ans = db.search('',error_parameter[0])
    if(ans==[]):
        name2=s.stackoverflow(err)
        text=[]
        solution=[]
        
        for txt in name2.find_all("p"):
            text.append(txt.text)
        
        for pre in name2.find_all("pre"):
            for code in pre.find_all("code"):
                solution.append(code.text)
        
        ans= str(name2)
        print(ans)
        length = len(ans)

        answer_list = []
        
        for i in range(length):
            if(ans[i]=="<"):
                if(ans[i+1]=="p"):
                    if(ans[i+2]==">"):
                        p=text.pop(0)
                        answer_list.append(p)
                        answer_list.append('1')
                    if(ans[i+2]=="r"):
                        p=solution.pop(0)
                        answer_list.append(p)
                        answer_list.append('0')

        if(len(error_parameter)>1):
            if(not db.insert(error_parameter[0],error_parameter[1],json.dumps(answer_list))):
                return "Insertion Error! Try After sometime"
        else:
            if(not db.insert('',error_parameter[0],json.dumps(answer_list))):
                return "Insertion Error! Try After sometime"
    else:
        answer_list = json.loads(ans[0][0])
    
    return answer_list

@app.route('/test',methods = ['GET'])
def test():
     return "Hello"


@app.route('/module_error/<error>',methods = ['GET'] )
def ModuleError(error):
    return jsonify({'data':module_error(error)})

@app.route('/stackoverflow_error/<error>',methods = ['GET'])
def StackOverflow_Flask(error):
    return jsonify({'data':stackoverflow(error)})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)





