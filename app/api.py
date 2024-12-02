import httpx
from typing import List, Dict, Any
import asyncio

async def search_places(query: str, api_key: str, max_results: int = 20) -> List[Dict[str, Any]]:
    # Split the request into multiple calls if max_results > 20
    all_results = []
    remaining = max_results
    page_token = None
    
    while remaining > 0:
        url = "https://places.googleapis.com/v1/places:searchText"
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': api_key,
            'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount'
        }
        
        data = {
            'textQuery': query,
            'maxResultCount': min(remaining, 20)  # Google's API limit is 20 per request
        }
        if page_token:
            data['pageToken'] = page_token
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            places = result.get('places', [])
            all_results.extend(places)
            
            # Check if there are more results
            page_token = result.get('nextPageToken')
            remaining -= len(places)
            
            if not page_token or not places:
                break
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.5)
    
    return all_results

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
        display_name = result.get('displayName', {}).get('text', '')
        business_type = result.get('primaryTypeDisplayName', '')
        
        # Format opening hours with proper encoding
        opening_hours = []
        if 'regularOpeningHours' in result:
            hours = result.get('regularOpeningHours', {}).get('weekdayDescriptions', [])
            # Clean up the time format
            opening_hours = [h.replace('\u2009', ' ').replace('\u2013', '-') for h in hours]
        formatted_hours = ' | '.join(opening_hours) if opening_hours else ''
        
        return {
            'Business Name': display_name,
            'Type': business_type,
            'Address': result.get('formattedAddress', ''),
            'Phone': result.get('nationalPhoneNumber', '') or result.get('internationalPhoneNumber', ''),
            'Website': result.get('websiteUri', ''),
            'Opening Hours': formatted_hours,
            'Maps URL': result.get('googleMapsUri', ''),
            'Rating': str(result.get('rating', '')),
            'Reviews Count': str(result.get('userRatingCount', ''))
        } 