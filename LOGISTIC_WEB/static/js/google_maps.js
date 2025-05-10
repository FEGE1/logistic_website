var receiving_address = receiving;
var destination_address = destination;
var search_address;
var search_start_address;
var search_end_address;

if(receiving_address && destination_address){
  search_start_address = receiving_address;
  search_end_address = destination_address;
}

// Initialize and add the map
let map;
let marker;
let infoWindow;

async function initMap() {
  // Request needed libraries.
  //@ts-ignore
  
  const [{ Map }, { AdvancedMarkerElement }] = await Promise.all([
    google.maps.importLibrary("marker"),
    google.maps.importLibrary("places"),
  ]);
  const directionsService = new google.maps.DirectionsService(); //
  const directionsRenderer = new google.maps.DirectionsRenderer(); //

  // Initialize the map.
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 38.963745, lng: 35.243322 },
    zoom: 6,
    mapId: "4504f8b37365c3d0",
    mapTypeControl: false,
  });

  directionsRenderer.setMap(map); //

  const onChangeHandler = function () {  //
    calculateAndDisplayRoute(directionsService, directionsRenderer);//
  };//

  // Create the marker and infowindow
  marker = new google.maps.marker.AdvancedMarkerElement({
    map,
  });

  if(search_start_address && search_end_address){
      onChangeHandler();
  }

  function initAutocomplete() {
    const input = document.getElementsByClassName("autocomplete")[0];
    const options = {
      componentRestrictions: { country: "tr" },
      fields: ["address_components", "geometry", "icon", "name","formatted_address"],
      strictBounds: false,
    };
    const autocomplete = new google.maps.places.Autocomplete(input, options);
    autocomplete.addListener("place_changed", function(){
      const place = autocomplete.getPlace();
      if(input['id']=="receiving-address"){
        search_start_address = place.formatted_address;
      }
      else{
        search_end_address = place.formatted_address;
      }
      
      onChangeHandler();
    })
    }

  // Autocomplete
  initAutocomplete();
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {//
  directionsService
    .route({
      origin: {
        query: search_start_address,
      },
      destination: {
        query: search_end_address,
      },
      travelMode: google.maps.TravelMode.DRIVING,
      avoidHighways: true,
    })
    .then((response) => {
      directionsRenderer.setDirections(response);
    })
    .catch((e) => window.alert("Directions request failed due to " + status));
}//

initMap();

// Autocomplete
function initAutocomplete() {
	const input = document.getElementById("autocomplete");
	const options = {
	  componentRestrictions: { country: "tr" },
	  fields: ["address_components", "geometry", "icon", "name"],
	  strictBounds: false,
	};
	const autocomplete = new google.maps.places.Autocomplete(input, options);
  autocomplete.addListener("place_changed", function(){
    search_end_address = this.value;
    onChangeHandler();
  })
  }