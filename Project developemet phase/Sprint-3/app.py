import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import requests
from math import ceil

API_KEY = "QfeBSqnNqjSmGFdJ_DC2d6rWSA21J21p0dDt9kDCERhm"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type":'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['GET','post'])
def predict():  
	
	GRE_Score = int(request.form['GRE Score'])
	TOEFL_Score = int(request.form['TOEFL Score'])
	University_Rating = int(request.form['University Rating'])
	SOP = float(request.form['SOP'])
	LOR = float(request.form['LOR'])
	CGPA = float(request.form['CGPA'])
	Research = int(request.form['Research'])
	
	final_features = [GRE_Score, TOEFL_Score, University_Rating, SOP, LOR, CGPA, Research]
	x = ['GRE_Score', 'TOEFL_Score', 'University_Rating', 'SOP', 'LOR', 'CGPA', 'Research']
	payload_scoring = { "input_data": [{"fields":[x], "values": [final_features]}]}
	response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/72590142-1e6c-4a84-ab58-8fe106dadb4e/predictions?version=2022-11-19', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
	predictions=response_scoring.json()['predictions'][0]['values'][0][0]
	predict=ceil(predictions[0])

	if predict>50:
		predict=ceil(predictions[0]*1.44927536)
	else:
		predict=ceil(predictions[0])
	if predict>50:
		return render_template('index.html', prediction_text='You have a {}%Chance to Get Admission '.format(predict))
	else:
	    return render_template('index.html', prediction_text='You have NO chance of {}% to Get Admission '.format(predict))
	
if __name__ == "__main__":
	app.run(debug=True)
