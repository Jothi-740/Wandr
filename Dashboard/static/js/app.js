// Fallback Images logic handled dynamically in loadNearby()
// Navigation

function goLogin() {
  window.location.href = "/login/";
}

function goBack() {
  window.history.back();
}


// Login Demo

function login() {

  const user = document.getElementById("username").value;
  const pass = document.getElementById("password").value;

  if (user === "" || pass === "") {
    alert("Please fill all fields");
    return;
  }

  window.location.href = "/home/";
}


// OTP System

let generatedOTP = "";

function sendOTP() {

  const name = document.getElementById("name").value.trim();
  const mobile = document.getElementById("mobile").value.trim();
  const p1 = document.getElementById("pass1").value;
  const p2 = document.getElementById("pass2").value;

  if (name === "" || mobile === "" || p1 === "" || p2 === "") {
    alert("Please fill all fields");
    return;
  }

  if (!/^[0-9]{10}$/.test(mobile)) {
    alert("Enter valid 10 digit mobile number");
    return;
  }

  if (p1.length < 6) {
    alert("Password must be at least 6 characters");
    return;
  }

  if (p1 !== p2) {
    alert("Passwords do not match");
    return;
  }

  generatedOTP = Math.floor(1000 + Math.random() * 9000);

  alert("Your OTP is: " + generatedOTP);

  document.getElementById("otpBox").style.display = "block";

  setTimeout(() => {
    document.getElementById("otpInput").value = generatedOTP;
  }, 1500);

}

function verifyOTP() {

  const userOTP = document.getElementById("otpInput").value;

  if (userOTP === "") {
    alert("Enter OTP");
    return;
  }

  if (userOTP == generatedOTP) {

    alert("Account Created Successfully!");
    window.location.href = "/login/";

  } else {

    alert("Wrong OTP");

  }
}


// Map Display

//Dashboard Map
function initDashboardMap() {

  if (!document.getElementById("map")) return;

  navigator.geolocation.getCurrentPosition((pos) => {

    const lat = pos.coords.latitude;
    const lng = pos.coords.longitude;

    loadLiveMap(lat, lng);

  },
    () => {
      console.log("Location permission denied");
    });

}


let map;

function loadLiveMap(lat, lon) {

  if (map) {
    map.remove();
  }

  map = L.map("map").setView([lat, lon], 14);

  L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
      attribution: "© OpenStreetMap"
    }
  ).addTo(map);

  L.marker([lat, lon])
    .addTo(map)
    .bindPopup("📍 You are here")
    .openPopup();

  setTimeout(() => {
    map.invalidateSize();
  }, 500);

}


// Dashboard

function goNearby() {
  window.location.href = "/nearby/";
}

function logout() {
  document.getElementById("exitPopup").classList.add("active");
}

function logoutNow() {
  window.location.href = "/login/";
}

function closeExitPopup() {
  document.getElementById("exitPopup").classList.remove("active");
}

function openModal(id) {
  document.getElementById(id).classList.add("active");
}

function closeModal(id) {
  document.getElementById(id).classList.remove("active");
}

// Close modals when clicking outside
window.onclick = function(event) {
  if (event.target.classList.contains('modal-overlay')) {
    event.target.classList.remove('active');
  }
}

// Form Handlers
document.addEventListener("DOMContentLoaded", () => {
    const supForm = document.getElementById("supportForm");
    if(supForm) {
        supForm.addEventListener("submit", (e) => {
            e.preventDefault();
            alert("Support Request Submitted! We'll get back to you soon.");
            closeModal("supportModal");
            supForm.reset();
        });
    }

    const fbForm = document.getElementById("feedbackForm");
    if(fbForm) {
        fbForm.addEventListener("submit", (e) => {
            e.preventDefault();
            alert("Thank you for your feedback! 🚀");
            closeModal("feedbackModal");
            fbForm.reset();
        });
    }
});

let userRating = 0;
function rate(n) {
  userRating = n;
  const stars = document.querySelectorAll(".star");
  stars.forEach((s, i) => {
    if (i < n) s.classList.add("active");
    else s.classList.remove("active");
  });
}

function submitExitFeedback() {
  const msg = document.getElementById("exitFeedbackMsg").value;
  console.log("Exit Feedback:", { rating: userRating, message: msg });
  alert("Thank you for your feedback! 🚀");
  logoutNow();
}

// Exit Intent Logic
document.addEventListener("mouseleave", (e) => {
  if (e.clientY < 0) {
    document.getElementById("exitPopup").classList.add("active");
  }
});


// Route Page

function goRoute(place) {

  localStorage.setItem("place", place);
  window.location.href = "/route/";

}

