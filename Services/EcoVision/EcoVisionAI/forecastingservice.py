from flask import Flask, jsonify
from prophet import Prophet
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

@app.route('/forecast', methods=['GET'])
def forecast():
    engine = create_engine('sqlite:///ecovision.db')
    df = pd.read_sql('SensorData', con=engine)
    df.rename(columns={'Timestamp': 'ds', 'Temperature': 'y'}, inplace=True)
    model = Prophet()
    model.fit(df[['ds', 'y']])
    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    forecast_data = forecast[['ds', 'yhat']].tail(24).to_dict(orient='records')
    return jsonify(forecast_data)

if __name__ == '__main__':
    app.run(port=5005)
