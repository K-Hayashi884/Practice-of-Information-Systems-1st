$(function () {
    url = "http://127.0.0.1:8080/recipe"

    /*$.ajax({
        url: url,
        type: 'GET',
        dataTyoe : JSON,
        success: function(result){
            console.log(result)
            console.log("成功")
        },
        error: function(error){
            console.log(`error ${error}`)
        }
    })*/

    const json = [{ "ingredients": ["\u9d8f\u30e2\u30e2\u8089", "\u5375", "\u307f\u308a\u3093", "\u91a4\u6cb9", "\u7247\u6817\u7c89", "\u304a\u308d\u3057\u30cb\u30f3\u30cb\u30af", "\u304a\u308d\u3057\u751f\u59dc", "\u5869", "\u30ec\u30e2\u30f3\u6c41", "\u63da\u3052\u6cb9", "\u30ec\u30e2\u30f3"], "name": "\u9d8f\u306e\u5510\u63da\u3052", "stores": [{ "flyer_url": "url1", "items": ["\u9d8f\u30e2\u30e2\u8089", "\u5375"], "latitude": 35.07622608, "longitude": 135.7876542, "name": "\u30b3\u30fc\u30d7\u5ca9\u5009", "url_type": 0 }, { "flyer_url": "url3", "items": ["\u304a\u308d\u3057\u30cb\u30f3\u30cb\u30af", "\u304a\u308d\u3057\u751f\u59dc", "\u63da\u3052\u6cb9"], "latitude": 35.07384751, "longitude": 135.7877275, "name": "A\u30b3\u30fc\u30d7\u5ca9\u5009", "url_type": 1 }, { "flyer_url": "url2", "items": ["\u5869", "\u30ec\u30e2\u30f3\u6c41", "\u30ec\u30e2\u30f3"], "latitude": 35.07463776, "longitude": 135.7879421, "name": "\u30a8\u30e0\u30b8\u30fc\u30b7\u30e7\u30c3\u30d7\u5ca9\u5009", "url_type": 1 }], "time": 15, "url": "https://chefgohan.gnavi.co.jp/detail/91" }, { "ingredients": ["\u5375", "\u51fa\u6c41", "\u307f\u308a\u3093", "\u91a4\u6cb9", "\u7802\u7cd6", "\u7247\u6817\u7c89", "\u6cb9", "\u5927\u6839"], "name": "\u5375\u713c\u304d", "stores": [{ "flyer_url": "url1", "items": ["\u5375"], "latitude": 35.07622608, "longitude": 135.7876542, "name": "\u30b3\u30fc\u30d7\u5ca9\u5009", "url_type": 0 }, { "flyer_url": "url3", "items": ["\u6cb9"], "latitude": 35.07384751, "longitude": 135.7877275, "name": "A\u30b3\u30fc\u30d7\u5ca9\u5009", "url_type": 1 }], "time": 10, "url": "https://chefgohan.gnavi.co.jp/detail/90" }, { "ingredients": ["\u9d8f\u30e2\u30e2\u8089", "\u5375", "\u7c73", "\u51fa\u6c41", "\u307f\u308a\u3093", "\u91a4\u6cb9", "\u4e09\u3064\u8449", "\u7c89\u5c71\u6912"], "name": "\u89aa\u5b50\u4e3c", "stores": [{ "flyer_url": "url1", "items": ["\u9d8f\u30e2\u30e2\u8089", "\u5375"], "latitude": 35.07622608, "longitude": 135.7876542, "name": "\u30b3\u30fc\u30d7\u5ca9\u5009", "url_type": 0 }], "time": 10, "url": "https://chefgohan.gnavi.co.jp/detail/89" }]
    var properties = $.parseJSON(json)
    console.log("テスト")

    /*var test_data = [
        { "name": "キャベツ", "value": 100, "shop":"フレスコ", "flyer":"url of flyer1" },
        { "name": "じゃがいも", "value": 200, "shop":"ダックス", "flyer":"url of flyer2"  },
        { "name": "にんじん", "value": 300, "shop":"直売所", "flyer":"url of flyer3"  }
    ];*/

    var $res = $('#body');
    for (var i in properties) {

        $res.append(`<tr><td>${properties[i].ingredients}</td>
                        <td>${properties[i].name}</td>
                        <td>${properties[i].stores}</td>
                        <td>${properties[i].stores}</td></tr>`);
    }

})




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