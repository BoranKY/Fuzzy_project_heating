to transfer data from the sensor to the page the flask API is used

pip install flask pyserial

one should ensure to als have installed the CORS library

pip install flask_cors


to run the project one has to be sure that the app.js has been build (done via the command "tsc app.ts")

then one need to be in the folder "fuzzy project working page"

run the webserver with python server.py


(can check the flask connectivity on the page [localhost:5000/data](http://127.0.0.1:5000/data) and the values of feeling and ecology on the page http://127.0.0.1:5000/sliders )


in the end open the html on a browser of your choice
to avoid problems of POST blocking, do not open it as file:///, rather launch the command
python -m http.server 8000

and then open the page
http://localhost:8000/page.html