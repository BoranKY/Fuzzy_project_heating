

  

# Web page and sensor connection
In this section it is possible to test our program with some real data and interact with it through a GUI.

  

## Elements

 - *fuzzy_heating_with_web_values.ipynb* contains the fuzzy program that computes with the values recorded by the sensor (humidity and temperature) and the values selected by the user (feeling and ecological impact)
 - /server:
 > - *server.py* is the server, the flask API regulating the routes
 - /page:
  > - *page.htm* is the html file of the web page with its basic components
 > - *style.css* used to make the web page more aesthetically pleasing
   >- *app.js* built from *app.ts* (`tsc app.ts`) regulates the behavior of the webpage. Reactivity, posting on the routes and retrieving from them.

## Required libraries
To run the Flask API
`pip install flask pyserial`

one should ensure to also have installed the CORS library
`pip install flask_cors`

then one need to be in the current folder 
` cd FuzzyprogWebSensor`

go to the curresponding folder and run the webserver 
` cd server`
` python server.py`

(can check the flask connectivity on the page localhost:5000/data (sensor values) and the values of feeling and ecology on the page http://127.0.0.1:5000/sliders )

 
in the end open the html on a browser of your choice
! to avoid problems of POST blocking, do not open it as file:///, rather launch the command 
`python -m http.server 8000`
from the folder */FuzzyprogWebSensor/page*

and then open the page http://localhost:8000/page.html
