to transfer data from the sensor to the page the flask API is used

pip install flask pyserial

one should ensure to als have installed the CORS library

pip install flask_cors


to run the project one has to be sure that the app.js has been build (done via the command "tsc app.ts")

then one need to be in the folder "fuzzy project working page"

run the webserver with python server.py


(can check the flask connectivity on the page [localhost:5000/data](http://127.0.0.1:5000/data))

in the end open the html on a browser of your choice