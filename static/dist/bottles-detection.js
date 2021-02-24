 
 
 var map = L.map('map'),
    //realtime = L.realtime('https://41.190.131.190:5000/gps/', {
    realtime = L.realtime('https://wanderdrone.appspot.com/', { 
	
        interval: 300000 * 1000
    });//.addTo(map);

var bounds = [[0,0], [9.1021, 18.2812]];
map.fitBounds(bounds, {maxZoom: 3});
//map.dragging.disable()

//var map = L.map('map').setView([8.7832, 34.5085], 13);

map.options.minZoom = 2;

function bottles(){
			
	var planes = [
		["Nsazi", 3000,0.0964, 32.5572],
		["Koome",2100,-0.0850, 32.7500],
		["Zinga",2000,0.0188889, 32.2372],
		["Damba",1800,0.0039, 32.7915],
		["Namalusu",1600,0.2705, 32.6581],
		["Nakiwogo",1000,0.08192, 32.45469],
		["Bukasa",800,0.2989, 32.6207],
		["Ssese",700,-0.4333, 32.2500]];
		
	colors = ["blue", "orange", "magenta", "green", "yellow", "Cinnabar", "red", "brown", "olive"];	
	
	var total = 0;
	for (var i = 0; i < planes.length; i++) {
			total += planes[i][1];
	}
	
	var size=0;
	for (var i = 0; i < planes.length; i++) {
			size = (planes[i][1]/total)*100;
			//L.circleMarker([planes[i][2],planes[i][3]],{ color: colors[i], radius: size } ).addTo(map).bindPopup("<b>"+planes[i][0]+"<br><strong>Bottles Detected: </strong>"+planes[i][1]);
	        L.circleMarker([planes[i][2],planes[i][3]],{ color: "red", radius: size } ).addTo(map).bindPopup("<b>"+planes[i][0]+"<br><strong>Bottles Detected:</strong>"+planes[i][1]);
			//marker = new L.marker([planes[i][1],planes[i][2]])
			//	.bindPopup(planes[i][0])
			//	.addTo(map);
			//polyline = L.polyline([planes[i][2],planes[i][3]]).addTo(map);
		}
		
}

function pampers(){
	var planes = [
		["Nsazi", 3000,0.0964, 32.5572],
		["Koome",2100,-0.0850, 32.7500],
		["Zinga",2000,0.0188889, 32.2372],
		["Damba",1800,0.0039, 32.7915],
		["Namalusu",1600,0.2705, 32.6581],
		["Nakiwogo",1000,0.08192, 32.45469],
		["Bukasa",800,0.2989, 32.6207],
		["Ssese",700,-0.4333, 32.2500]];
		
	colors = ["blue", "orange", "magenta", "green", "yellow", "Cinnabar", "red", "brown", "olive"];	
	
	var total = 0;
	for (var i = 0; i < planes.length; i++) {
			total += planes[i][1];
	}
	
	var size=0;
	for (var i = 0; i < planes.length; i++) {
			size = (planes[i][1]/total)*100;
	        L.circleMarker([planes[i][2],planes[i][3]],{ color: "orange", radius: size } ).addTo(map).bindPopup("<b>"+planes[i][0]+"<br><strong>Pampers Detected:</strong>"+planes[i][1]);
		}
	}

function polythenebags(){
	var planes = [
		["Nsazi", 3000,0.0964, 32.5572],
		["Koome",2100,-0.0850, 32.7500],
		["Zinga",2000,0.0188889, 32.2372],
		["Damba",1800,0.0039, 32.7915],
		["Namalusu",1600,0.2705, 32.6581],
		["Nakiwogo",1000,0.08192, 32.45469],
		["Bukasa",800,0.2989, 32.6207],
		["Ssese",700,-0.4333, 32.2500]];
		
	colors = ["blue", "orange", "magenta", "green", "yellow", "Cinnabar", "red", "brown", "olive"];	
	
	var total = 0;
	for (var i = 0; i < planes.length; i++) {
			total += planes[i][1];
	}
	
	var size=0;
	for (var i = 0; i < planes.length; i++) {
			size = (planes[i][1]/total)*100;
	        L.circleMarker([planes[i][2],planes[i][3]],{ color: "green", radius: size } ).addTo(map).bindPopup("<b>"+planes[i][0]+"<br><strong>Polythene Bags Detected:</strong>"+planes[i][1]);
		}
}
	
   setInterval(function(){ 
    //var x = myFunction(4, 3); 
    //console.log(x);
	var xhr = new XMLHttpRequest();
	xhr.open('get', 'https://wanderdrone.appspot.com/');
	xhr.send();
	  
	xhr.onload = function() {
		var d = xhr.response;
		var de = JSON.parse(d);
		var coord = de["geometry"]["coordinates"];
		//L.circleMarker([0.3252622,32.5752037],{ color: 'blue', radius: 10.0 } ).addTo(map).bindPopup("<b> <br><strong>Bottles Detected: </strong>1");
		//L.circleMarker([0.3252622,32.5752037],{ color: 'blue', radius: 10.0 } ).addTo(map).bindPopup("<b>Bukasa <br><strong>Bottles Detected: </strong>800");
	  };
	 
	}, 8000);

   L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">Water</a> Pollutants'
   }).addTo(map);

   realtime.on('update', function() {
    map.fitBounds(realtime.getBounds(), {maxZoom: 3});
   });
   
   map.addControl( new L.Control.Search({
		url: 'https://nominatim.openstreetmap.org/search?format=json&q={s}',
		jsonpParam: 'json_callback',
		propertyName: 'display_name',
		propertyLoc: ['lat','lon'],
		marker: L.circleMarker([0,0],{radius:30}),
		autoCollapse: true,
		autoType: false,
		minLength: 2
	}) );
	
	this.map = new Map('mapId', {attributionControl: false});
    L.esri.basemapLayer('Topographic').addTo(map);