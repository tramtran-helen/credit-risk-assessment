from flask import Flask, render_template, request
import pandas as pd
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load pre-trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Dictionaries to map form values
EDUCATION_MAP = {
    "Graduate School": 1,
    "University": 2,
    "High School": 3,
    "Others": 4
}

MARRIAGE_MAP = {
    "Married": 1,
    "Single": 2,
    "Others": 3
}

# Helper function to extract integer form inputs with default
def get_int_form_value(name, default=0):
    return int(request.form.get(name, default))

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        try:
            # Fetching form inputs
            limit_bal = get_int_form_value("limit_bal")
            age = get_int_form_value("age")
            sex = 0 if request.form.get("sex", "Female") == "Female" else 1
            education = EDUCATION_MAP.get(request.form.get("education", "Others"), 4)
            marriage = MARRIAGE_MAP.get(request.form.get("marriage", "Others"), 3)

            pay_status = [get_int_form_value(f"pay_status_{month}") for month in ["sept", "aug", "jul", "jun", "may", "apr"]]
            bill_amts = [get_int_form_value(f"bill_amt_{month}") for month in ["sept", "aug", "jul", "jun", "may", "apr"]]
            pay_amts = [get_int_form_value(f"pay_amt_{month}") for month in ["sept", "aug", "jul", "jun", "may", "apr"]]

            # Assemble input DataFrame
            input_data = pd.DataFrame({
                "LIMIT_BAL": [limit_bal],
                "SEX": [sex],
                "EDUCATION": [education],
                "MARRIAGE": [marriage],
                "AGE": [age],
                "PAY_0": [pay_status[0]],
                "PAY_2": [pay_status[1]],
                "PAY_3": [pay_status[2]],
                "PAY_4": [pay_status[3]],
                "PAY_5": [pay_status[4]],
                "PAY_6": [pay_status[5]],
                "BILL_AMT1": [bill_amts[0]],
                "BILL_AMT2": [bill_amts[1]],
                "BILL_AMT3": [bill_amts[2]],
                "BILL_AMT4": [bill_amts[3]],
                "BILL_AMT5": [bill_amts[4]],
                "BILL_AMT6": [bill_amts[5]],
                "PAY_AMT1": [pay_amts[0]],
                "PAY_AMT2": [pay_amts[1]],
                "PAY_AMT3": [pay_amts[2]],
                "PAY_AMT4": [pay_amts[3]],
                "PAY_AMT5": [pay_amts[4]],
                "PAY_AMT6": [pay_amts[5]]
            })

            # (Optional) Debugging: print input data
            print("Form Input:")
            print(input_data)

            # Make prediction
            result = model.predict(input_data)[0]
            prediction = (
                "The customer is likely to default on the payment."
                if result == 1 else
                "The customer is not likely to default on the payment."
            )

        except Exception as e:
            prediction = f"Something went wrong: {e}"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