//Slider 

function startSlider() {
  const slidesContainer = document.querySelector(".slides");
  const slides = document.querySelectorAll(".slide");

  if (slides.length === 0 || !slidesContainer) return;

  let index = 0;

  setInterval(() => {
    index = (index + 1) % slides.length;
    slidesContainer.style.transform = `translateX(-${index * 100}%)`;
  }, 4000);
}


// Load Route Data

window.onload = function () {

  const place = localStorage.getItem("place");

  // ROUTE PAGE

  if (place && document.getElementById("placeName")) {

    document.getElementById("placeName").innerText = place;

    document.getElementById("placeInfo").innerText =
      "You are navigating to " + place;

    loadRoute();

  }


  // DASHBOARD MAP

  if (document.getElementById("map") && !document.getElementById("placeName")) {

    navigator.geolocation.getCurrentPosition((pos) => {

      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;

      loadLiveMap(lat, lng);

    });

  }


  // START IMAGE SLIDER
  startSlider();
}

// FEEDBACK POPUP REFINDED LOGIC
document.addEventListener("DOMContentLoaded", () => {
  if (window.location.pathname.includes("/home/")) {
    const usageFlag = localStorage.getItem("visitedFeature");
    if (usageFlag === "true") {
      setTimeout(() => {
        const popup = document.getElementById("exitPopup");
        if (popup) {
          popup.classList.add("active");
          const title = popup.querySelector("h2");
          if (title) title.innerText = "Welcome Back! 🌍";
          const subtitle = popup.querySelector("p");
          if (subtitle) subtitle.innerText = "How was your experience using Wandr just now?";
          localStorage.removeItem("visitedFeature");
        }
      }, 1500); 
    }
  }
});


// NEARBY MODULE

const API_KEY = "c98680a8710e49b2ab45650010f0f45a";

function toggleSearch() {
  const input = document.getElementById("radiusInput");
  if (!input) return;

  if (input.classList.contains("active")) {
    loadNearby();
  } else {
    input.classList.add("active");
    input.focus();
  }
}

function checkEnter(event) {
  if (event.key === "Enter") {
    loadNearby();
  }
}

async function loadNearby() {

  const list = document.getElementById("nearbyList");
  const status = document.getElementById("statusMsg");

  if (!list || !status) return;

  // Track feature usage for feedback popup
  localStorage.setItem("visitedFeature", "true");

  const radiusInput = document.getElementById("radiusInput");
  let radiusMeters = 5000; // Default 5km

  if (radiusInput && radiusInput.value) {
    const km = parseFloat(radiusInput.value);
    if (!isNaN(km) && km > 0) {
      radiusMeters = km * 1000;
    }
  }

  status.innerText = "Getting your location...";
  list.innerHTML = "";

  navigator.geolocation.getCurrentPosition(

    async (position) => {

      const lat = position.coords.latitude;
      const lon = position.coords.longitude;

      status.innerText = "Searching nearby places...";

      const url =
        "https://api.geoapify.com/v2/places?" +
        "categories=tourism.attraction,leisure.park,entertainment,commercial.shopping_mall,religion.place_of_worship,heritage" +
        `&filter=circle:${lon},${lat},${radiusMeters}` +
        "&limit=50" +
        `&apiKey=${API_KEY}`;

      try {

        const res = await fetch(url);
        const data = await res.json();

        list.innerHTML = "";

        if (!data.features || data.features.length === 0) {

          status.innerText = "No nearby places found";
          return;
        }

        status.innerText = "";

        let places = data.features;

        // Shuffle the results to get a random mix up to the radius boundary
        for (let i = places.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [places[i], places[j]] = [places[j], places[i]];
        }

        // Take at most 20 random places
        places = places.slice(0, 20);

        // Sort the remaining 20 linearly by distance (closest first)
        places.sort((a, b) => {
          const distA = a.properties.distance || L.latLng(lat, lon).distanceTo(L.latLng(a.geometry.coordinates[1], a.geometry.coordinates[0]));
          const distB = b.properties.distance || L.latLng(lat, lon).distanceTo(L.latLng(b.geometry.coordinates[1], b.geometry.coordinates[0]));
          return distA - distB;
        });

        for (const place of places) {

          if (!place.properties.name) continue;

          const name = place.properties.name;

          const lat2 = place.geometry.coordinates[1];
          const lon2 = place.geometry.coordinates[0];

          let rawDist = place.properties.distance;
          if (!rawDist) {
            rawDist = L.latLng(lat, lon).distanceTo(L.latLng(lat2, lon2));
          }

          const dist = (rawDist / 1000).toFixed(2);

          let img = await getWikiImage(name);

          if (!img) {
            // Ensure every fallback is a unique call to prevent identical image caching
            img = `https://picsum.photos/400/300?random=${Math.random()}`;
          }

          const rating =
            (Math.random() * 1.5 + 3.5).toFixed(1);

          const card = `

          <div class="place-card glass">

            <img src="${img}" class="place-img"
            loading="lazy"
            onerror="this.onerror=null; this.src='https://via.placeholder.com/400x300?text=No+Image';">

            <div class="place-info">

              <h3>${name}</h3>

              <p>📍 ${dist} km</p>

              <p class="rating">⭐ ${rating} / 5</p>

              <button
                onclick="goDynamicRoute(${lat2},${lon2},'${name}')"
                class="btn-primary small">

                Go

              </button>

            </div>

          </div>
          `;

          list.innerHTML += card;

        }

      }
      catch (err) {

        console.error(err);
        status.innerText = "API Error. Check console.";

      }

    },

    () => {

      status.innerText = "Location permission denied.";

    }

  );

}


