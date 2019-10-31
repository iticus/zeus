function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    let latitude = position.coords.latitude;
    let longitude =  position.coords.longitude;
    let url = "/forecast?lat=" + latitude + "&lng=" + longitude;
    fetch(url)
        .then(response => response.text())
        .then(body => {
            let element = document.querySelector("#result");
            element.innerHTML = "<pre>" + JSON.stringify(JSON.parse(body), null, 4) + "</pre>";
        })
}

document.addEventListener("DOMContentLoaded", () => {
    getLocation();
});