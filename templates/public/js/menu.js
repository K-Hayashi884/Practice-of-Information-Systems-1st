window.addEventListener("load", function() {
    url="http://127.0.0.1:8080/recipe";

    $.ajax({
        url: url,
        type: 'GET',
        dataTyoe : JSON,
        success: function(result){
            // console.log(result);
            console.log("成功");
            // console.log(result);
            append_table(result);
        },
        error: function(error){
            console.log(`error ${error}`);
        }
    });

    initMap();
})

function append_table (properties){
    //var properties = $.parseJSON(json_file);
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
