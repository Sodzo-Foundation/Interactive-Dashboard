   var geojson;

    // Lat/Long for Prague
    var lat = 50.0755381;
    var long = 14.43780049999998;
	
	var lat = 0.347596;
	var long = 32.582520;

    var mymap = L.map('mapid').setView([lat, long], 13); //([51.505, -0.09], 13);
	

	//mymap.dragging.disable();
   L.tileLayer('  https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibmlja255ciIsImEiOiJjajduNGptZWQxZml2MndvNjk4eGtwbDRkIn0.L0aWwfHlFJVGa-WOj7EHaA', {
      attribution: 'Map data &copy; <a href="#">Sodzo Foundation</a> <a href="#">Water Pollutants</a>',
      maxZoom: 41,
      minZoom: 7,
      id: 'mapbox.dark'
    }).addTo(mymap);
	/*
	L.easyButton( 'glyphicon-star', function(){
  alert('you just clicked a glyphicon');
}).addTo(mymap);

	L.easyButton( '<span class="star">&starf;</span>', function(){
		alert('you just clicked the html entity \&starf;');
		}).addTo(mymap);
	
	*/
	var circleOptions = {
		color: 'red',
		opacity: 1,
		 weight: 1,
		fillColor: '#f03',
		fillOpacity: 0
		}
	
	var circleCenter = [0.0964, 32.5572];
	var layers=[];

	/*
	var planes = [
		[3000,0.0964, 32.5572],
		[2100,-0.0850, 32.7500],
		[2000,0.0188889, 32.2372],
		[1800,0.0039, 32.7915],
		[1600,0.2705, 32.6581],
		[1000,0.08192, 32.45469],
		[800,0.2989, 32.6207],
		[700,-0.4333, 32.2500]];
		
	colors = ["blue", "orange", "magenta", "green", "yellow", "Cinnabar", "red", "brown", "olive"];	
	
	var total = 0;
	for (var i = 0; i < planes.length; i++) {
			total += planes[i][1] * 10;
	}
	
	var size=0;
	for (var i = 0; i < planes.length; i++) {
			//size = (planes[i][0]/total)*100;
			size = planes[i][0];
	        L.circle([planes[i][1],planes[i][2]],size, circleOptions).addTo(mymap);
		}
	*/	

    mymap.panTo(new L.LatLng(lat, long));
    function getColor(d) {
      return d > 1000000 ? '#005824' :
          d > 500000  ? '#238b45' :
          d > 200000  ? '#41ae76' :
          d > 100000  ? '#66c2a4' :
          d > 50000   ? '#99d8c9' :
          d > 20000   ? '#ccece6' :
          d > 15000   ? '#edf8fb':
                       'snow'
    }
	
	mymap.setZoom(7);	
	
	var c = mymap.getContainer();
	c.style.overflow = 'hidden';
    function style(feature) {
      return {
          fillColor: getColor(feature.properties.gdp_md_est),
          weight: 1,
          opacity: 2,
          color: 'snow',
          fillOpacity: .7,
		  fill: 'red',
          //stroke: true,
          //weight: .7,
          //fill: true,
          //clickable: true
      };
    }
	

/*
// Set style function that sets fill color property
function style(feature) {
    return {
        fillColor: '#004691', 
        fillOpacity: 0.5,  
        weight: 1,
        opacity: 1,
        color: '#424a44',
        dashArray: '1'
    };
}
*/

    // Happens on mouse hover
    function highlight(e) {
      var layer = e.target;
	  
	  //L.remove();
	  
	
    layer.setStyle({
          weight: 1,  //colour boiling over 
          color: '#802b1a',//#ffd32a', // colour of background
          dashArray: '',
          fillOpacity: 1.7 // concentration of background colour
      });
	  //var count="20,000";
	  
	  //this.markers.clear();
		 
	  layer.bindPopup("<strong>"+layer.feature.properties.count+"</strong><br/>bottles originating from <br/><strong>" + layer.feature.properties.name + "</strong>").openPopup();
	  	  
	

      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          layer.bringToFront();
      }

      //displayInfo.update(layer.feature.properties);
    }

    // Happens on mouse out
    function reset(e) {
	//var circleCenter = [0.0964, 32.5572];
	  //this.marker = L.circleMarker(circleCenter, 50000, circleOptions).addTo(mymap);
      geojson.resetStyle(e.target);
      //displayInfo.update();
	  
	  
    }
	
	
    // Click listener that zooms to country
    function zoomToCountry(e) {
      mymap.fitBounds(e.target.getBounds());

    }

	var myStyle = { // Define the boundary lines of countries
    "color": "#dddddd0d"//"#ddd"
	};
	
    function onEachFeature(feature, layer) {
      layer.on({
          mouseover: highlight,
          mouseout: reset,
          click: zoomToCountry,
		  /*click: function () {
           layer.bindPopup('<p>' + layer.feature.properties.name + '</p><p>' + layer.feature.properties.density + '</p>').openPopup()
                } */
		  
      });
    }

    geojson = L.geoJson(countriesData, {
        style: myStyle,
        onEachFeature: onEachFeature
    }).addTo(mymap);



    // Legend
    var legend = L.control({
      position: 'bottomright'
      }
    );
	
    //legend.addTo(mymap);








   setInterval(function(){ 
    //var x = myFunction(4, 3); 
    //console.log(x);
	var xhr = new XMLHttpRequest();
	//xhr.open('get', 'https://wanderdrone.appspot.com/');
	xhr.open('get', '/mapupdate');
	xhr.send();
	  
	xhr.onload = function() {
		var d = xhr.response;
		var de = JSON.parse(d);
		var size=0;
		//var coord = de["geometry"]["coordinates"];
		console.log(8888888888888888);
		console.log(de);
		var json = de['latest_results_list'];
		//var a = [0.0964, 32.5572];

		for (var i in json) {
			size = json[i][3] * 70;
			
			//console.log(json[i][0], json[i][0], json[i][0]);
			
			L.circle([json[i][2],json[i][3]],size, circleOptions).addTo(mymap).bindPopup("<b>"+json[i][0]+"<br><strong>Bottles Detected: </strong>"+json[i][1]);
			
			//a.push.apply(a, [json[i][2],json[i][3]]);
			
			
		}
		//L.circleMarker(coord,{ color: 'blue', radius: 10.0 } ).addTo(map).bindPopup("<b>Bukasa <br><strong>Bottles Detected: </strong>800");
	  };
	 
	}, 20000);

	/*
	var markerGroup = L.layerGroup([
      L.marker([37.8, -91]), L.marker([38.8, -86]), L.marker([47.8, -106]),
      L.marker([31.8, -90]), L.marker([39.8, -96]), L.marker([33.8, -100]) ]);
	*/
	
	var markerGroup = L.layerGroup();

