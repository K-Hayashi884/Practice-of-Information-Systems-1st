window.addEventListener("load", function () {
    store_name = getParam("store_name")
    url = "http://127.0.0.1:8080/store?name="+store_name;

    $.ajax({
        url: url,
        type: 'GET',
        dataTyoe: JSON,
        success: function (result) {
            console.log("店情報の検索成功");
            append_table(result);
        },
        error: function (error) {
            console.log(`error ${error}`);
        }
    });

    initMap();
})

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