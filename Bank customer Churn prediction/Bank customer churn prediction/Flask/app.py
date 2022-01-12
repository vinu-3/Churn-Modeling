# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 16:11:18 2022

@author: Vinu Abinayaa
"""


import numpy as np
from flask import Flask, request,jsonify,render_template
import requests

import json
API_KEY = "QN45BrPwmUWbPT0dPGYKk6761QcooinTgfBQVzJjFGzD"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/y_predict',methods=["POST"])
def y_predict():
    geography=request.form["geography"]
    gender=request.form["gender"]
    age=request.form["age"]
    tenure=request.form["tenure"]
    creditscore=request.form["creditscore"]
    
    balance=request.form["balance"]
    noof=request.form["no of"]
    hascreditcard=request.form["has credit card"]
    isactivemember=request.form["is active member"]
    estimatedsalary=request.form["estimated salary"]
    
    if(geography=="Spain"):
        s1,s2,s3=0,0,1
    if(geography=="Germany"):
         s1,s2,s3=0,1,0
    if(geography=="Newyork"):
        s1,s2,s3=0,1,0
        
    if(gender=="female"):
        gender=0
    if(gender=="male"):
        gender=1
    if (isactivemember == "no"):
        isactivemember=0
    if (isactivemember == "yes"):
        isactivemember=1
    
    if (hascreditcard == "no"):
        hascreditcard=0
    if (hascreditcard == "yes"):
        hascreditcard=1
        
    t=[[int(s1),int(s2),int(s3),int(creditscore),int(gender),int(age),int(tenure),int(balance),int(noof),int(hascreditcard),int(isactivemember),int(estimatedsalary)]]
    print(t)
    
    payload_scoring = {"input_data": [{"field": [["G1","G2","G3","CreditScore","Gender","Age","Tenure","Balance","NumOfProducts","HasCrCard","IsActiveMember","EstimatedSalary"]], "values": t}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/88e61062-974c-4fa1-8969-5db6ec2eed65/predictions?version=2022-01-11', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions=response_scoring.json()
    print(predictions)
    pred=predictions['predictions'][0]['values'][0][0]

    if(pred==0):
        output="he will exit"
        print("He will exit")
    else:
        output="he will not exit"
        print("He will not exit")
    return render_template('index.html',prediction_text=output)

if __name__=="__main__":
    app.run(debug=True)
    
        
         
         
             
    