//bottle
var toggle = L.easyButton({
  states: [{
    stateName: 'add-bottles',
    icon: '<img src="https://www.flaticon.com/premium-icon/icons/svg/2745/2745070.svg" style="width:20px">',
    title: 'Bottles',
    onClick: function(control) {
	  //L.addTo(mymap);
      mymap.addLayer(markerGroup);
      
	  control.state('remove-bottles');
	  
	  //btn.state('remove-markers'); 
    }
  }, {
    icon: '<img src="https://www.flaticon.com/premium-icon/icons/svg/2951/2951247.svg" style="width:20px">',
    stateName: 'remove-bottles',
    onClick: function(control) {
      mymap.removeLayer(L);//markerGroup);
	  control.state('add-bottles');
	  
	  //btn.state('add-markers');
    },
    title: 'Remove bottles'
  }]
});
toggle.addTo(mymap);




//pampers
var toggle = L.easyButton({
  states: [{
    stateName: 'add-pampers',
    icon: '<img src="https://as2.ftcdn.net/jpg/01/52/27/51/500_F_152275131_InTFlkEDKrvkGLDIj1e0KLghnXWOuWR3.jpg" style="width:20px">',
    title: 'Pampers',
    onClick: function(control) {
      mymap.addLayer(markerGroup);
	  control.state('remove-pampers');
	  //btn.state('remove-markers'); 
    }
  }, {
    icon: '<img src="https://www.flaticon.com/premium-icon/icons/svg/2951/2951247.svg" style="width:20px">',
    stateName: 'remove-pampers',
    onClick: function(control) {
      mymap.removeLayer(markerGroup);
      control.state('add-pampers');
	  //btn.state('add-markers');
    },
    title: 'Remove pampers'
  }]
});
toggle.addTo(mymap);






//plastic
var toggle = L.easyButton({
  states: [{
    stateName: 'add-plastic',
    icon: '<img src="https://as2.ftcdn.net/jpg/01/69/94/29/500_F_169942978_kFhWOS9AtDf3XVljAmNMNy7hzctWxwHX.jpg" style="width:20px">',
    title: 'Plastic bags',
    onClick: function(control) {
      mymap.addLayer(markerGroup);
      control.state('remove-plastic');
	  //btn.state('remove-markers'); 
    }
  }, {
    icon: '<img src="https://www.flaticon.com/premium-icon/icons/svg/2951/2951247.svg" style="width:20px">',
    stateName: 'remove-plastic',
    onClick: function(control) {
      mymap.removeLayer(markerGroup);
      control.state('add-plastic');
	  //btn.state('add-markers');
    },
    title: 'Remove plastic bags'
  }]
});
toggle.addTo(mymap);


/*
L.easyButton('<img src="https://www.flaticon.com/premium-icon/icons/svg/2745/2745070.svg" style="width:16px">', function(btn, map){
    //helloPopup.setLatLng(map.getCenter()).openOn(mymap);
	mymap.addLayer(markerGroup);
}).addTo(mymap);


L.easyButton('<img src="bottle.png" style="width:16px">', function(btn, map){
    //helloPopup.setLatLng(map.getCenter()).openOn(mymap);
	mymap.addLayer(markerGroup);
}).addTo(mymap);


L.easyButton('<img src="https://www.flaticon.com/premium-icon/icons/svg/2745/2745070.svg" style="width:26px">', function(btn, map){
    //helloPopup.setLatLng(map.getCenter()).openOn(mymap);
	mymap.addLayer(markerGroup);
}).addTo(mymap);

*/