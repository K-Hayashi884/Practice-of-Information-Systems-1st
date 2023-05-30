window.addEventListener("load", function () {
    fetchAPI();
    time = getParam("min")
    if(time=="NaN"){
        url = "http://127.0.0.1:8080/recipe?time=10000";
    }else{
        url = "http://127.0.0.1:8080/recipe?time=" + time;
    }


    $.ajax({
        url: url,
        type: 'GET',
        dataTyoe: JSON,
        success: function (result) {
            console.log("献立検索成功");
            append_title(time)
            append_table(result);
            initMap(result);
        },
        error: function (error) {
            console.log(`error ${error}`);
        }
    });
})

function append_title(time) {
    var title = $('#table_title');
    if(time=="NaN"){
        title.text(`おすすめメニュー`);        
    }else{
        title.text(`${time}分以内で完成するメニュー`);
    }

}

function append_table(properties) {
    var table = $('#result_table>tbody');
    properties.forEach(i => {
        var recipeName = i["name"];
        var ingredients = i["ingredients"];
        var storeName = [];
        var flyerUrl = [];
        var time = i["time"];
        i["stores"].forEach(store => {
            storeName.push(store["name"]);
            flyerUrl.push(`<a href=${store["flyer_url"]}>${store["name"]}</a>`);
        });
        var recipeUrl = i["url"];

        var newRow = "<tr>";
        newRow += `<td><a href=${recipeUrl}>${recipeName}</a></td>`;
        newRow += "<td>" + ingredients.join("<br>") + "</td>";
        newRow += "<td>" + time + "</td>";
        newRow += "<td>" + storeName.join("<br>") + "</td>";
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
    if (result == null) return;

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
    })
    makeMarker(map, "現在地", "現在地", lat, lng);

    const infoStores = makeStoreInfoArr(result)
    console.log("重複抜きのリスト");
    console.log(infoStores);
    infoStores.forEach(store => {
        makeMarker(
            map,
            store["storeName"],
            '<a href="' + store["url"] + '">' + store["storeName"] + "</a>",
            parseFloat(store["lat"]),
            parseFloat(store["lng"])
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

function makeStoreInfoArr(result) {//返り値：重複のない店舗情報連想配列
    var arrStores = new Array();
    var nameList = [];
    result.forEach(menu => {
        menu["stores"].forEach(store => {
            var targetName = store["name"]
            var isStoreExists = false;
            for (index in nameList) {
                if (nameList[index] == targetName) {
                    isStoreExists = true;
                    break;
                }
            }
            if (isStoreExists == false) {
                nameList.push(targetName);
                var storeInfo = {
                    storeName: store["name"],
                    url: store["flyer_url"],
                    lat: store["latitude"],
                    lng: store["longitude"]
                };
                arrStores.push(storeInfo);
            }

        })
    });
    return arrStores;

}


window.initMap = initMap;