window.addEventListener("load", function () {
    fetchAPI();
    url = "http://127.0.0.1:8080/store?name=";

    $.ajax({
        url: url,
        type: 'GET',
        dataTyoe: JSON,
        success: function (result) {;
            initMap(result);
        },
        error: function (error) {
            console.log(`error ${error}`);
        }
    });
})

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

function fetchAPI(){
    var sc = document.createElement('script');
    sc.src = "https://maps.googleapis.com/maps/api/js?key="+conf.apikey+"&callback=initMap";
    sc.async = true;
    document.body.appendChild(sc);
}

function initMap(result) {
    if(result == null)return;
    var lat = 35.027221289790276;//京大
    var lng = 135.78074403227868;

    function success(pos) {
        lat = pos.coords.latitude;
        lng = pos.coords.longitude;
    }
    function fail(error) {
        alert('位置情報の取得に失敗しました。エラーコード：' + error.code);
    }
    navigator.geolocation.getCurrentPosition(success, fail);

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: {lat:lat, lng:lng},
    });

    makeMarker(map, "現在地", "現在地", lat, lng);
    result.forEach(i => {
        makeMarker(
            map,
            i["name"],
            '<a href="'+(window.location.hostname + window.location.pathname).replace("/top", "/result_store") + '?store_name='+i["name"]+'">'+i["name"]+"</a>",
            i["latitude"],
            i["longitude"]
        );
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