function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(processLocation);
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
    let y_range = [100, -100];
    for (let i = 0; i < forecast.daily.data.length; i++) {
        let item = forecast.daily.data[i];
        x.push(new Date(item.time * 1000));
        if (y_range[0] > item.temperatureLow)
            y_range[0] = item.temperatureLow
        if (y_range[1] < item.temperatureHigh)
            y_range[1] = item.temperatureHigh
        temperatureLow.y.push(item.temperatureLow);
        temperatureHigh.y.push(item.temperatureHigh);
    }
    y_range[0] -= 2; y_range[1] += 2;
    temperatureLow.text = temperatureLow.y.map(String);
    temperatureHigh.text = temperatureHigh.y.map(String);
    let dailyData = [temperatureHigh, temperatureLow];
    let layout = {
        title: "Temperature",
        colorway : ['#F9C74F', '#277DA1'],
        barmode: "group",
        xaxis: {tickformat: "%d %B"},
        yaxis: {title: "Temperature [C]", autorange: true, range: y_range}
    };
    Plotly.newPlot("temperatureChart", dailyData, layout);

    document.getElementById("temperatureChart").on("plotly_click", function(data) {
        let key = data.points[0].x;
        let hourlyTemperature = {y: [], x: [], type: "line", "name": "Temperature", "line": {"shape": "spline", "smoothing": 1.3}, fill: "tozeroy"}
        let hourlyPrecipitation = {y: [], x: [], type: "line", "name": "Precipitation", yaxis: "y2",  "line": {"shape": "spline", "smoothing": 1.3},  fill: "tozeroy"}
        for (let i = 0; i < forecast.hourly.data.length; i++) {
            let item = forecast.hourly.data[i];
            let d = new Date(item.time * 1000);
            let k = d.toISOString().slice(0,10);
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
            colorway : ['#F9C74F', '#90BE6D'],
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
            let forecastUrl = "/forecast?lat=" + latitude + "&lng=" + longitude;
            fetch(forecastUrl)
                .then(response => response.text())
                    .then(body => {
                        let url = "/forecast?lat=" + latitude + "&lng=" + longitude;
                        processForecast(JSON.parse(body));
                    })
        })
}

document.addEventListener("DOMContentLoaded", () => {
    getLocation();
});