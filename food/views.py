import requests
from django.shortcuts import render

def nearby_food(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    food_results = []

    if lat and lng:
        overpass_url = "http://overpass-api.de/api/interpreter"
        food_query = f"""
        [out:json];
        (
          node["amenity"="restaurant"](around:1500,{lat},{lng});
          node["tourism"="hotel"](around:1500,{lat},{lng});
        );
        out body 10;
        """
        food_response = requests.get(overpass_url, params={'data': food_query})

        if food_response.status_code == 200:
            food_results = food_response.json().get('elements', [])

    context = {
        'food_results': food_results,
        'lat': lat,
        'lng': lng
    }

    return render(request, 'food/nearby.html', context)


def route_page(request):
    lat = request.GET.get("lat", "13.0827")
    lon = request.GET.get("lon", "80.2707")
    name = request.GET.get("name", "Destination")

    context = {
        "lat": lat,
        "lon": lon,
        "name": name
    }

    return render(request, "food/route.html", context)
