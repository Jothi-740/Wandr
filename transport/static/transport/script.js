let userLat, userLng;
let map;
let markers = [];
let routingControl = null;

/* Get user location */
function getLocation(callback) {

  if (navigator.geolocation) {

    navigator.geolocation.getCurrentPosition(function (position) {

      userLat = position.coords.latitude;
      userLng = position.coords.longitude;

      callback();

    }, function () {

      alert("Please allow location access.");

    });

  }

}

/* Initialize map */
function initMap() {

  if (!map) {

    map = L.map('map').setView([userLat, userLng], 14);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19
    }).addTo(map);

    L.marker([userLat, userLng]).addTo(map)
      .bindPopup("You are here")
      .openPopup();

  }

}

/* Distance calculator */
function calculateDistance(lat1, lon1, lat2, lon2) {

  const R = 6371;

  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return (R * c).toFixed(2);

}

/* Fetch data from Overpass API */
async function fetchOverpassData(query, label) {

  const response = await fetch("https://overpass-api.de/api/interpreter", {
    method: "POST",
    body: query
  });

  const data = await response.json();

  displayResults(data.elements, label);

}

/* Show transport options */
function showTransportOptions() {

  document.getElementById("transportOptions").style.display = "block";

}

/* BUS STOPS */
function getBus() {

  document.getElementById("status").innerText = "Finding bus stops...";

  getLocation(function () {

    initMap();

    const query =
      `[out:json];node["highway"="bus_stop"](around:3000,${userLat},${userLng});out;`;

    fetchOverpassData(query, "Bus Stop");

  });

}

/* RAILWAY STATIONS */
function getTrain() {

  document.getElementById("status").innerText = "Finding railway stations...";

  getLocation(function () {

    initMap();

    const query =
      `[out:json];node["railway"="station"](around:3000,${userLat},${userLng});out;`;

    fetchOverpassData(query, "Railway Station");

  });

}

/* Display results */
function displayResults(places, typeLabel) {

  const resultsDiv = document.getElementById("results");

  resultsDiv.innerHTML = "";

  document.getElementById("main-layout").style.display = "flex";
  document.getElementById("right-title").innerText = `Nearby ${typeLabel}s`;

  // Hide category cards after a selection
  const categoryContainer = document.getElementById("categoryContainer");
  if (categoryContainer) {
    categoryContainer.style.display = "none";
  }

  // Hide map initially when clicking a category
  document.querySelector(".left-panel").style.display = "none";
  document.querySelector(".right-panel").style.width = "100%";

  /* Set limit based on type */
  let limit = 12;
  if (typeLabel === "Bus Stop" || typeLabel === "Railway Station") {
    limit = 3;
  }
  const displayCount = Math.min(places.length, limit);

  /* Update status */
  document.getElementById("status").innerText =
    `Found ${displayCount} places near you`;

  /* Clear old markers */
  markers.forEach(m => map.removeLayer(m));
  markers = [];

  /* Limit results */
  places.slice(0, limit).forEach((place, index) => {

    const name = place.tags?.name || "Unnamed Place";

    const lat = place.lat;
    const lon = place.lon;

    const dist = calculateDistance(userLat, userLng, lat, lon);

    /* Image selection */
    const busImgs = [
      "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400",
      "https://images.unsplash.com/photo-1494515843206-f3117d3f51b7?w=400",
      "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=400",
      "https://images.unsplash.com/photo-1560945781-a67b936d0b67?w=400",
      "https://images.unsplash.com/photo-1621245781223-9388334442df?w=400",
      "https://images.unsplash.com/photo-1528728329032-2972f65dfb3f?w=400"
    ];
    const trainImgs = [
      "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=400",
      "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=400",
      "https://images.unsplash.com/photo-1520101244465-9b244f0ce803?w=400",
      "https://images.unsplash.com/photo-1533100652599-fb9baeccb24e?w=400",
      "https://images.unsplash.com/photo-1517868352518-2ad16a3074cd?w=400",
      "https://images.unsplash.com/photo-1605639156481-244775d6f803?w=400"
    ];

    let image = busImgs[index % busImgs.length];
    let fallbackImage = busImgs[0];

    if (typeLabel === "Railway Station") {
      image = trainImgs[index % trainImgs.length];
      fallbackImage = trainImgs[0];
    }

    /* Add map marker */
    const marker = L.marker([lat, lon]).addTo(map)
      .bindPopup(`<b>${name}</b>`);

    markers.push(marker);

    /* Create card */
    const card = document.createElement("div");

    card.className = "card";

    const rating = (Math.random() * (5.0 - 3.8) + 3.8).toFixed(1);

    card.innerHTML = `

<img src="${image}" onerror="this.onerror=null; this.src='${fallbackImage}';" class="place-img">

<h3>${name}</h3>

<p style="margin: 5px 0; color: #d0d8ff;">⭐ ${rating} | 📍 ${dist} km</p>

<button class="nav-btn">Go</button>

`;

    /* Click go -> navigate to route dashboard */
    card.querySelector('.nav-btn').onclick = (e) => {
      e.stopPropagation();
      window.location.href = `route/?lat=${lat}&lon=${lon}&name=${encodeURIComponent(name)}`;
    };

    resultsDiv.appendChild(card);

  });

}

