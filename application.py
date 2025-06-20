import pickle
from flask import Flask,jsonify,request,render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
application=Flask(__name__)
app=application
ridge_model=pickle.load(open('models/ridge.pkl','rb'))
standard_scaler=pickle.load(open('models/scaler.pkl','rb'))
@app.route("/")
def index():
    return render_template("index.html")
@app.route('/predictdata',methods=['GET','POST'])
@app.route('/predictdata', methods=['GET', 'POST'])
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == "POST":
        try:
            temp = float(request.form.get("temp"))
            rh = float(request.form.get("rh"))
            ws = float(request.form.get("ws"))
            rain = float(request.form.get("rain"))
            ffmc = float(request.form.get("ffmc"))
            dmc = float(request.form.get("dmc"))
            isi = float(request.form.get("isi"))
            region = float(request.form.get("region"))
            classes = float(request.form.get("classes"))
            input_data = np.array([[temp, rh, ws, rain, ffmc, dmc, isi,region,classes]])
            scaled_data = standard_scaler.transform(input_data)
            prediction = ridge_model.predict(scaled_data)

            return render_template(
                "home.html",
                prediction_text=f"Predicted Fire Weather Index (FWI): {prediction[0]:.2f} (Region: {region}, Class: {classes})"
            )

        except Exception as e:
            return render_template("home.html", prediction_text=f"Error: {str(e)}")
    else:
        return render_template("home.html")
if __name__=="__main__":
    app.run(host="0.0.0.0")

