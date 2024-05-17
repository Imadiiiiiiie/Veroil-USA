import pickle 
from flask import Flask, request, jsonify, render_template
from statsmodels.tsa.arima.model import ARIMA
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to load saved models
def load_models(filename):
    with open(filename, 'rb') as file:
        models = pickle.load(file)
    return models

# Load the saved models
Regular_models = load_models('Regular_models.pkl')
Premium_models = load_models('Premium_models.pkl')
Reformulated_models = load_models('Reformulated_models.pkl')
Diesel_model = load_models('Diesel_model.pkl')

@app.route('/', methods=['GET'])
def index():
    return render_template('index_1.html')

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data from the request
        date = request.form['date']
        fuel_type = request.form['fuelType']

        if fuel_type == 'Diesel':
            # Use diesel model directly for prediction
            model = Diesel_model
            forecast_value = model.forecast()  # Example: model.forecast(date)
            return jsonify({'predicted_value': float(forecast_value)}), 200

        elif fuel_type == 'Gasoline':
            gasoline_type = request.form['gasolineType']

            # Prepare to collect predictions from all relevant models
            predictions = {}

            # Iterate over all relevant models for the selected gasoline type
            if gasoline_type == 'Regular':
                for category, model in Regular_models.items():
                    if category.startswith('Regular'):
                        print(f"Using model for category: {category}")
                        forecast_value = model.forecast()  # Example: model.forecast(date)
                        predictions[category] = float(forecast_value)

            elif gasoline_type == 'Midgrade':
                for category, model in Premium_models.items():
                    if category.startswith('Midgrade'):
                        print(f"Using model for category: {category}")
                        forecast_value = model.forecast()  # Example: model.forecast(date)
                        predictions[category] = float(forecast_value)

            elif gasoline_type == 'Premium':
                for category, model in Reformulated_models.items():
                    if category.startswith('Premium'):
                        print(f"Using model for category: {category}")
                        forecast_value = model.forecast()  # Example: model.forecast(date)
                        predictions[category] = float(forecast_value)

            print("Predictions:", predictions)  # Debug print to check predictions dictionary
            return jsonify({'predictions': predictions}), 200
        

            if not predictions:
                return jsonify({'error': f"No predictions available for gasoline type '{gasoline_type}'"}), 400

            return jsonify({'predictions': predictions}), 200

        

        else:
            return jsonify({'error': f"Invalid fuel type '{fuel_type}'"}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
