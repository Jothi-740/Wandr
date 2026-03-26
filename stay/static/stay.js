const GEOAPIFY_KEY = "5394f0c353f24e0c9a729a76fd125c95";
const UNSPLASH_KEY = "NB21_l97rNLAQbqE8wv_nUqK1xvQYhW7Dlpk0dyMn6k";

function toggleSearch() {
  const input = document.getElementById("radiusInput");
  if (!input) return;

  if (input.classList.contains("active")) {
    getLocation();
  } else {
    input.classList.add("active");
    input.focus();
  }
}

function checkEnter(event) {
  if (event.key === "Enter") {
    getLocation();
  }
}

function getLocation(){
  const container = document.getElementById("hotelContainer");
  if (container) container.innerHTML = "Getting your location...";

  if(navigator.geolocation){
    navigator.geolocation.getCurrentPosition(fetchHotels);
  }else{
    alert("Geolocation not supported");
  }
}


async function fetchHotels(position){

const userLat = position.coords.latitude;
const userLon = position.coords.longitude;

const radiusInput = document.getElementById("radiusInput");
let radiusMeters = 7000; // Default 7km
if (radiusInput && radiusInput.value) {
  const km = parseFloat(radiusInput.value);
  if (!isNaN(km) && km > 0) {
    radiusMeters = km * 1000;
  }
}

const url =
`https://api.geoapify.com/v2/places?categories=accommodation.hotel&filter=circle:${userLon},${userLat},${radiusMeters}&limit=20&apiKey=${GEOAPIFY_KEY}`;

try{

const response = await fetch(url);
const data = await response.json();

displayHotels(data.features,userLat,userLon);

}catch(error){

console.log(error);

}

}


function calculateDistance(lat1,lon1,lat2,lon2){

const R = 6371;

const dLat = (lat2-lat1)*Math.PI/180;
const dLon = (lon2-lon1)*Math.PI/180;

const a =
Math.sin(dLat/2)*Math.sin(dLat/2)+
Math.cos(lat1*Math.PI/180)*
Math.cos(lat2*Math.PI/180)*
Math.sin(dLon/2)*Math.sin(dLon/2);

const c = 2*Math.atan2(Math.sqrt(a),Math.sqrt(1-a));

return R*c;

}


function getHotelImage(index){

const images=[

"https://images.unsplash.com/photo-1566073771259-6a8506099945",
"https://images.unsplash.com/photo-1582719478250-c89cae4dc85b",
"https://images.unsplash.com/photo-1590490360182-c33d57733427",
"https://images.unsplash.com/photo-1578683010236-d716f9a3f461",
"https://images.unsplash.com/photo-1551882547-ff40c63fe5fa",
"https://images.unsplash.com/photo-1520250497591-112f2f40a3f4",
"https://images.unsplash.com/photo-1596394516093-501ba68a0ba6",
"https://images.unsplash.com/photo-1564501049412-61c2a3083791"

];

return images[index % images.length];

}


function displayHotels(hotels,userLat,userLon){

const container = document.getElementById("hotelContainer");

container.innerHTML="";

hotels.sort((a,b)=>{

const d1 = calculateDistance(userLat,userLon,a.properties.lat,a.properties.lon);
const d2 = calculateDistance(userLat,userLon,b.properties.lat,b.properties.lon);

return d1-d2;

});


for(let i=0;i<hotels.length;i++){

const hotel = hotels[i];

const name = hotel.properties.name || "Nearby Hotel";

const lat = hotel.properties.lat;
const lon = hotel.properties.lon;

const distance = calculateDistance(userLat,userLon,lat,lon);

const rating = (Math.random()*2+3).toFixed(1);

const price = Math.floor(Math.random()*2000+1000);

const image = getHotelImage(i);

const card = `

<div class="place-card glass">

<img src="${image}" class="place-img" loading="lazy">

<div class="place-info">

<h3>${name}</h3>

<p>📍 ${distance.toFixed(2)} km</p>

<p class="rating">⭐ ${rating} / 5</p>

<p>₹ ${price}</p>

<button onclick="goRoute(${lat},${lon},'${name}')" class="btn-primary small">Go</button>

</div>

</div>

`;

container.innerHTML += card;

}

}


function goRoute(lat,lon,name){

window.location.href =
`/stay/route/?lat=${lat}&lon=${lon}&name=${encodeURIComponent(name)}`;

}


getLocation();