// AUTO LOAD WHEN PAGE OPENS

window.addEventListener("load", () => {

  if (document.getElementById("nearbyList")) {

    loadNearby();

  }

});


function goDynamicRoute(lat, lng, name) {

  localStorage.setItem("destLat", lat);
  localStorage.setItem("destLng", lng);
  localStorage.setItem("place", name);

  window.location.href = "/route/";

}


// Get Image From Wikipedia

async function getWikiImage(placeName) {

  try {

    const searchUrl =
      "https://en.wikipedia.org/w/api.php?" +
      "action=query" +
      "&format=json" +
      "&origin=*" +
      "&list=search" +
      "&srsearch=" + encodeURIComponent(placeName);

    const searchRes = await fetch(searchUrl);
    const searchData = await searchRes.json();

    if (!searchData.query.search.length) {
      return null;
    }

    const pageTitle =
      searchData.query.search[0].title;

    const pageUrl =
      "https://en.wikipedia.org/w/api.php?" +
      "action=query" +
      "&format=json" +
      "&origin=*" +
      "&prop=pageimages" +
      "&pithumbsize=400" +
      "&titles=" + encodeURIComponent(pageTitle);

    const pageRes = await fetch(pageUrl);
    const pageData = await pageRes.json();

    const pages = pageData.query.pages;
    const page = Object.values(pages)[0];

    if (page.thumbnail) {
      return page.thumbnail.source;
    }

    return null;

  }
  catch (err) {
    console.error("Wiki Error:", err);
    return null;
  }

}

let userIcon, destIcon;
if (typeof L !== 'undefined') {
    // User location — pulsing blue circle
    userIcon = L.divIcon({
        className: '',
        html: `<div style="
            width: 18px; height: 18px;
            background: #2ec4ff;
            border: 3px solid #fff;
            border-radius: 50%;
            box-shadow: 0 0 0 6px rgba(46,196,255,0.3), 0 0 20px rgba(46,196,255,0.5);
            animation: pulse-user 1.8s infinite;
        "></div>
        <style>
            @keyframes pulse-user {
                0%   { box-shadow: 0 0 0 6px rgba(46,196,255,0.3), 0 0 20px rgba(46,196,255,0.5); }
                50%  { box-shadow: 0 0 0 12px rgba(46,196,255,0.1), 0 0 30px rgba(46,196,255,0.3); }
                100% { box-shadow: 0 0 0 6px rgba(46,196,255,0.3), 0 0 20px rgba(46,196,255,0.5); }
            }
        </style>`,
        iconSize: [18, 18],
        iconAnchor: [9, 9]
    });

    // Destination — glowing gradient teardrop pin
    destIcon = L.divIcon({
        className: '',
        html: `<div style="
            position: relative;
            width: 40px;
            height: 50px;
            display: flex;
            flex-direction: column;
            align-items: center;
        ">
            <div style="
                width: 40px; height: 40px;
                background: linear-gradient(135deg, #2ec4ff, #5a78ff);
                border-radius: 50% 50% 50% 0;
                transform: rotate(-45deg);
                box-shadow: 0 6px 20px rgba(46,196,255,0.6);
                border: 2px solid rgba(255,255,255,0.8);
                display: flex; align-items: center; justify-content: center;
            ">
                <span style="
                    transform: rotate(45deg);
                    font-size: 18px;
                    line-height: 1;
                ">✈️</span>
            </div>
            <div style="
                width: 6px; height: 10px;
                background: linear-gradient(#5a78ff, transparent);
                border-radius: 0 0 4px 4px;
                margin-top: 0px;
            "></div>
        </div>`,
        iconSize: [40, 50],
        iconAnchor: [20, 50],
        popupAnchor: [0, -50]
    });
}

