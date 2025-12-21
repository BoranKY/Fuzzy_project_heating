# Server.py
## Libraries
To set and have a functional server we use the following libraries:
- **flask** and  **flask_cors** to create an API sever
- **serial** and **re** to read the sensor's values

## Functions
In the program we define two functions **extract data(output)** and **read_sensor()**. They are used to get the interesting data (Temperature and Humidity) from the sensor.

## Routes
The main goal of the server is to provide some routes for the transmission of information.
When the program is run, the server run on the port 5000
```
if  __name__  ==  "__main__":
	app.run(host="0.0.0.0", port=5000)
```
So on the browser we need to go on http://localhost:5000

Starting from this main route, the following are created:

- http://localhost:5000/data where the Flask server itself uploads the values of temperature and humidity 
i.e. {"humidity": 51, "temperature": 20.4} 
Since only the Flask server updates it, only the action GET needs to be set down.
- http://localhost:5000/sliders cointaining the selected values of Feeling and Ecology 
i.e. {"ecology":5,"feeling":5}
These values are both uploaded and retrieved by files external to the server, hence we define both the GET and the POST methods.
- http://localhost:5000/room cointaining the selected entity of the room
i.e. {"room": "living room"}
This value is both uploaded and retrieved by files external to the server, hence we define both the GET and the POST methods.
- http://localhost:5000/heat cointaining the computed value of the temperature to be set
i.e. {"heat":21.34}
This value is both uploaded and retrieved by files external to the server, hence we define both the GET and the POST methods.