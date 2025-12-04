from flask import Flask, render_template, request
import pickle
import numpy as np

# ---------------- Load Model ----------------
with open("rf_electricity_model.pkl", "rb") as file:
    model = pickle.load(file)

app = Flask(__name__)

# ---------------- Helper Functions ----------------
def convert_house_size(size_str):
    """Convert house size like '0-5' or '10-15' to numeric midpoint."""
    try:
        parts = size_str.split('-')
        if len(parts) == 2:
            return (float(parts[0]) + float(parts[1])) / 2
        else:
            return float(parts[0])
    except:
        return 0

# ---------------- Routes ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get input values from form
        house_size = convert_house_size(request.form["house_size_marla"])
        num_residents = float(request.form["num_residents"])
        month = float(request.form["month"])
        temperature = float(request.form["temperature"])
        num_lights = float(request.form["num_lights"])
        hours_lights = float(request.form["hours_lights"])
        num_fans = float(request.form["num_fans"])
        hours_fans = float(request.form["hours_fans"])
        num_AC = float(request.form["num_AC"])
        hours_AC = float(request.form["hours_AC"])
        num_fridge = float(request.form["num_fridge"])
        num_washing_machine = float(request.form["num_washing_machine"])
        hours_washing_machine = float(request.form["hours_washing_machine"])
        num_TV = float(request.form["num_TV"])
        hours_TV = float(request.form["hours_TV"])
        num_computer = float(request.form["num_computer"])
        hours_computer = float(request.form["hours_computer"])
        num_water_heater = float(request.form["num_water_heater"])
        hours_water_heater = float(request.form["hours_water_heater"])

        # Arrange in same order as training features
        features = np.array([[house_size, num_residents, month, temperature,
                              num_lights, hours_lights, num_fans, hours_fans,
                              num_AC, hours_AC, num_fridge, num_washing_machine,
                              hours_washing_machine, num_TV, hours_TV,
                              num_computer, hours_computer, num_water_heater, hours_water_heater]])

        # Make prediction
        predicted_kwh = model.predict(features)[0]
        predicted_kwh = round(predicted_kwh, 1)

        return render_template("index.html", prediction=predicted_kwh)

    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    app.run(debug=True)