let routeMap;
let userMarker;
let routeControl; // Voice
function speak(text) {
  speechSynthesis.cancel();
  speechSynthesis.speak(new SpeechSynthesisUtterance(text));
}

// Track instruction stages
let instructionStage = new Map();

function getSpeed() {
  const mode = document.getElementById('mode').value;
  if (mode === 'walk') return 5;
  if (mode === 'bike') return 35;
  if (mode === 'car') return 45;
  return 30;
}

// Distance helper
function getDistance(lat1, lon1, lat2, lon2) {
  const R = 6371e3, φ1 = lat1 * Math.PI / 180, φ2 = lat2 * Math.PI / 180;
  const Δφ = (lat2 - lat1) * Math.PI / 180, Δλ = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(Δφ / 2) ** 2 + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function loadRoute() {

  const destLat = localStorage.getItem("destLat");
  const destLng = localStorage.getItem("destLng");
  const place = localStorage.getItem("place");

  if (document.getElementById("placeHeading")) {
    document.getElementById("placeHeading").innerText = place || "Route";
    document.getElementById("placeInfo").innerText = "Navigating to " + (place || "Destination");
  }

  // Track feature usage for feedback popup
  localStorage.setItem("visitedFeature", "true");

  if (!destLat || !destLng) return;

  navigator.geolocation.watchPosition((pos) => {

    const userLat = pos.coords.latitude;
    const userLng = pos.coords.longitude;

    if (!routeMap) {

      routeMap = L.map("map").setView([userLat, userLng], 14);

      L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        { attribution: "© OpenStreetMap" }
      ).addTo(routeMap);

      // USER MARKER
      userMarker = L.marker([userLat, userLng], {
        icon: userIcon
      }).addTo(routeMap);

      // DESTINATION MARKER
      L.marker([destLat, destLng], {
        icon: destIcon
      }).addTo(routeMap);

      routeControl = L.Routing.control({
        waypoints: [
          L.latLng(userLat, userLng),
          L.latLng(destLat, destLng)
        ],
        routeWhileDragging: false,
        show: false, // Don't show the default panel, we have our own
        createMarker: function () { return null; }
      }).addTo(routeMap);


      // We are going to put the instructions in our glass card
      setTimeout(() => {

        const instructions =
          document.querySelector(".leaflet-routing-container");

        const infoCard =
          document.querySelector(".route-info");

        if (instructions && infoCard) {
          // Re-inserting instructions before the nav-buttons
          const navBtns = document.querySelector(".nav-buttons");
          infoCard.insertBefore(instructions, navBtns);
        }

      }, 500);

      // DISTANCE + TIME
      routeControl.on("routesfound", function (e) {

        const route = e.routes[0];
        totalDistance = route.summary.totalDistance;

        const distance = (totalDistance / 1000).toFixed(2);
        const timeValue = (route.summary.totalTime / 60).toFixed(0);

        document.getElementById("distance").innerText = "Distance: " + distance + " km";
        document.getElementById("eta").innerText = "Estimated Time: " + timeValue + " mins";

        if (isJourneyStarted && route.instructions && route.instructions.length > 0) {
          const firstInstr = route.instructions[0];
          if (!instructionStage.has(firstInstr.text)) {
            instructionStage.set(firstInstr.text, 'advance');
            document.getElementById("nextStreet").innerText = "Next street: " + firstInstr.text;
            speak("Navigation started. First turn on " + firstInstr.text);
          }
        }
      });

    }
    else {

      userMarker.setLatLng([userLat, userLng]);

      routeControl.setWaypoints([
        L.latLng(userLat, userLng),
        L.latLng(destLat, destLng)
      ]);

      if (isJourneyStarted) {
        routeMap.setView([userLat, userLng], 18);
      }

      // Stats Update
      const remain = getDistance(userLat, userLng, destLat, destLng) / 1000;
      const remainElem = document.getElementById("remain");
      if (remainElem) remainElem.innerText = remain.toFixed(2);

      const speed = getSpeed();
      const speedElem = document.getElementById("speed");
      if (speedElem) speedElem.innerText = speed;

      const dashEtaElem = document.getElementById("dashEta");
      if (dashEtaElem) dashEtaElem.innerText = Math.round((remain / speed) * 60);

      const progress = ((totalDistance - remain * 1000) / totalDistance) * 100;
      const progressBar = document.getElementById("progressBar");
      if (progressBar && progress > 0) progressBar.style.width = progress + "%";

      // Arrival logic
      if (remain < 0.05 && isJourneyStarted && instructionStage.get("arrived") !== "done") {
        speak("You have arrived at your destination");
        instructionStage.set("arrived", "done");
        
        // Enable End Journey button
        const btn = document.getElementById("journeyBtn");
        if (btn) {
          btn.innerHTML = "🏁 End Journey";
          btn.style.background = "#22c55e"; // Success green
          btn.style.boxShadow = "0 0 10px #22c55e";
          btn.disabled = false;
          btn.onclick = endJourney;
        }
      }

      // Turn arrow (Very basic simulation)
      const turnArrow = document.getElementById("turnArrow");
      if (turnArrow) turnArrow.innerText = remain > 1 ? "⬆️" : remain > 0.5 ? "➡️" : "⬅️";

      // Live Instructions processing
      if (routeControl && routeControl._routes && routeControl._routes[0] && isJourneyStarted) {
        const instructions = routeControl._routes[0].instructions;
        if (instructions && instructions.length > 0) {
          for (let instr of instructions) {
            const dist = getDistance(userLat, userLng, instr.latLng.lat, instr.latLng.lng);
            const stage = instructionStage.get(instr.text) || "none";

            // Advance alert ~150m
            if (stage === "none" && dist < 150) {
              speak("Upcoming turn on " + instr.text + " in 150 meters");
              instructionStage.set(instr.text, "advance");
              document.getElementById("nextStreet").innerText = "Next street: " + instr.text;
            }
            // Turn now ~50m
            else if (stage === "advance" && dist < 50) {
              speak("Turn now on " + instr.text);
              instructionStage.set(instr.text, "done");
              document.getElementById("nextStreet").innerText = "Next street: " + instr.text;
            }
          }
        }
      }
    }
  });
}

