#Step1 - Importing Required Libraries 
from flask import Flask, request, render_template
import pickle

#Step2 - Initializing the Flask
app = Flask(__name__)
model = pickle.load(open(r'PlacementPrediction_rf.pk1','rb'))

#step3 - Routing to the templates with functionalities
@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/Home', methods = ['POST'])

def prod():
    name = request.form.get('name')
    gender = request.form.get('gender')
    ssc_p = request.form.get('ssc_p')
    hsc_p = request.form.get('hsc_p')
    hsc_s = request.form.get('hsc_s')
    degree_p = request.form.get('degree_p')
    degree_t = request.form.get('degree_t')
    workex = request.form.get('workex')
    etest_p = request.form.get('etest_p')
    specialisation = request.form.get('specialisation')
    mba_p = request.form.get('mba_p')
    input = [[int(gender), float(ssc_p), float(hsc_p), int(hsc_s), float(degree_p), int(degree_t), int(workex), float(etest_p), int(specialisation), float(mba_p)]]
    #print(input)
    op = model.predict(input)
    
    if op == 1:
        text = "You are placed!"
        print(text)
    else:
        text = "You are not placed!"
        print(text)
    
    return render_template('Home.html', Output = str(text))

#step4- run the application

if __name__ == '__main__':
    app.run()

  