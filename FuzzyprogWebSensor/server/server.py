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
    try:
        ser = serial.Serial('COM3', 9600, timeout=2)
    except Exception as e:
        print("Serial error:", e)
        return {"temperature": None, "humidity": None}

    def wait_for(tag):
        for _ in range(50):   # try max 50 lines
            line = ser.readline().decode(errors="ignore").strip()
            if tag in line:
                value = extract_data(line)
                return value
        print("Failed to find tag:", tag)
        return None

    temp = wait_for("Temperature")
    hum = wait_for("Humidity")

    ser.close()
    return {"temperature": temp, "humidity": hum}

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


current_heating = None

# to parse the output of the computation
@app.route("/heat", methods=["POST"])
def set_heating():
    global current_heating
    data = request.get_json()
    current_heating = float(data["heat"])
    print("Temperature set to:", current_heating)
    return jsonify({"status": "ok"})

@app.route("/heat", methods=["GET"])
def get_heat():
    return jsonify({"heat": current_heating})




#main flask server run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
