import requests
import pandas as pd

# Your Google Maps API Key
API_KEY = "AIzaSyAgystIFC3IITxINAiJPX1ge_zcuLeMq6g"

# Function to search places using Text Search API
def search_places(query, location, radius=5000):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "location": location,
        "radius": radius,
        "key": API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("Error:", response.json())
        return []

# Function to get detailed place info (minimal fields)
def get_place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website",
        "key": API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("result", {})
    else:
        print("Error:", response.json())
        return {}

# Main Function
def main():
    search_query = "restaurants"
    location = "40.730610,-73.935242"  # Example: New York coordinates
    radius = 5000  # 5 km search radius

    # Search places
    places = search_places(search_query, location, radius)
    
    # Collect detailed information
    detailed_info = []
    for place in places:
        details = get_place_details(place.get("place_id"))
        if details:
            detailed_info.append(details)

    # Save to CSV
    df = pd.DataFrame(detailed_info)
    df.to_csv("places_data.csv", index=False)
    print("Data saved to places_data.csv")

if __name__ == "__main__":
    main()
