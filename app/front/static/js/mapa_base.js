var  IGN_Base = L.tileLayer.wms('https://www.ign.es/wms-inspire/ign-base?', {
    layers: 'IGNBaseTodo-gris',
    maxZoom: 21,
    nombre: "IGN base",
    attribution: '&copy; <a href="https://www.ign.es/web/ign/portal">Instituto Geográfico Nacional</a>'
}),

WMSlayer = L.tileLayer.wms('https://ideg.xunta.gal/servizos/services/Raster/PNOA_2017/MapServer/WmsServer?', {
    layers: '1',
    maxZoom: 21,
    nombre: "WMSlayer",
    attribution: '&copy; <a href="https://cmatv.xunta.gal/organizacion/c/CMAOT_Instituto_Estudos_Territorio">Instituto de Estudos do Territorio</a>'
}),

OpenTopoMap = L.tileLayer('http://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
maxZoom: 21,
nombre: "OpenTopoMap",
attribution: '<a href="https://creativecommons.org/licenses/by-sa/3.0/es/">CC-BY-SA</a> <a href="https://opentopomap.org//">OpenTopoMap</a>'
});

var greenIcon = L.icon({
    iconUrl: 'static/img/mapas/green.png',
    iconSize:     [25, 41],
    iconAnchor:   [12.5, 41],
    popupAnchor:  [0, -30],
    shadowUrl: 'static/img/mapas/rojo_s.png'
});

var blackCircleIcon = L.icon({
iconUrl: 'static/img/mapas/negro_circulo.png',
iconSize:     [10, 10],
    iconAnchor:   [5, 5],
popupAnchor:  [0, 0]
});

var brownCircleIcon = L.icon({
iconUrl: 'static/img/mapas/marron_circulo.png',
iconSize:     [10, 10],
iconAnchor:   [5, 5],
popupAnchor:  [0, 0]
});

var blueCircleIcon = L.icon({
iconUrl: 'static/img/mapas/azul_circulo.png',
iconSize:     [10, 10],
iconAnchor:   [5, 5],
popupAnchor:  [0, 0]
});

var orangeCircleIcon = L.icon({
iconUrl: 'static/img/mapas/naranja_circulo.png',
iconSize:     [10, 10],
iconAnchor:   [5, 5],
popupAnchor:  [0, 0]
});

var greenCircleIcon = L.icon({
iconUrl: 'static/img/mapas/verde_circulo.png',
iconSize:     [10, 10],
iconAnchor:   [5, 5],
popupAnchor:  [0, 0]
});

var lilaCircleIcon = L.icon({
iconUrl: 'static/img/mapas/rosa_circulo.png',
iconSize:     [10, 10],
iconAnchor:   [5, 5],
popupAnchor:  [0, 0]
});

var fucsiaCircleIcon = L.icon({
iconUrl: 'static/img/mapas/fucsia_circulo.png',
iconSize:     [10, 10],
iconAnchor:   [5, 5],
popupAnchor:  [0, 0]
});

var turquesaCircleIcon = L.icon({
iconUrl: 'static/img/mapas/turquesa_circulo.png',
iconSize:     [10, 10],
iconAnchor:   [5, 5],
popupAnchor:  [0, 0]
});

var limaCircleIcon = L.icon({
iconUrl: 'static/img/mapas/lima_circulo.png',
iconSize:     [10, 10],
iconAnchor:   [5, 5],
popupAnchor:  [0, 0]
});

var grisCircleIcon = L.icon({
iconUrl: 'static/img/mapas/gris_circulo.png',
iconSize:     [10, 10],
iconAnchor:   [5, 5],
popupAnchor:  [0, 0]
});

var zoom_inic = 8;
