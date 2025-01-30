from flask import Flask, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io

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

@app.route("/average_volume_by_month", methods=["GET"])
def average_volume_by_month():
    try:
        # Load the CSV file
        columns_to_load = ["Date", "TotalVolume", "type"]
        data = pd.read_csv(CSV_PATH, usecols=columns_to_load)

        # Convert Date column to datetime
        data["Date"] = pd.to_datetime(data["Date"])

        # Extract month from the Date column
        data["Month"] = data["Date"].dt.month

        # Group by Month and type, then calculate the average TotalVolume
        grouped_data = data.groupby(["Month", "type"]).TotalVolume.mean().unstack()

        # Plot the data
        plt.figure(figsize=(10, 6))
        for avocado_type in grouped_data.columns:
            plt.plot(grouped_data.index, grouped_data[avocado_type], label=avocado_type)

        plt.title("Average Volume Sold by Month")
        plt.xlabel("Month")
        plt.ylabel("Average Volume (Scaled)")
        plt.xticks(range(1, 13))
        plt.legend(title="Type")
        plt.grid()

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plt.close()

        # Return the image as a response
        return send_file(img, mimetype="image/png")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/average_price_by_month/<int:year>", methods=["GET"])
def average_price_by_month(year):
    try:
        # Load the CSV file
        columns_to_load = ["Date", "AveragePrice", "type"]
        data = pd.read_csv(CSV_PATH, usecols=columns_to_load)

        # Convert Date column to datetime
        data["Date"] = pd.to_datetime(data["Date"])

        # Filter data for the specified year
        data = data[data["Date"].dt.year == year]

        # Extract month from the Date column
        data["Month"] = data["Date"].dt.month

        # Group by Month and type, then calculate the average AveragePrice
        grouped_data = data.groupby(["Month", "type"]).AveragePrice.mean().unstack()

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(grouped_data.index, grouped_data["conventional"], label="Conventional", color="orange")
        plt.plot(grouped_data.index, grouped_data["organic"], label="Organic", color="green")

        plt.title(f"Average Price by Month ({year})")
        plt.xlabel("Month")
        plt.ylabel("Average Price ($)")
        plt.xticks(range(1, 13))
        plt.legend(title="Type")
        plt.grid()

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plt.close()

        # Return the image as a response
        return send_file(img, mimetype="image/png")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
