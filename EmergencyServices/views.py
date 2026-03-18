from django.shortcuts import render
import requests
from django.http import JsonResponse

def emergency_dashboard(request):
    return render(request, "EmergencyServices/emergency.html")

#Hospital API
def nearby_hospitals(request):
    try:
        try:
            lat = float(request.GET.get("lat", 0))
            lon = float(request.GET.get("lon", 0))
        except (ValueError, TypeError):
            return JsonResponse([], safe=False)

        if not lat or not lon:
            return JsonResponse([], safe=False)

        servers = [
            "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter",
            "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
            "https://overpass.osm.ch/api/interpreter"
        ]
        
        headers = {
            'User-Agent': 'WandrEmergencyApp/1.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        query = f"""
        [out:json];
        (
          node["amenity"~"hospital|clinic|nursing_home"]["name"](around:20000,{lat},{lon});
          way["amenity"~"hospital|clinic|nursing_home"]["name"](around:20000,{lat},{lon});
        );
        out center;
        """

        data = None
        for url in servers:
            try:
                print(f"Requesting hospitals from {url}...")
                response = requests.post(url, data={"data": query}, headers=headers, timeout=12)
                if response.status_code == 200:
                    data = response.json()
                    break
            except Exception as e:
                print(f"Overpass error at {url}: {e}")
                continue

        if not data or "elements" not in data:
            return JsonResponse([], safe=False)
            
        hospitals = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            center = element.get("center") or {}
            h_lat = element.get("lat") or center.get("lat")
            h_lon = element.get("lon") or center.get("lon")
            name = tags.get("name")
            
            if h_lat and h_lon and name:
                hospitals.append({
                    "name": name,
                    "lat": float(h_lat),
                    "lon": float(h_lon),
                    "type": tags.get("amenity", "hospital").replace('_', ' ').capitalize(),
                    "dist": (float(h_lat) - lat)**2 + (float(h_lon) - lon)**2
                })

        hospitals.sort(key=lambda x: x["dist"])
        return JsonResponse(hospitals[:3], safe=False)
    except Exception as e:
        print(f"Internal error in nearby_hospitals: {e}")
        return JsonResponse([], safe=False)

def nearby_police(request):
    try:
        try:
            lat = float(request.GET.get("lat", 0))
            lon = float(request.GET.get("lon", 0))
        except (ValueError, TypeError):
            return JsonResponse([], safe=False)

        if not lat or not lon:
            return JsonResponse([], safe=False)

        servers = [
            "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter",
            "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
            "https://overpass.osm.ch/api/interpreter"
        ]
        
        headers = {
            'User-Agent': 'WandrEmergencyApp/1.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        query = f"""
        [out:json];
        (
          node["amenity"~"police"]["name"](around:50000,{lat},{lon});
          way["amenity"~"police"]["name"](around:50000,{lat},{lon});
        );
        out center;
        """

        data = None
        for url in servers:
            try:
                print(f"Requesting police from {url}...")
                response = requests.post(url, data={"data": query}, headers=headers, timeout=12)
                if response.status_code == 200:
                    data = response.json()
                    break
            except Exception as e:
                print(f"Overpass error at {url}: {e}")
                continue

        if not data or "elements" not in data:
            return JsonResponse([], safe=False)

        stations = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            center = element.get("center") or {}
            h_lat = element.get("lat") or center.get("lat")
            h_lon = element.get("lon") or center.get("lon")
            name = tags.get("name")
            
            if h_lat and h_lon and name:
                stations.append({
                    "name": name,
                    "lat": float(h_lat),
                    "lon": float(h_lon),
                    "type": "Police Station",
                    "dist": (float(h_lat) - lat)**2 + (float(h_lon) - lon)**2
                })

        stations.sort(key=lambda x: x["dist"])
        return JsonResponse(stations[:3], safe=False)
    except Exception as e:
        print(f"Internal error in nearby_police: {e}")
        return JsonResponse([], safe=False)

def nearby_fire(request):
    try:
        try:
            lat = float(request.GET.get("lat", 0))
            lon = float(request.GET.get("lon", 0))
        except (ValueError, TypeError):
            return JsonResponse([], safe=False)

        if not lat or not lon:
            return JsonResponse([], safe=False)

        servers = [
            "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter",
            "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
            "https://overpass.osm.ch/api/interpreter"
        ]
        
        headers = {
            'User-Agent': 'WandrEmergencyApp/1.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        query = f"""
        [out:json];
        (
          node["amenity"~"fire_station"]["name"](around:50000,{lat},{lon});
          way["amenity"~"fire_station"]["name"](around:50000,{lat},{lon});
        );
        out center;
        """

        data = None
        for url in servers:
            try:
                print(f"Requesting fire stations from {url}...")
                response = requests.post(url, data={"data": query}, headers=headers, timeout=12)
                if response.status_code == 200:
                    data = response.json()
                    break
            except Exception as e:
                print(f"Overpass error at {url}: {e}")
                continue

        if not data or "elements" not in data:
            return JsonResponse([], safe=False)

        stations = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            center = element.get("center") or {}
            h_lat = element.get("lat") or center.get("lat")
            h_lon = element.get("lon") or center.get("lon")
            name = tags.get("name")
            
            if h_lat and h_lon and name:
                stations.append({
                    "name": name,
                    "lat": float(h_lat),
                    "lon": float(h_lon),
                    "type": "Fire Station",
                    "dist": (float(h_lat) - lat)**2 + (float(h_lon) - lon)**2
                })

        stations.sort(key=lambda x: x["dist"])
        return JsonResponse(stations[:3], safe=False)
    except Exception as e:
        print(f"Internal error in nearby_fire: {e}")
        return JsonResponse([], safe=False)

def nearby_mechanic(request):
    try:
        try:
            lat = float(request.GET.get("lat", 0))
            lon = float(request.GET.get("lon", 0))
        except (ValueError, TypeError):
            return JsonResponse([], safe=False)

        if not lat or not lon:
            return JsonResponse([], safe=False)

        servers = [
            "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter",
            "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
            "https://overpass.osm.ch/api/interpreter"
        ]
        
        headers = {
            'User-Agent': 'WandrEmergencyApp/1.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        query = f"""
        [out:json];
        (
          node["shop"~"car_repair"]["name"](around:50000,{lat},{lon});
          way["shop"~"car_repair"]["name"](around:50000,{lat},{lon});
          node["amenity"~"car_repair"]["name"](around:50000,{lat},{lon});
          way["amenity"~"car_repair"]["name"](around:50000,{lat},{lon});
        );
        out center;
        """

        data = None
        for url in servers:
            try:
                print(f"Requesting mechanics from {url}...")
                response = requests.post(url, data={"data": query}, headers=headers, timeout=12)
                if response.status_code == 200:
                    data = response.json()
                    break
            except Exception as e:
                print(f"Overpass error at {url}: {e}")
                continue

        if not data or "elements" not in data:
            return JsonResponse([], safe=False)

        mechanics = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            center = element.get("center") or {}
            h_lat = element.get("lat") or center.get("lat")
            h_lon = element.get("lon") or center.get("lon")
            name = tags.get("name")
            
            if h_lat and h_lon and name:
                mechanics.append({
                    "name": name,
                    "lat": float(h_lat),
                    "lon": float(h_lon),
                    "type": "Mechanic",
                    "dist": (float(h_lat) - lat)**2 + (float(h_lon) - lon)**2
                })

        mechanics.sort(key=lambda x: x["dist"])
        return JsonResponse(mechanics[:5], safe=False)
    except Exception as e:
        print(f"Internal error in nearby_mechanic: {e}")
        return JsonResponse([], safe=False)


def hospital_route(request):
    name = request.GET.get('name', 'Medical Center')
    lat = request.GET.get('lat', '0')
    lon = request.GET.get('lon', '0')
    
    context = {
        'name': name,
        'lat': lat,
        'lon': lon,
        'type': request.GET.get('type', 'Medical'),
        'title': f'Route to {name}'
    }
    return render(request, "EmergencyServices/hospital_route.html", context)