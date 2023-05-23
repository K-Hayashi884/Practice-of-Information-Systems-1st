$(function(){
    const url=
    $('#btn-store').click(function(){
        $.ajax({
            url: url,
            type: "Get",
            success: function(result){
                console.log(result);
            },
            error: function(error){
                console.log(`error ${error}`);
            }

        });
    });
    $('.copy-txt').text('jqueryは起動中');
});

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