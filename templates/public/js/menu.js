$(function(){
    url="http://127.0.0.1:8080/recipe"

function append_table (json_file){
    var properties = $.parseJSON(json_file);
    var $res = $('#result_table');
    for(var i in properties){
        $res.append(`<tr><td>${properties[i].ingredients}</td>
                        <td>${properties[i].name}</td>
                        <td>${properties[i].stores}</td>
                        <td>${properties[i].stores}</td></tr>`);
    }

}

    $.ajax({
        url: url,
        type: 'GET',
        dataTyoe : JSON,
        success: function(result){
            console.log(result);
            console.log("成功");
            append_table(result);
        },
        error: function(error){
            console.log(`error ${error}`);
        }
    })


    /*var test_data = [
        { "name": "キャベツ", "value": 100, "shop":"フレスコ", "flyer":"url of flyer1" },
        { "name": "じゃがいも", "value": 200, "shop":"ダックス", "flyer":"url of flyer2"  },
        { "name": "にんじん", "value": 300, "shop":"直売所", "flyer":"url of flyer3"  }
    ]; */

   

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
