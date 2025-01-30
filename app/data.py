from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Path to the CSV file
CSV_PATH = r"C:\\Users\\Ev\\Desktop\\TRG9\\avocado.csv"

@app.route("/load_data", methods=["GET"])
def load_data():
    try:
        # Load the CSV file and select the required columns
        columns_to_load = ["Date", "AveragePrice", "TotalVolume", "type", "year", "region"]
        data = pd.read_csv(CSV_PATH, usecols=columns_to_load)
        
        # Convert the DataFrame to a list of dictionaries for JSON response
        data_json = data.to_dict(orient="records")

        return jsonify({"status": "success", "data": data_json}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
