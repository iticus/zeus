function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function processForecast(forecast) {
    let x = [];
    let temperature = {y: [], type: "scatter", "name": "Temperature"};
    let wind = {y: [], type: "scatter", "name": "Wind", yaxis: "y2"};
    for (let i = 0; i < forecast.hourly.data.length; i++) {
        let item = forecast.hourly.data[i];
        x.push(new Date(item.time * 1000));
        temperature.y.push(item.temperature);
        wind.y.push(item.windSpeed);
    }
    temperature.x = x;
    wind.x = x;
    let data = [temperature, wind];
    let layout = {
        xaxis: {"tickformat": "%d/%m"},
        title: "Weather Forecast for " + forecast.latitude + ", " + forecast.longitude,
        yaxis: {title: "Temperature [C]"},
        yaxis2: {
            title: "Wind [km/h]",
            titlefont: {color: "rgb(148, 103, 189)"},
            tickfont: {color: "rgb(148, 103, 189)"},
            overlaying: "y",
            side: "right"
        }
    };
    Plotly.newPlot("result", data, layout);
}

function showPosition(position) {
    let latitude = position.coords.latitude;
    let longitude = position.coords.longitude;
    let url = "/forecast?lat=" + latitude + "&lng=" + longitude;
    fetch(url)
        .then(response => response.text())
        .then(body => {
            let element = document.querySelector("#result");
            processForecast(JSON.parse(body));
        })
}

document.addEventListener("DOMContentLoaded", () => {
    getLocation();
});