#Step1 - Importing Required Libraries 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, request, render_template, redirect, url_for
import pickle

#Step2 - Initializing the Flask
app = Flask(__name__)
model = pickle.load(open(r'SBSPS-Challenge-10396-1691070448\PlacementPrediction\PlacementPrediction_rf.pk1','rb'))


#step3 - Routing to the templates with functionalities
@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/submit', methods = ['POST'])

def submit():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        gender = request.form.get('gender')
        secondary_school_percentage = request.form.get('ssc_p')
        high_school_percentage = request.form.get('hsc_p')
        high_school_stream = request.form.get('hsc_s')
        degree_percentage = request.form.get('degree_p')
        degree_type = request.form.get('degree_t')
        work_experience = request.form.get('workex')
        employability_test_percentage = request.form.get('etest_p')
        specialisation = request.form.get('specialisation')
        mba_percentage = request.form.get('mba_p')

    try:
        secondary_school_percentage = float(secondary_school_percentage)
        high_school_percentage = float(high_school_percentage)
        degree_percentage = float(degree_percentage)
        employability_test_percentage = float(employability_test_percentage)
        mba_percentage = float(mba_percentage)
    
    except ValueError:
        # Handle invalid input (e.g., non-numeric values)
        return "Invalid input. Please enter numeric values for percentage fields."

    # Create a feature vector with the form inputs
    feature_vector = [int(gender), secondary_school_percentage, high_school_percentage, int(high_school_stream), degree_percentage, int(degree_type), int(work_experience), employability_test_percentage, specialisation, mba_percentage]

    # Make predictions using the loaded model
    import requests

    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "yjE1EqzMhv1bFKv4PlKZdClTCnLaFgx8e-Vu2mYUyzri"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["gender", "ssc_p", "hsc_p","hsc_s", "dgree_p", "degree_t", "workex", "etest_p","specialisation", "mba_p"], "values": feature_vector}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/84db3997-9455-4e0c-90ab-6d2158394b12/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    prediction = response_scoring

    # Define a result message and URL for redirection based on the prediction
    if prediction == 1:
        result_message = "Congratulations " + name + "! You have high chances of getting placed."
    else:
        result_message = "Sorry " + name + ", your chances of getting placed are low."

    # Redirect to the results page with the result message
    return redirect(url_for('results', message=result_message))

@app.route('/results/<message>')
def results(message):
    return render_template('results.html', message=message)


if __name__ == '__main__':
    app.run()


  