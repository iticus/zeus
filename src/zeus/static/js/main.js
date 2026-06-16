function cacheForecast(location, forecast) {
    localStorage.setItem(location, JSON.stringify(forecast));
}

function loadForecast(location) {
    let data = localStorage.getItem(location);
    if (data === null) {
        return {};
    }
    return JSON.parse(data);
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(processLocation);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function generateTemperatureHumidity(forecast, key) {
    let temperature = {y: [], x: [], type: "line", "name": "Temperature", "line": {"shape": "spline", "smoothing": 1.3}, fill: "tozeroy"}
    let humidity = {y: [], x: [], type: "line", "name": "Humidity", yaxis: "y2",  "line": {"shape": "spline", "smoothing": 1.3},  fill: "tozeroy"}
    for (let i = 0; i < forecast.list.length; i++) {
        let item = forecast.list[i];
        let d = new Date(item.dt * 1000);       
        let k = d.toISOString().slice(0,10);
        if (key === undefined || key === k) {
            temperature.x.push(d);
            temperature.y.push(item.main.temp);
            humidity.x.push(d);
            humidity.y.push(item.main.humidity);
        }
    }
    let data = [temperature, humidity];
    let layout = {
        title: key,
        colorway : ['#F9C74F', '#90BE6D'],
        xaxis: {"tickformat": "%H:%M"},
        yaxis: {title: "Temperature [C]"},
        yaxis2: {
            title: "Humidity [%]",
            titlefont: {color: "rgb(148, 103, 189)"},
            tickfont: {color: "rgb(148, 103, 189)"},
            tickformat: ',.0%',
            overlaying: "y",
            side: "right"
        }
    };
    Plotly.newPlot("hourlyChart", data, layout);
}

function processForecast(forecast) {
    let x = [];
    let temperatureLow = {
        y: [], x: x, type: "line", "name": "Low", textposition: "auto", opacity: 0.9,
        line: {"shape": "spline", "smoothing": 1.3}, fill: "tozeroy"
    };
    let temperatureHigh = {
        y: [], x: x, type: "line", "name": "High", textposition: "auto", opacity: 0.9,
        line: {"shape": "spline", "smoothing": 1.3}, fill: "tozeroy"
    };
    let y_range = [100, -100];
    for (let i = 0; i < forecast.list.length; i++) {
        let item = forecast.list[i];
        x.push(new Date(item.dt * 1000));
        if (y_range[0] > item.main.temp_min) {
            y_range[0] = item.main.temp_min;
        }
        if (y_range[1] < item.main.temp_max) {
            y_range[1] = item.main.temp_max;
        }
        temperatureLow.y.push(item.main.temp_min);
        temperatureHigh.y.push(item.main.temp_max);
    }
    y_range[0] -= 2; y_range[1] += 2;
    temperatureLow.text = temperatureLow.y.map(String);
    temperatureHigh.text = temperatureHigh.y.map(String);
    let dailyData = [temperatureHigh, temperatureLow];
    let layout = {
        title: "Temperature",
        colorway : ['#F9C74F', '#277DA1'],
        // barmode: "group",
        xaxis: {tickformat: "%d %B"},
        yaxis: {title: "Temperature [C]", autorange: true, range: y_range}
    };
    Plotly.newPlot("temperatureChart", dailyData, layout);
    generateTemperatureHumidity(forecast);
    document.getElementById("temperatureChart").on("plotly_click", function(data) {
        let key = data.points[0].x;
        generateTemperatureHumidity(forecast, key);
    });
}

function processLocation(position) {
    let latitude = position.coords.latitude;
    let longitude = position.coords.longitude;
    let geocodeUrl = "/geocode?lat=" + latitude + "&lng=" + longitude;
    fetch(geocodeUrl)
        .then(response => response.text())
        .then(body => {
            let element = document.querySelector("#locationHeader");
            let geocodeResult = JSON.parse(body);
            let bestGuess = geocodeResult["results"][0];
            for (let i=0; i<geocodeResult["results"].length;i++){
                if (geocodeResult["results"][i]["geometry"]["location_type"] == "APPROXIMATE") {
                    bestGuess = geocodeResult["results"][i];
                    break;
                }
            }
            element.innerHTML = bestGuess["formatted_address"];
            let forecastUrl = "/weather?operation=forecast&lat=" + latitude + "&lng=" + longitude;
            fetch(forecastUrl)
                .then(response => response.text())
                    .then(body => {
                        // let url = "/forecast?lat=" + latitude + "&lng=" + longitude;
                        processForecast(JSON.parse(body));
                    })
        })
}

document.addEventListener("DOMContentLoaded", () => {
    getLocation();
    $(".nav-tabs").find("a").on("show.bs.tab", function () {
        $('#locationModal').modal('show');
    });
});