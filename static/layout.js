var places;
places = ["loznice","chodba","schody"]
var timer;
var edited = false;

function rgb2hex(rgb){
	rgb = rgb.match(/^rgba?[\s+]?\([\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?/i);
	return (rgb && rgb.length === 4) ? "#" +
		("0" + parseInt(rgb[1],10).toString(16)).slice(-2) +
		("0" + parseInt(rgb[2],10).toString(16)).slice(-2) +
		("0" + parseInt(rgb[3],10).toString(16)).slice(-2) : '';
}

function addPlace(place){
	var td;
	td = document.getElementById(place);
	var input = document.createElement('input');
	input.id = place+"-picker";
	input.type = "color";
	var changed = document.createElement('p');
	changed.id = place+"-changed";
	changed.classList.add('changed');
	td.appendChild(changed); 
	td.appendChild(input);
}

function loaded(){
	places.forEach(addPlace);
	refresh();
	timer = window.setInterval(refresh,1000);

}

function refresh(){
	$.ajax({
		dataType:"json",
		url:"/state/",
		success:updateColors
	});
}

function updateColors(data){
	data.forEach(function (place){
		var picker;
		var td;
		var changed;
		changed = document.getElementById(place.name+"-changed");
		picker = document.getElementById(place.name+"-picker");
		td = document.getElementById(place.name);
		if (!edited){
			picker.value = place.color;
		}
		if (place.changed){
			changed.innerHTML = 'changed';	
		} else {
			changed.innerHTML = '';	
		}
		td.style.backgroundColor = place.color;
	});
	edited = true;
}

function setColors(){
	places.forEach(function (place){
		var picker;
		var td;
		picker = document.getElementById(place+"-picker");
		td = document.getElementById(place);
		if (picker.value != rgb2hex(td.style.backgroundColor)){
			setColor(place,picker.value);	
		}
	});	
}

function setColor(place,color){
	$.ajax({
		url:"/set?name="+place+"&color="+color.substring(1)	
	});	
}

function resetColors(){
	places.forEach(function (place){
		var picker;
		var td;
		picker = document.getElementById(place+"-picker");
		td = document.getElementById(place);
		picker.value = rgb2hex(td.style.backgroundColor);
	});	
}


		


window.onload = loaded;
