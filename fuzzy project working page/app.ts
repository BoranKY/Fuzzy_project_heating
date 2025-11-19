const tempSlider = document.getElementById("Temp_slider") as HTMLInputElement;
const humSlider = document.getElementById("Hum_slider") as HTMLInputElement;
const tempValue = document.getElementById("temp_value")!;
const humValue = document.getElementById("hum_value")!;


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

function sendValues() {
    const payload = {
        feeling: Number(feelingSlider.value),
        ecology: Number(ecoSlider.value)
    };

    fetch("http://localhost:5000/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    }).catch(err => console.error(err));
}


async function updateFromSensor() {
  try {
    const res = await fetch("http://localhost:5000/data");
    const data = await res.json();

    // Aggiorna valori numerici
    tempValue.textContent = data.temperature.toFixed(1);
    humValue.textContent = data.humidity.toFixed(1);
    console.log(tempValue.textContent)

    // Aggiorna slider coerenti con i limiti impostati
    tempSlider.value = data.temperature.toString();
    humSlider.value = data.humidity.toString();
  } catch (err) {
    console.error("Errore durante la lettura del sensore:", err);
  }
}

// aggiorna ogni 2 secondi
setInterval(updateFromSensor, 2000);
