# Web page
## HTML page
The structure of the HTML page is pretty straight foreward.

It cointains:

- a title
- some buttons to select the current room
- a display of the selected room
- some sliders displaying the actual values of temperature and humidity
- some sliders where the user can set their feeling and degree of ecology
- a display of the computed settings of the thermostat (temperature set) 

## responsive elements, app.js script
Apart from the title, all the elements on the page are related to other programs. 
We then set the following IDs:

- id="room_value"
- id="Temp_slider"
- id="Hum_slider"
- id="Feeling_slider"
- id="Eco_slider"
- id="heat_value"

Whose values are either posted or retreated by the js program. 

The room buttons are simply set in a class (class="room-btn") who takes the same value as the label of the clicked button.

