
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

    window.location.href = (window.location.hostname + window.location.pathname).replace("/top", "/menu") + `?min=${resMin}`;
};

function groceryOnClick() {
    let element = document.getElementById('search_grocery');
    var value = element.value;
    window.location.href = (window.location.hostname + window.location.pathname).replace("/top", "/result_grocery") + `?grocery_name=${value}`;
};
function storeOnClick() {
    let element = document.getElementById('search_store');
    var value = element.value;
    window.location.href = (window.location.hostname + window.location.pathname).replace("/top", "/result_store") + `?store_name=${value}`;
};

function initMap() {

    function success(pos) {
        var lat = pos.coords.latitude;
        var lng = pos.coords.longitude;
        var latlng = new google.maps.LatLng(lat, lng); //中心の緯度, 経度
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 15,
            center: latlng
        });
        makeMarker(map, "現在地", "現在地", lat, lng);

    }

    function fail(error) {
        alert('位置情報の取得に失敗しました。エラーコード：' + error.code);
        var latlng = new google.maps.LatLng(35.027221289790276, 135.78074403227868); //京大
        var map = new google.maps.Map(document.getElementById('maps'), {
            zoom: 10,
            center: latlng
        });
    }
    navigator.geolocation.getCurrentPosition(success, fail);

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: myLatlng,
    });
}

function makeMarker(map, title, href, lat, lng) {
    const marker = new google.maps.Marker({
        position: { lat: lat, lng: lng },
        map,
        title: title,
    });
    const contentString = href;
    const infowindow = new google.maps.InfoWindow({
        content: contentString,
        arialabel: title,
    });
    marker.addListener("click", () => {
        infowindow.open({
            anchor: marker,
            map,
        });
    });
    marker.addListener("closeclick", () => {
        infowindow.close({});
    });
    return marker;
}

window.initMap = initMap;