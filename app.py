import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from flask import Flask, request, render_template

# Load dataset and model
dataset = pd.read_csv('dataset/upi_fraud_dataset.csv', index_col=0)
x = dataset.iloc[:, :10].values
y = dataset.iloc[:, 10].values

scaler = StandardScaler()
scaler.fit_transform(x)

model = tf.keras.models.load_model('model/project_model1.h5')

app = Flask(__name__)

# Routes
@app.route('/')
@app.route('/first')
def first():
    return render_template('first.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/preview', methods=['GET', 'POST'])  # <-- Allow both for testing
def preview():
    if request.method == 'POST':
        if 'datasetfile' not in request.files:
            return "No file part"
        dataset = request.files['datasetfile']
        if dataset.filename == '':
            return "No selected file"
        df = pd.read_csv(dataset, encoding='unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html", df_view=df)
    return "Please submit the form via POST."

@app.route('/prediction1', methods=['GET'])
def prediction1():
    return render_template('index.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/detect', methods=['POST'])
def detect():
    trans_datetime = pd.to_datetime(request.form.get("trans_datetime"))
    v1 = trans_datetime.hour
    v2 = trans_datetime.day
    v3 = trans_datetime.month
    v4 = trans_datetime.year
    v5 = int(request.form.get("category"))
    v6 = float(request.form.get("card_number"))
    dob = pd.to_datetime(request.form.get("dob"))
    v7 = (trans_datetime - dob).days // 365
    v8 = float(request.form.get("trans_amount"))
    v9 = int(request.form.get("state"))
    v10 = int(request.form.get("zip"))

    x_test = np.array([v1, v2, v3, v4, v5, v6, v7, v8, v9, v10])
    y_pred = model.predict(scaler.transform([x_test]))

    result = "VALID TRANSACTION" if y_pred[0][0] <= 0.5 else "FRAUD TRANSACTION"
    return render_template('result.html', OUTPUT=result)

if __name__ == "__main__":
    app.run(debug=True)
