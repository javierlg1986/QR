mymap.on('click', function (e) {
	if (geoposactivado == 0) {
		latlng = L.latLng(e.latlng);
		userMarker.addTo(position)
		userMarker.setLatLng (latlng).bindPopup("Posición establecida manualmente.");
	};
});

var geoposactivado = 0;
var positionId;
var latlng;

function success (pos) {
    latlng = {"lat": pos.coords.latitude, "lng": pos.coords.longitude}
    userMarker
      .setLatLng(latlng)
      .bindPopup(
        `Latitude: ${pos.coords.latitude.toFixed(4)}<br>` +
        `Lonxitude: ${pos.coords.longitude.toFixed(4)}<br>` 
      );
}
function error (err) {
}

function getPosition() {

  if (geoposactivado == 1) {
      navigator.geolocation.clearWatch(positionId);
      geoposactivado=0;
  }

  else if (geoposactivado == 0) {
      geoposactivado=1 
      //Toma la posición, la guarda en variables
      options = {enableHighAccuracy: true, timeout: 5000, maximumAge: 10000}
      if (navigator.geolocation) {
        positionId = navigator.geolocation.watchPosition (success, error, options);
      }
      else{
          console.log("Tu navegador no soporta la API de Geoposicionamiento.");
      }
  }
}

getPosition();