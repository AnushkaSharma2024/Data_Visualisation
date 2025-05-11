from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Ensure no GUI backend is used
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

app = Flask(__name__)

@app.route("/")
def home():
    # Load and preprocess data
    data = pd.read_csv("Sample_Data.csv")
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], dayfirst=True)  # Ensure day-first format

    # Chart 1: Voltage vs. Time
    plt.figure(figsize=(12, 6))
    plt.plot(data['Timestamp'], data['Values'], label='Voltage')
    plt.xlabel('Timestamp')
    plt.ylabel('Values')
    plt.title('Voltage vs. Time')
    plt.legend()
    plt.savefig("static/voltage_chart.png")  # Save the chart in the 'static' folder
    plt.close()

    # Chart 2: Peaks and Lows
    peaks, _ = find_peaks(data['Values'])
    lows, _ = find_peaks(-data['Values'])
    plt.figure(figsize=(12, 6))
    plt.plot(data['Timestamp'], data['Values'], label='Voltage')
    plt.scatter(data['Timestamp'][peaks], data['Values'][peaks], color='green', label='Peaks')
    plt.scatter(data['Timestamp'][lows], data['Values'][lows], color='red', label='Lows')
    plt.xlabel('Timestamp')
    plt.ylabel('Values')
    plt.title('Voltage with Peaks and Lows')
    plt.legend()
    plt.savefig("static/peaks_lows_chart.png")  # Save the chart in the 'static' folder
    plt.close()

    # Chart 3: Moving Average
    data['5-Day MA'] = data['Values'].rolling(window=5).mean()
    plt.figure(figsize=(12, 6))
    plt.plot(data['Timestamp'], data['Values'], label='Voltage')
    plt.plot(data['Timestamp'], data['5-Day MA'], label='5-Day Moving Average', linestyle='--')
    plt.xlabel('Timestamp')
    plt.ylabel('Values')
    plt.title('Voltage with 5-Day Moving Average')
    plt.legend()
    plt.savefig("static/moving_avg_chart.png")  # Save the chart in the 'static' folder
    plt.close()

    return render_template("index.html", 
                           chart1="voltage_chart.png", 
                           chart2="peaks_lows_chart.png", 
                           chart3="moving_avg_chart.png")

if __name__ == "__main__":
    app.run(debug=True)
