from flask import Flask, render_template, request
import requests
import jsonify
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from datetime import datetime

app = Flask(__name__)

model = pickle.load(open("random_forest_regression_model.pkl","rb"))

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


def get_data():
        predictors_lst = []
        Fuel_Type_Diesel = 0
        manufactured_year = int(request.form['Year'])
        if not manufactured_year.is_integer():
            return [['Year must be an integer']]
        age_of_car = datetime.today().year - manufactured_year
        if age_of_car < 0:
            return [['Wrong Year entered']]
        Present_Price = float(request.form['Present_Price'])
        if not Present_Price.is_float():
            return [['Present price must be a number']]
        if Present_Price < 0:
            return [['Wrong Showroom price entered']]

        Kms_Driven = int(request.form['Kms_Driven'])
        if not Kms_Driven.is_integer():
            return [['Kilometers must be a number']]
        if Kms_Driven < 0:
            return [['Wrong kilometers entered']]

        no_of_owner = int(request.form['Owner'])

        if no_of_owner not in [0,1,2,3]:
            return [['Wrong number of owners entered. Enter a number from 0 to 3']]


        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol == "Petrol":
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif Fuel_Type_Petrol == "Diesel":
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0

        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if Seller_Type_Individual == 'Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0

        Transmission_Mannual = request.form['Transmission_Mannual']
        if Transmission_Mannual == 'Mannual':
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0

        predictors_lst.append(Present_Price)
        predictors_lst.append(Kms_Driven)
        predictors_lst.append(no_of_owner)
        predictors_lst.append(age_of_car)
        predictors_lst.append(Fuel_Type_Diesel)
        predictors_lst.append(Fuel_Type_Petrol)
        predictors_lst.append(Seller_Type_Individual)
        predictors_lst.append(Transmission_Mannual)

        return [predictors_lst]



@app.route('/predict', methods=['POST'])
def predict_price():

    if request.method == "POST":

        predictors = get_data()
        if len(predictors) == 1:
            return render_template('index.html', prediction_text=predictors[0][0])
        prediction = model.predict(predictors)
        prediction = round(prediction[0], 2)

        if prediction > 0:
            return render_template('index.html', prediction_text = "You can sell this car for {} lakhs.".format(prediction))
        else:
            return render_template('index.html', prediction_text = "Sorry, you cannot sell this car!!" )

    else:
        return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)