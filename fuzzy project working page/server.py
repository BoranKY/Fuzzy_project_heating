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





# problematic part
@app.route("/compute", methods=["POST"])
def compute_heat():
    import numpy as np
    import skfuzzy as fuzz
    from skfuzzy import control as ctrl





    ############################################### fuzzy I/O variables  ######################################################

    # Inputs
    temperature = ctrl.Antecedent(np.arange(-44, 86, 1), 'temperature')      # °C
    humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')     # %
    feeling = ctrl.Antecedent(np.arange(0, 11, 1), 'feeling')        # 0=cold ... 10=hot
    ecology = ctrl.Antecedent(np.arange(0, 11, 1), 'ecology')        # 0=very ecologically concerned ... 10=not concerned by ecology

    # Output
    heat = ctrl.Consequent(np.arange(10, 45, 1), 'heat')       # heating level °C

    # It's gonna show us to which temperature we should heat/cool the room.





    ############################################### membership functions ############################################################


    room = current_room["room"]
    print("Using room:", room)


    def temp_membership_func(var, b1, c1, s1, m1, s2, m2, s3 ,m3, b2, c2):
        # for the b parameter we set the mean of our data and for c the standard deviation, even though this is not totally accurate and we would need a curve fitting, we think these are relatively acceptable parameters
        var['too cold']    = fuzz.sigmf(var.universe, b=b1,  c=-c1)
        var['chilly']    = fuzz.gaussmf(var.universe, sigma=s1,  mean=m1)
        var['comfortable']  = fuzz.gaussmf(var.universe, sigma=s2,  mean=m2)
        var['rather hot']     = fuzz.gaussmf(var.universe, sigma=s3,  mean=m3)
        var['too hot']     = fuzz.sigmf(var.universe, b=b2,  c=c2)


    if room == 'bathroom':
        temp_membership_func(temperature, 15.38, 2.73, 2.60, 17.75, 1.91, 21.75, 2.10, 25.88, 28.68, 1.69)
        temp_membership_func(heat, 15.38, 2.73, 2.60, 17.75, 1.91, 21.75, 2.10, 25.88, 28.68, 1.69)

    elif room == 'kitchen':
        temp_membership_func(temperature, 12.75, 3.49, 3.14, 16.88, 3.55, 21.00, 3.98, 25.19, 28.25, 4.37)
        temp_membership_func(heat, 12.75, 3.49, 3.14, 16.88, 3.55, 21.00, 3.98, 25.19, 28.25, 4.37)

    elif room == 'bedroom':
        temp_membership_func(temperature, 13.39, 4.68, 4.06, 15.59, 3.08, 18.83, 2.76, 23.11, 25.08, 2.46)
        temp_membership_func(heat, 13.39, 4.68, 4.06, 15.59, 3.08, 18.83, 2.76, 23.11, 25.08, 2.46)

    #else: # room in living room or any other room (standard)
    #    temp_membership_func(temperature, 13.00, 3.16, 2.67, 17.62, 2.91, 21.07, 4.49, 26.77, 29.50, 4.66)
    #    temp_membership_func(heat, 13.00, 3.16, 2.67, 17.62, 2.91, 21.07, 4.49, 26.77, 29.50, 4.66)

    elif room == 'living room': # room in living room or any other room (standard)
        temp_membership_func(temperature, 13.00, 3.16, 2.67, 17.62, 2.91, 21.07, 1.49, 26.77, 29.50, 4.66)
        temp_membership_func(heat, 13.00, 3.16, 2.67, 17.62, 2.91, 21.07, 1.49, 26.77, 29.50, 4.66)


    # according to https://atmotube.com/blog/ideal-household-humidity-level, a good humidity for inside is 40-50% --> 45% should be optimal
    humidity['low']    = fuzz.trapmf(humidity.universe, [0, 0, 0, 45])
    humidity['ok']     = fuzz.trimf(humidity.universe, [0, 45, 100])
    humidity['high']   = fuzz.trapmf(humidity.universe, [45, 100, 100, 100])

    feeling['too cold']    = fuzz.trapmf(feeling.universe, [0, 0, 0, 5])
    feeling['okay']   = fuzz.trimf(feeling.universe, [0, 5, 10])
    feeling['too hot']     = fuzz.trapmf(feeling.universe, [5, 10, 10, 10])

    ecology['not eco']    = fuzz.trapmf(ecology.universe, [0, 0, 0, 5])
    ecology['medium']   = fuzz.trimf(ecology.universe, [0, 5, 10])
    ecology['eco']     = fuzz.trapmf(ecology.universe, [5, 10, 10, 10])


    ################################################ using Sophie's rules#################################################################


    r1 = ctrl.Rule(temperature['too hot'], heat['chilly'])
    r2 = ctrl.Rule(temperature['too cold'], heat['rather hot'])

    r3 = ctrl. Rule(temperature['chilly'] & feeling['too cold'], heat['rather hot'])
    r4 = ctrl. Rule(temperature['chilly'] & feeling['too hot'], heat['too cold'])
    r5 = ctrl. Rule(temperature['rather hot'] & feeling['too cold'], heat['too hot'])
    r6 = ctrl. Rule(temperature['rather hot'] & feeling['too hot'], heat['chilly'])
    r7 = ctrl. Rule(temperature['chilly'] & feeling['okay'], heat['chilly'])
    r8 = ctrl. Rule(temperature['rather hot'] & feeling['okay'], heat['rather hot'])
    r9 = ctrl. Rule(temperature['comfortable'] & feeling['too hot'], heat['chilly'])
    r10 = ctrl. Rule(temperature['comfortable'] & feeling['okay'], heat['comfortable'])
    r11 = ctrl. Rule(temperature['comfortable'] & feeling['too cold'], heat['rather hot'])

    r12 = ctrl. Rule((temperature['too cold'] | temperature['chilly']) & ecology['eco'], heat['chilly'])
    r13 = ctrl. Rule((temperature['too hot'] | temperature['rather hot']) & ecology['eco'], heat['rather hot'])
    r14 = ctrl. Rule((temperature['too cold'] | temperature['chilly']) & ecology['medium'], heat['comfortable'])
    r15 = ctrl. Rule((temperature['too hot'] | temperature['rather hot']) & ecology['medium'], heat['comfortable'])
    r16 = ctrl. Rule((temperature['too cold'] | temperature['chilly']) & ecology['not eco'], heat['rather hot'])
    r17 = ctrl. Rule((temperature['too hot'] | temperature['rather hot']) & ecology['not eco'], heat['chilly'])

    heating_ctrl = ctrl.ControlSystem([r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17])
    heating_sim = ctrl.ControlSystemSimulation(heating_ctrl)



    ########################## Fuzzy computation ##########################################


    #get sensor's records from flask API

    sensor = read_sensor()

    if t is None or h is None:
        return jsonify({"error": "Sensor read failed"}), 500


    t = sensor["temperature"]
    h = sensor["humidity"]

    print("Sensor:", sensor)

    #get user's preferences (feeling, ecology)

    user_feeling = slider_values["feeling"]
    user_ecology = slider_values["ecology"]

    print("Sliders:", user_feeling, user_ecology)



    #heating_sim.input['temperature'] = 17
    heating_sim.input['temperature'] = t  
    #heating_sim.input['humidity'] = h

    #heating_sim.input['humidity'] = 60
    heating_sim.input['feeling'] = user_feeling
    heating_sim.input['ecology'] = user_ecology


    heating_sim.compute()
    #print( "Computed heat output:", heating_sim.output['heat'])
    return jsonify({
    "heat": float(heating_sim.output['heat']),
    "temperature": t,
    "humidity": h
    })
 



#main flask server run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
