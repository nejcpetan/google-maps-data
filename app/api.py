import httpx
from typing import List, Dict, Any, Tuple
import asyncio
import json
from math import cos, radians
from datetime import datetime

async def search_places(query: str, api_key: str, max_results: int = 20) -> List[Dict[str, Any]]:
    all_results = []
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,nextPageToken'
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        page_token = None
        page_count = 0
        
        while len(all_results) < max_results:
            try:
                # Prepare request data
                request_data = {
                    'textQuery': query,
                    'pageSize': min(20, max_results - len(all_results))  # Request up to 20 at a time
                }
                if page_token:
                    request_data['pageToken'] = page_token
                
                # Make request
                response = await client.post(url, headers=headers, json=request_data)
                response.raise_for_status()
                result = response.json()
                
                # Get places from response
                places = result.get('places', [])
                if not places:
                    print(f"No more places found after {len(all_results)} results")
                    break
                
                # Add places to results
                all_results.extend(places)
                page_count += 1
                print(f"Page {page_count}: Found {len(places)} places. Total so far: {len(all_results)}")
                
                # Check if we have a next page
                page_token = result.get('nextPageToken')
                if not page_token:
                    print("No next page token received")
                    break
                
                # Small delay before next request (required by Google)
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"Error on page {page_count + 1}: {str(e)}")
                break
    
    print(f"Final result count: {len(all_results)}")
    return all_results[:max_results]

async def search_nearby(client, location, query: str, api_key: str, remaining: int) -> List[Dict[str, Any]]:
    """Helper function to perform nearby search"""
    nearby_results = []
    
    # Different radius and ranking combinations
    variations = [
        {'radius': 25000, 'rank': 'RATING'},
        {'radius': 25000, 'rank': 'DISTANCE'},
        {'radius': 15000, 'rank': 'RATING'},
    ]
    
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.location'
    }
    
    for variation in variations:
        if len(nearby_results) >= remaining:
            break
            
        try:
            nearby_data = {
                'locationRestriction': {
                    'circle': {
                        'center': location,
                        'radius': float(variation['radius'])
                    }
                },
                'maxResultCount': remaining,
                'rankPreference': variation['rank']
            }
            
            # Add original query as keyword
            if not any(word.lower() in ['in', 'at', 'near'] for word in query.split()):
                nearby_data['textQuery'] = query.split()[0]
            
            response = await client.post(
                "https://places.googleapis.com/v1/places:searchNearby",
                headers=headers,
                json=nearby_data
            )
            
            if response.status_code == 200:
                results = response.json().get('places', [])
                nearby_results.extend(results)
                print(f"Nearby search ({variation['radius']}m, {variation['rank']}): Found {len(results)} places")
            
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"Nearby search error: {str(e)}")
            continue
    
    return nearby_results

def generate_grid_points(center_lat: float, center_lng: float, radius_km: float, grid_size: int) -> List[Tuple[float, float]]:
    """Generate a grid of points around a center location."""
    points = []
    # Calculate lat/lng deltas (approximate)
    lat_delta = radius_km / 111.0  # 1 degree lat = ~111km
    lng_delta = radius_km / (111.0 * cos(radians(center_lat)))  # Adjust for latitude
    
    # Generate grid
    for i in range(-grid_size//2, grid_size//2 + 1):
        for j in range(-grid_size//2, grid_size//2 + 1):
            lat = center_lat + (i * lat_delta)
            lng = center_lng + (j * lng_delta)
            points.append((lat, lng))
    
    return points

async def get_place_details(place_id: str, api_key: str) -> Dict[str, Any]:
    url = f"https://places.googleapis.com/v1/places/{place_id}"
    fields = [
        "id", "displayName", "formattedAddress", "nationalPhoneNumber",
        "internationalPhoneNumber", "websiteUri", "regularOpeningHours",
        "rating", "userRatingCount", "googleMapsUri", "primaryTypeDisplayName"
    ]
    
    headers = {
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': ','.join(fields)
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        # Clean and format the data
        company = result.get('displayName', {}).get('text', '')
        
        # Clean up the type field
        business_type = result.get('primaryTypeDisplayName', '')
        if isinstance(business_type, dict):
            business_type = business_type.get('text', '')
            
        # Format phone number (remove spaces and special characters)
        phone = result.get('nationalPhoneNumber', '') or result.get('internationalPhoneNumber', '')
        phone = phone.replace(' ', '').replace('(', '').replace(')', '').replace('+', '')
            
        # Format address
        address = result.get('formattedAddress', '')
        
        # Format opening hours
        opening_hours = []
        if 'regularOpeningHours' in result:
            hours = result.get('regularOpeningHours', {}).get('weekdayDescriptions', [])
            opening_hours = [h.replace('\u2009', ' ').replace('\u2013', '-') for h in hours]
        business_hours = ' | '.join(opening_hours) if opening_hours else ''
        
        # Get rating without /5
        rating = str(result.get('rating', ''))
            
        return {
            'Company record ID': place_id,  # Using Google Place ID as unique identifier
            'Company': company,
            'Phone Number': phone,
            'Website URL': result.get('websiteUri', ''),
            'Street Address': address,
            'Business Type': business_type,
            'Business Hours': business_hours,
            'Google Maps URL': result.get('googleMapsUri', ''),
            'Rating': rating,
            'Number of Reviews': result.get('userRatingCount', ''),
            'Last Updated': datetime.now().strftime('%Y-%m-%d')
        } 