var position = L.layerGroup();
var userMarker=L.marker([42.88043950138168, -8.545687906444074], {icon: greenIcon})
.addTo(position)
.bindPopup('Esta é a túa posición actual');

var mymap = L.map('mapid',{
  layers: [IGN_Base, position, grupoEnsaios],
  minZoom: 7,
  zoomControl: false,
  tap: false
}).setView([{{traballo.latitud}}, {{traballo.longitud}}], 18);

var baseLayers = {
"Mapa base": IGN_Base,
"Ortofoto" : WMSlayer,
"OpenTopoMap": OpenTopoMap
};

var overlayMaps = {
  "<img src='static/img/mapas/green.png' style='height: 20px; vertical-align:top;' /> Usuario": position,
  "<img src='static/img/mapas/naranja_circulo.png' style='height: 10px' /> Ensaios": grupoEnsaios
};

var colapsado = true
var leyenda = L.control.layers(baseLayers, overlayMaps, {hideSingleBase:true, collapsed:colapsado, position:'topright' })
.addTo(mymap);

function centrarMapa(geometria) {
  if (geometria[0].length == 2) {
    mymap.fitBounds(geometria);
  } else {
    mymap.setView([geometria[0], geometria[1]], 15)
  }
};

function centrarObjeto(id) {
  mymap.setView(window["e"+id]._latlng, 15);
  window["e"+id].openPopup()
};
