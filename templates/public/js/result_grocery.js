$(function(){
    var test_data = [
        { "name": "キャベツ", "value": 100, "shop":"フレスコ", "flyer":"url of flyer1" },
        { "name": "じゃがいも", "value": 200, "shop":"ダックス", "flyer":"url of flyer2"  },
        { "name": "にんじん", "value": 300, "shop":"直売所", "flyer":"url of flyer3"  }
    ];
    var $res = $('#body');


    for(var i in test_data){

        $res.append(`<tr><td>${test_data[i].name}</td>
                        <td>${test_data[i].value}</td>
                        <td>${test_data[i].shop}</td>
                        <td>${test_data[i].flyer}</td></tr>`);
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