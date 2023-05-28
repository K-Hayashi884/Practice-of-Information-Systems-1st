window.addEventListener("load", function () {
    fetchAPI();
    grocery_name = getParam("grocery_name")
    url = "http://127.0.0.1:8080/item?name="+grocery_name;

    $.ajax({
        url: url,
        type: 'GET',
        dataTyoe: JSON,
        success: function (result) {
            console.log("商品情報検索成功");
            append_title(grocery_name)
            append_table(result);
            initMap(result);
        },
        error: function (error) {
            console.log(`error ${error}`);
        }
    });
})

function append_title(grocery_name){
    var title = $('#table_title');
    title.append(grocery_name + " (商品名)の検索結果一覧")
}

function append_table(properties) {
    var table = $('#result_table>tbody');
    properties.forEach(i => {
        var storeName = i["name"];
        var items = i["items"];
        var flyerUrl = i["flyer_url"];
        var newRow = "<tr>";
        newRow += `<td><a href=${flyerUrl}>${storeName}</a></td>`;
        newRow += "<td>" + items.join("<br>") + "</td>";
        newRow += "</tr>"

        table.append(newRow);
    });

}

function getParam(name) {
    url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return "";
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function fetchAPI(){
    var sc = document.createElement('script');
    sc.src = "https://maps.googleapis.com/maps/api/js?key="+conf.apikey+"&callback=initMap";
    sc.async = true;
    document.body.appendChild(sc);
}

function initMap(result) {
    if(result == null)return;
    const myLatlng = { lat: 35.027221289790276, lng: 135.78074403227868 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: myLatlng,
    })
    makeMarker(map,"現在地", "現在地", myLatlng.lat, myLatlng.lng);
    result.forEach(i => {
        makeMarker(
            map,
            i["name"],
            '<a href="'+i["flyer_url"]+'">'+i["name"]+"</a>",
            i["latitude"],
            i["longitude"]
        );
    });
}

function makeMarker(map,title,href,lat,lng){
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