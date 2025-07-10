from flask import Flask, render_template, request

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the data
data = pd.read_csv(r"C:\Users\hocke\OneDrive\Documents\R Programs (Intro to Data Science Class)\Data Sets\insurance2yrs.csv")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form inputs
        age = int(request.form['age'])
        sex = request.form['sex']
        feet = int(request.form['feet'])
        inches = int(request.form['inches'])
        height = feet * 12 + inches
        weight = float(request.form['weight'])
        children_input = request.form['children']
        smoker = request.form['smoker']
        region = request.form['region']

        # Step 1: Calculate BMI
        bmi = round((weight / (height ** 2)) * 703, 1)
        bmi_range = (bmi * 0.9, bmi * 1.1)  # ±10%

        # Step 2: Start filtering
        filtered = data.copy()

        # Age ±1
        filtered = filtered[(filtered['age'] >= age - 1) & (filtered['age'] <= age + 1)]

        # Sex exact match
        filtered = filtered[filtered['sex'].str.lower() == sex.lower()]

        # BMI ±10%
        filtered = filtered[(filtered['bmi'] >= bmi_range[0]) & (filtered['bmi'] <= bmi_range[1])]

        # Children
        if children_input == 'no':
            filtered = filtered[filtered['children'] == 0]
        # if "yes", include all

        # Smoker exact match
        filtered = filtered[filtered['smoker'].str.lower() == smoker.lower()]

        # Region exact match
        filtered = filtered[filtered['region'].str.lower() == region.lower()]

        # Step 3: Calculate average charge
        if not filtered.empty:
            average_charge = round(filtered['charges'].mean(), 2)
            result_message = f"${average_charge} (based on {len(filtered)} matching profiles)"
        else:
            result_message = "No similar profiles found in the dataset."

        return render_template('result.html', estimated_charge=result_message)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
