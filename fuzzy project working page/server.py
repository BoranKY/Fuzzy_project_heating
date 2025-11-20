from flask import Flask, jsonify
import serial, re
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)

print("FLASK STARTED - CORS SHOULD BE ENABLED")

def extract_data(output):
    match = re.search(r'\d+\.\d+', output)
    if match:
        return float(match.group(0))
    return None

def read_sensor():
    ser = serial.Serial('COM3', 9600, timeout=2)

    data = {}

    # read until target keyword appears
    def wait_for(tag):
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if tag in line:
                return extract_data(line)

    data["temperature"] = wait_for("Temperature")
    data["pressure"]    = wait_for("Pressure")
    data["altitude"]    = wait_for("Altitude")
    data["humidity"]    = wait_for("Humidity")

    ser.close()
    return data

@app.route("/data", methods=["GET", "OPTIONS"])
def get_data():
    return jsonify(read_sensor())



@app.route("/sliders", methods=["POST"])
def post_data():
    data = request.get_json()
    print("Received:", data)
    return jsonify({"status": "ok"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