let isJourneyStarted = false;
let totalDistance = 0;

function toggleJourney() {
  if (!isJourneyStarted) {
    isJourneyStarted = true;
    const btn = document.getElementById("journeyBtn");
    if (btn) {
      btn.innerHTML = "On Route...";
      btn.style.background = "#ffa500"; // Orange to indicate in progress
      btn.style.boxShadow = "0 0 10px #ffa500";
      // Disable the button until they reach the destination
      btn.disabled = true;
    }
    
    // Announce start
    speak("Journey started. Happy travels!");

    if (routeMap && userMarker) {
      routeMap.setView(userMarker.getLatLng(), 18);
    }
  }
}

function recenter() {
  if (routeMap && userMarker) {
    routeMap.setView(userMarker.getLatLng(), isJourneyStarted ? 18 : 15);
  }
}

function endJourney() {

  confetti({
    particleCount: 150,
    spread: 70,
    origin: { y: 0.6 }
  });

  const popup = document.createElement("div");
  popup.style.position = "fixed";
  popup.style.top = "50%";
  popup.style.left = "50%";
  popup.style.transform = "translate(-50%, -50%)";
  popup.style.background = "#1F2937";
  popup.style.color = "white";
  popup.style.padding = "20px 40px";
  popup.style.borderRadius = "15px";
  popup.style.fontSize = "24px";
  popup.style.zIndex = "10001";
  popup.style.boxShadow = "0 0 30px rgba(0,0,0,0.5)";
  popup.innerHTML = "🎉 Journey Completed! 🎉<br><small style='font-size:14px; opacity:0.8;'>Returning to nearby places...</small>";

  document.body.appendChild(popup);


  setTimeout(() => {
    window.location.href = "/nearby/";
  }, 3000);

}
// ---------------------------
// FOOTER NAVIGATION
// ---------------------------

function openSupport() {
  openModal("supportModal");
}

function openFeedback() {
  openModal("feedbackModal");
}

// ---------------------------
// FLASHCARDS SLIDER
// ---------------------------

let currentFlashcardIndex = 0;

function showFlashcard(index) {
  const flashcards = document.querySelectorAll(".flashcard");
  if (flashcards.length === 0) return;
  
  // Wrap around logic
  if (index >= flashcards.length) {
    currentFlashcardIndex = 0;
  } else if (index < 0) {
    currentFlashcardIndex = flashcards.length - 1;
  } else {
    currentFlashcardIndex = index;
  }
  
  // Hide all flashcards and show the active one
  flashcards.forEach((card, i) => {
    if (i === currentFlashcardIndex) {
      card.classList.add("active");
    } else {
      card.classList.remove("active");
    }
  });
}

function nextFlashcard() {
  showFlashcard(currentFlashcardIndex + 1);
}

function prevFlashcard() {
  showFlashcard(currentFlashcardIndex - 1);
}