/* Voice & Tracking Globals */
let watchId;
let voiceEnabled = false;
let lastSpoken = "";

function speakInstruction(text) {
  if (voiceEnabled && 'speechSynthesis' in window && text !== lastSpoken) {
    window.speechSynthesis.cancel();
    const msg = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(msg);
    lastSpoken = text;
  }
}

function toggleVoice() {
  voiceEnabled = !voiceEnabled;
  const icon = document.getElementById("voiceToggle");
  if (voiceEnabled) {
    icon.className = "fas fa-volume-up";
    icon.style.color = "#4cc9f0";
    const currentText = document.querySelector('.next-street-text span').innerText.replace("Next street: ", "");
    if (currentText && currentText !== "--") {
      speakInstruction(currentText);
    }
  } else {
    icon.className = "fas fa-volume-mute";
    icon.style.color = "#a0a0b5";
    window.speechSynthesis.cancel();
    lastSpoken = "";
  }
}

/* Start inline Navigation */
function startInlineNavigation(destLat, destLon, destName) {

  // Show the map panel and nav controls, hide nearby places list
  document.querySelector(".left-panel").style.display = "flex";

  const placesPanel = document.getElementById("places-panel");
  const navPanel = document.getElementById("nav-panel");

  if (placesPanel) placesPanel.style.display = "none";
  if (navPanel) navPanel.style.display = "block";

  document.getElementById("nav-dest-title").innerText = `${destName}`;
  document.getElementById("left-title").innerText = `Directions to ${destName}`;

  setTimeout(() => {
    map.invalidateSize();
  }, 100);

  if (routingControl) {
    map.removeControl(routingControl);
  }

  routingControl = L.Routing.control({
    waypoints: [
      L.latLng(userLat, userLng),
      L.latLng(destLat, destLon)
    ],
    routeWhileDragging: false,
    addWaypoints: false,
    draggableWaypoints: false,
    createMarker: () => null,
    lineOptions: {
      styles: [{ color: '#4cc9f0', weight: 6 }]
    },
    show: false
  }).addTo(map);

  const directionsPanel = document.getElementById("directions-panel");
  directionsPanel.innerHTML = "";
  directionsPanel.appendChild(routingControl._container);

  routingControl.on('routesfound', function (e) {
    const route = e.routes[0];
    const totalDistance = route.summary.totalDistance;

    const distElem = document.getElementById("distance");
    const timeElem = document.getElementById("time");
    if (distElem) distElem.innerText = (totalDistance / 1000).toFixed(2) + " km";
    if (timeElem) timeElem.innerText = (route.summary.totalTime / 60).toFixed(0) + " min";

    if (route.instructions && route.instructions.length > 0) {
      const nextText = route.instructions[0].text;
      const nextStreetElem = document.querySelector('.next-street-text span');
      if (nextStreetElem) nextStreetElem.innerText = "Next street: " + nextText;
      if (voiceEnabled) {
        speakInstruction(nextText);
      }
    }
  });

  // Track buttons
  const recenterBtn = document.getElementById("recenterBtn");
  const startBtn = document.getElementById("startBtn");

  if (recenterBtn) {
    recenterBtn.onclick = () => {
      navigator.geolocation.getCurrentPosition(p => {
        map.setView([p.coords.latitude, p.coords.longitude], 17);
      });
    };
  }

  if (startBtn) {
    startBtn.onclick = () => {
      startBtn.innerHTML = '<i class="fas fa-play"></i> Routing Active';
      startBtn.style.background = "#27ae60";

      if (!voiceEnabled) {
        toggleVoice(); // Auto-enable voice
      }

      if (watchId) navigator.geolocation.clearWatch(watchId);

      watchId = navigator.geolocation.watchPosition(function (livePos) {
        const currLat = livePos.coords.latitude;
        const currLon = livePos.coords.longitude;

        map.setView([currLat, currLon]);

        const remain = calculateDistance(currLat, currLon, destLat, destLon);
        const remainElem = document.getElementById("remain");
        if (remainElem) remainElem.innerText = remain;

        const speed = 40; // Default est speed
        const speedElem = document.getElementById("speed");
        if (speedElem) speedElem.innerText = speed;

      }, null, { enableHighAccuracy: true });
    };
  }
}

