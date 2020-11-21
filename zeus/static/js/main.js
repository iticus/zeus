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
    let dailyData = [temperatureLow, temperatureHigh];
    let layout = {
        title: "Weather Forecast for " + forecast.latitude + ", " + forecast.longitude,
        barmode: "relative",
        xaxis: {"tickformat": "%d %B"},
        yaxis: {title: "Temperature [C]"}
    };
    Plotly.newPlot("temperatureChart", dailyData, layout);

    document.getElementById("temperatureChart").on("plotly_click", function(data) {
        let key = data.points[0].x;
        let hourlyTemperature = {y: [], x: [], type: "scatter", "name": "Temperature"}
        let hourlyPrecipitation = {y: [], x: [], type: "scatter", "name": "Precipitation", yaxis: "y2"}
        for (let i = 0; i < forecast.hourly.data.length; i++) {
            let item = forecast.hourly.data[i];
            let d = new Date(item.time * 1000);
            let k = `${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()}`;
            if (key === k) {
                hourlyTemperature.x.push(d);
                hourlyTemperature.y.push(item.temperature);
                hourlyPrecipitation.x.push(d);
                hourlyPrecipitation.y.push(item.precipProbability);
            }
        }
        let hourlyData = [hourlyTemperature, hourlyPrecipitation];
        let layout = {
            title: key,
            xaxis: {"tickformat": "%H:%M"},
            yaxis: {title: "Temperature [C]"},
            yaxis2: {
                title: "Precipitation [%]",
                titlefont: {color: "rgb(148, 103, 189)"},
                tickfont: {color: "rgb(148, 103, 189)"},
                tickformat: ',.0%',
                overlaying: "y",
                side: "right"
            }
        };
        Plotly.newPlot("hourlyChart", hourlyData, layout);
    });
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