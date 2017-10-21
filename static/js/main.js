function initMap() {
      
  function mapMaker(location){
   
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 9,
        center: {lat:pos.lat,lng:pos.lng}
      });
      // var marker;
      for (var i = 0; i < myplaces.length; i++) {
  let infowindow = new google.maps.InfoWindow({
  content: myname[i][1]
  });
  
  let marker = new google.maps.Marker({
            position: myplaces[i],
            map: map,
            title:myname[i][0]     
        });
        marker.addListener('click',function(){
                infowindow.open(map,marker);
              })
    }//end of for loop
  

  }

  }