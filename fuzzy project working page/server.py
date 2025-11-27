from flask import Flask, jsonify
import serial, re
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)

print("FLASK STARTED - CORS SHOULD BE ENABLED")

#at the beginning set to 5 later used to store sliders preference
slider_values = {"feeling": 5, "ecology": 5}

# as default we start with living room rule
current_room = {"room": "living room"}


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


#for ecology and feeling
@app.route("/sliders", methods=["POST"])
def post_sliders():
    global slider_values
    print("RAW request data:", request.data)
    print("RAW request json:", request.get_json(silent=True))
    slider_values = request.get_json()
    print("SLIDERS SET TO:", slider_values)
    return jsonify({"status": "ok"})


@app.route("/sliders", methods=["GET"])
def get_sliders():
    return jsonify(slider_values)


#for room change
@app.route("/room", methods=["POST"])
def set_room():
    global current_room
    current_room = request.get_json()
    print("ROOM SET TO:", current_room)
    return jsonify({"status": "ok"})

@app.route("/room", methods=["GET"])
def get_room():
    return jsonify(current_room)





#main flask server run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
