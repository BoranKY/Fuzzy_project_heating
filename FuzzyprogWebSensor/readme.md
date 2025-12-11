
  

# Web page and sensor connection
In this section it is possible to test our program with some real data and interact with it through a GUI.

  

## Elements

  

 - *Test_sensor.ipynb* contains the code we used to test the sensor used and retrieve the data from it
 - *app.js* built from *app.ts* regulates the behavior of the webpage. Reactivity, posting on the routes and retrieving from them.
 - *fuzzy_heating_with_web_values.ipynb* contains the fuzzy program that computes with the values recorded by the sensor (humidity and temperature) and the values selected by the user (feeling and ecological impact)
 - *page.htm* is the html file of the web page with its basic components
 - *server.py* is the server, the flask API regulating the routes
 - *style.css* used to make the web page more aesthetically pleasing

## Required libraries
to transfer data from the sensor to the page the flask API is used

  

pip install flask pyserial

  

one should ensure to als have installed the CORS library

  

pip install flask_cors

  

to run the project one has to be sure that the app.js has been build (done via the command "tsc app.ts")

  

then one need to be in the folder "fuzzy project working page"

  

run the webserver with python server.py

  

(can check the flask connectivity on the page localhost:5000/data and the values of feeling and ecology on the page http://127.0.0.1:5000/sliders )

  

in the end open the html on a browser of your choice to avoid problems of POST blocking, do not open it as file:///, rather launch the command python -m http.server 8000

  

and then open the page http://localhost:8000/page.html
