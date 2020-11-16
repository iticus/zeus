function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function processForecast(forecast) {
    let x = [];
    let temperatureLow = {
        y: [], x: x, type: "bar", "name": "Low",
        textposition: "auto", hoverinfo: "none", opacity: 0.9
    }
    let temperatureHigh = {
        y: [], x: x, type: "bar", "name": "High",
        textposition: "auto", hoverinfo: "none", opacity: 0.9
    };
    for (let i = 0; i < forecast.daily.data.length; i++) {
        let item = forecast.daily.data[i];
        x.push(new Date(item.time * 1000));
        temperatureLow.y.push(item.temperatureLow);
        temperatureHigh.y.push(item.temperatureHigh);
    }
    temperatureLow.text = temperatureLow.y.map(String);
    temperatureHigh.text = temperatureHigh.y.map(String);
    //
    // let wind = {y: [], type: "scatter", "name": "Wind", yaxis: "y2"};
    // wind.x = x;
    // let data = [temperature, wind];
    // let layout = {
    //     xaxis: {"tickformat": "%d/%m"},
    //     title: "Weather Forecast for " + forecast.latitude + ", " + forecast.longitude,
    //     yaxis: {title: "Temperature [C]"},
    //     yaxis2: {
    //         title: "Wind [km/h]",
    //         titlefont: {color: "rgb(148, 103, 189)"},
    //         tickfont: {color: "rgb(148, 103, 189)"},
    //         overlaying: "y",
    //         side: "right"
    //     }
    // };
    let data = [temperatureLow, temperatureHigh];
    let layout = {
        title: "Weather Forecast for " + forecast.latitude + ", " + forecast.longitude,
        barmode: "relative",
        xaxis: {"tickformat": "%d %B"},
        yaxis: {title: "Temperature [C]"}
    };
    Plotly.newPlot("temperatureChart", data, layout);
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