var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var tempSlider = document.getElementById("Temp_slider");
var humSlider = document.getElementById("Hum_slider");
var tempValue = document.getElementById("temp_value");
var humValue = document.getElementById("hum_value");
var heatValue = document.getElementById("heat_value");
//user inputs
var feelingSlider = document.getElementById("Feeling_slider");
var ecoSlider = document.getElementById("Eco_slider");
var feelingValue = feelingSlider.value;
var ecologyValue = ecoSlider.value;
console.log(feelingValue, ecologyValue);
feelingSlider.addEventListener("input", function () {
    console.log("Feeling:", feelingSlider.value);
    sendValues();
});
ecoSlider.addEventListener("input", function () {
    console.log("Ecology:", ecoSlider.value);
    sendValues();
});
// to get user's inputs
function sendValues() {
    var payload = {
        feeling: Number(feelingSlider.value),
        ecology: Number(ecoSlider.value)
    };
    fetch("http://localhost:5000/sliders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    }).catch(function (err) { return console.error(err); });
}
//to select the room
var roomButtons = document.querySelectorAll(".room-btn");
// Add click listeners to each room button
roomButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
        var roomName = btn.innerText.trim().toLowerCase();

        // Update the UI
        document.getElementById("room_value").textContent = btn.innerText;


        var payload = { room: roomName };
        fetch("http://localhost:5000/room", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
            .then(function (res) { return res.json(); })
            .then(function (data) { return console.log("Room updated:", data); })
            .catch(function (err) { return console.error("Error setting room:", err); });
    });
});
//to get the sensor's values
function updateFromSensor() {
    return __awaiter(this, void 0, void 0, function () {
        var res, data, err_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 3, , 4]);
                    return [4 /*yield*/, fetch("http://localhost:5000/data")];
                case 1:
                    res = _a.sent();
                    return [4 /*yield*/, res.json()];
                case 2:
                    data = _a.sent();
                    // Update visible numbers
                    document.getElementById("temp_value").textContent = data.temperature.toFixed(1);
                    document.getElementById("hum_value").textContent = data.humidity.toFixed(1);
                    //document.getElementById("heat_value")!.textContent = data.heat.toFixed(2);
                    // Update sliders
                    tempSlider.value = data.temperature.toString();
                    humSlider.value = data.humidity.toString();
                    return [3 /*break*/, 4];
                case 3:
                    err_1 = _a.sent();
                    console.error("Error fetching sensor data:", err_1);
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
// aggiorna ogni 2 secondi
setInterval(updateFromSensor, 2000);
// valore calcolato
function updateHeating() {
    return __awaiter(this, void 0, void 0, function () {
        var res, data, err_2;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 3, , 4]);
                    return [4 /*yield*/, fetch("http://localhost:5000/heat")];
                case 1:
                    res = _a.sent();
                    return [4 /*yield*/, res.json()];
                case 2:
                    data = _a.sent();
                    if (data.heat !== undefined && data.heat !== null) {
                        document.getElementById("heat_value").textContent = data.heat.toFixed(1);
                    }
                    return [3 /*break*/, 4];
                case 3:
                    err_2 = _a.sent();
                    console.error("Error reading heat:", err_2);
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
// aggiorna ogni second0
setInterval(updateHeating, 1000);
