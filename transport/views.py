import requests
from django.shortcuts import render

def nearby_transport(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    transport_results = []

    if lat and lng:
        overpass_url = "http://overpass-api.de/api/interpreter"
        transport_query = f"""
        [out:json];
        (
          node["highway"="bus_stop"](around:1500,{lat},{lng});
          node["railway"="station"](around:1500,{lat},{lng});
        );
        out body 10;
        """
        transport_response = requests.get(overpass_url, params={'data': transport_query})

        if transport_response.status_code == 200:
            transport_results = transport_response.json().get('elements', [])

    context = {
        'transport_results': transport_results,
        'lat': lat,
        'lng': lng
    }

    return render(request, 'transport/nearby.html', context)


def route_page(request):
    lat = request.GET.get("lat", "13.0827")
    lon = request.GET.get("lon", "80.2707")
    name = request.GET.get("name", "Destination")

    context = {
        "lat": lat,
        "lon": lon,
        "name": name
    }

    return render(request, "transport/route.html", context)
