from django.http import JsonResponse
from django.shortcuts import render 

def chatbot_reply(request):
    message = request.GET.get("message", "").lower()
    
    # Greeting
    if any(word in message for word in ["hello", "hi", "hey"]):
        reply = "Hello! I can help you find restaurants, hotels, transport, or plan your trip."

    # If user mentions another city
    elif any(city in message for city in ["delhi", "mumbai", "bangalore", "kolkata"]):
        reply = "Currently our app provides recommendations only for Chennai."

    # Restaurants / Food
    elif any(word in message for word in ["food", "restaurant", "eat"]):
        reply = "You can explore top restaurants in Chennai in the Food section of the app."

    # Hotels / Stay
    elif any(word in message for word in ["hotel", "stay", "accommodation"]):
        reply = "You can find recommended hotels across Chennai in the Stay section."

    # Transportation
    elif any(word in message for word in ["transport", "bus", "train", "travel"]):
        reply = "Transportation options like buses, trains, and metro in Chennai are available in the Transport section."

    # Planner
    elif any(word in message for word in ["plan", "planner", "trip"]):
        reply = "You can create and manage your travel plans using the Planner feature in your account."
    
    # Places in Chennai
    elif any(word in message for word in ["place", "visit", "tourist"]):
        reply = ("You can discover popular tourist places in Chennai using the map on the dashboard of the app." 
                  "Some popular tourist places in Chennai include Marina Beach, "
                  "Kapaleeshwarar Temple, Fort St. George, Santhome Basilica, "
                  "Elliot’s Beach, and Guindy National Park.")
    
    # Beaches
    elif any(word in message for word in ["beach", "beaches"]):
        reply = "Popular beaches in Chennai include Marina Beach, Elliot’s Beach, and Kovalam Beach."

    # Temples
    elif any(word in message for word in ["temple", "temples"]):
        reply = "Famous temples in Chennai include Kapaleeshwarar Temple, Ashtalakshmi Temple, and Marundeeswarar Temple."

    # Shopping
    elif any(word in message for word in ["shopping", "mall", "market"]):
        reply = "Popular shopping places in Chennai include T. Nagar, Express Avenue Mall, and Phoenix MarketCity."

    # Parks
    elif any(word in message for word in ["park", "parks", "zoo"]):
        reply = "You can visit Guindy National Park, Arignar Anna Zoological Park (Vandalur Zoo), and Semmozhi Poonga."

    # Help
    elif "help" in message:
        reply = "I can guide you to restaurants, hotels, transport, or help you plan your trip in Chennai. Just ask!"

    # Default
    else:
        reply = "Sorry, I didn’t understand. Please ask about restaurants, hotels, transport, or travel plans in Chennai."

    return JsonResponse({"reply": reply})


def test_chatbot(request):
    return render(request, "chatbot/test_chatbot.html")

# Create your views here.
