function initAutocomplete() {
	var inputs = document.getElementsByClassName("autocomplete");
	const options = {
	  componentRestrictions: { country: "tr" },
	  fields: ["address_components", "geometry", "icon", "name"],
	  strictBounds: false,
	};
	for(var i=0;i<inputs.length;i++){
		new google.maps.places.Autocomplete(inputs[i], options);
	}
}