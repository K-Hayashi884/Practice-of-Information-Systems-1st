
// const url =
function timeOnClick() {
    let element = document.getElementById('time');
    var value = element.value.split(":");
    var targetHour = parseInt(value[0]);
    var targetMin = parseInt(value[1])
    var now = new Date();
    var target = new Date();
    target.setHours(targetHour, targetMin);
    if (now > target) {
        target.setDate(target.getDate() + 1);
    }
    var resMilliSec = target - now;
    var resMin = parseInt(resMilliSec / 1000 / 60);

    window.location.href = (window.location.hostname + window.location.pathname).replace("top", "menu") + `?min=${resMin}`;
};

function initMap() {
    const myLatlng = { lat: 35.027221289790276, lng: 135.78074403227868 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: myLatlng,
    });
    const marker = new google.maps.Marker({
        position: myLatlng,
        map,
        title: "here!",
    });
    const contentString = "You are here!";
    const infowindow = new google.maps.InfoWindow({
        content: contentString,
        arialabel: "here",
    });

    marker.addListener("click", () => {
        infowindow.open({
            anchor: marker,
            map,
        });
    });
    marker.addListener("closeclick", () => {
        infowindow.close({
        });
    });
}

window.initMap = initMap;