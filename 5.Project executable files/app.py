from flask import Flask, request, render_template
import numpy as np
import joblib
#from flask_cors import CORS

app = Flask(__name__)
model = joblib.load('fleet_fuel.pkl')
#scaler = joblib.load('flee_fuel.pkl')
#CORS(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Fetch input data from the form
        distance = float(request.form['distance'])
        speed = float(request.form['speed'])
        temp_inside = float(request.form['temp_inside'])
        temp_outside = float(request.form['temp_outside'])
        AC = int(request.form['AC'])
        rain = int(request.form['rain'])
        sun = int(request.form['sun'])
        E10 = int(request.form['E10'])
        SP98 = int(request.form['SP98'])

        # Prepare the input data for prediction
        data = np.array([[distance, speed, temp_inside, temp_outside, AC, rain, sun, E10, SP98]])
        data[:, 7] = data[:, 7].astype(bool)
        data[:, 8] = data[:, 7].astype(bool)
        #dum1 = pd.get_dummies(df['gas_type'])
        #df = pd.concat([df, dum1], axis=1)
        #df.drop('gas_type', axis=1, inplace=True)
        #data = scaler.transform(data)  # Ensure the input data is scaled
        prediction = model.predict(data)
        prediction_text = f'Predicted Fuel Consumption: {prediction[0]:.2f}'
        return render_template('index.html', prediction_text=prediction_text)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)