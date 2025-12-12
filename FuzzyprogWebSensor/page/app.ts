const tempSlider = document.getElementById("Temp_slider") as HTMLInputElement;
const humSlider = document.getElementById("Hum_slider") as HTMLInputElement;
const tempValue = document.getElementById("temp_value")!;
const humValue = document.getElementById("hum_value")!;
const heatValue = document.getElementById("heat_value")  as HTMLInputElement;
const roomValue = document.getElementById("room_value")  as HTMLInputElement;


//user inputs
const feelingSlider = document.getElementById("Feeling_slider") as HTMLInputElement;
const ecoSlider = document.getElementById("Eco_slider") as HTMLInputElement;

const feelingValue = feelingSlider.value;
const ecologyValue = ecoSlider.value;

console.log(feelingValue, ecologyValue);

feelingSlider.addEventListener("input", () => {
    console.log("Feeling:", feelingSlider.value);
    sendValues();
});

ecoSlider.addEventListener("input", () => {
    console.log("Ecology:", ecoSlider.value);
    sendValues();
});


// to get user's inputs
function sendValues() {
    const payload = {
        feeling: Number(feelingSlider.value),
        ecology: Number(ecoSlider.value)
    };

    fetch("http://localhost:5000/sliders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    }).catch(err => console.error(err));
}


//to select the room
const roomButtons = document.querySelectorAll(".room-btn");

// Add click listeners to each room button
roomButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        const roomName = (btn as HTMLButtonElement).innerText.trim().toLowerCase();

        const payload = { room: roomName };

        fetch("http://localhost:5000/room", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => console.log("Room updated:", data))
        .catch(err => console.error("Error setting room:", err));
    });
});

// to display it
async function updateRoom() {
  try {
    const res = await fetch("http://localhost:5000/room");
    const data = await res.json();

    // Update the UI
    document.getElementById("room_value").textContent = btn.innerText;

    if (data.room !== undefined && data.room !== null) {
      document.getElementById("room_value").textContent = data.room.toFixed(1);
    }

  } catch (err) {
    console.error("Error fetching sensor data:", err);
  }
}




//to get the sensor's values


async function updateFromSensor() {
  try {
    const res = await fetch("http://localhost:5000/data");
    const data = await res.json();

    // Update visible numbers
    document.getElementById("temp_value")!.textContent = data.temperature.toFixed(1);
    document.getElementById("hum_value")!.textContent = data.humidity.toFixed(1);
    //document.getElementById("heat_value")!.textContent = data.heat.toFixed(2);


    // Update sliders
    tempSlider.value = data.temperature.toString();
    humSlider.value = data.humidity.toString();

  } catch (err) {
    console.error("Error fetching sensor data:", err);
  }
}


// aggiorna ogni 2 secondi
setInterval(updateFromSensor, 2000);




// valore calcolato
async function updateHeating() {
  try {
    const res = await fetch("http://localhost:5000/heat");
    const data = await res.json();

    if (data.heat !== undefined && data.heat !== null) {
      document.getElementById("heat_value").textContent = data.heat.toFixed(1);
    }

  } catch (err) {
    console.error("Error reading heat:", err);
  }
}
// aggiorna ogni second0
setInterval(updateHeating, 1000);