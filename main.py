import os
import pandas as pd
import streamlit as st
from datetime import datetime
import requests
from time import sleep

# Directory to store CSV files
OUTPUT_DIR = "scraper_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_api_key():
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key and 'GOOGLE_MAPS_API_KEY' in st.secrets:
        api_key = st.secrets['GOOGLE_MAPS_API_KEY']
    return api_key

def get_place_details(place_id, api_key):
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'key': api_key,
        'fields': 'name,formatted_address,formatted_phone_number,website,opening_hours,url,email'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        result = response.json().get('result', {})
        
        # Format opening hours if available
        opening_hours = result.get('opening_hours', {}).get('weekday_text', [])
        formatted_hours = '\n'.join(opening_hours) if opening_hours else ''
        
        return {
            'Company Name': result.get('name', ''),
            'Address': result.get('formatted_address', ''),
            'Phone Number': result.get('formatted_phone_number', ''),
            'Website': result.get('website', ''),
            'Email': result.get('email', ''),
            'Opening Hours': formatted_hours,
            'Google Maps URL': result.get('url', '')
        }
    except requests.exceptions.RequestException as e:
        st.warning(f"Error fetching details for a place: {str(e)}")
        return None

def scrape_places(search_term, location, api_key):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    # Combine search term and location for the query
    query = f"{search_term} in {location}"
    
    params = {
        'query': query,
        'key': api_key
    }
    
    all_places = []
    
    try:
        # Make the initial request
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        results = response.json()
        
        # Process results
        for place in results.get('results', []):
            place_id = place.get('place_id')
            if place_id:
                place_details = get_place_details(place_id, api_key)
                if place_details:
                    # Add rating and total ratings from the initial search
                    place_details['Rating'] = place.get('rating', '')
                    place_details['User Ratings Total'] = place.get('user_ratings_total', '')
                    all_places.append(place_details)
            sleep(0.1)  # Small delay to avoid hitting rate limits
            
        # Handle pagination if there are more results
        next_page_token = results.get('next_page_token')
        while next_page_token and len(all_places) < 60:  # Limit to 3 pages (60 results)
            sleep(2)  # Required delay between requests when using page tokens
            params['pagetoken'] = next_page_token
            response = requests.get(base_url, params=params)
            results = response.json()
            
            for place in results.get('results', []):
                place_id = place.get('place_id')
                if place_id:
                    place_details = get_place_details(place_id, api_key)
                    if place_details:
                        place_details['Rating'] = place.get('rating', '')
                        place_details['User Ratings Total'] = place.get('user_ratings_total', '')
                        all_places.append(place_details)
                sleep(0.1)
                
            next_page_token = results.get('next_page_token')
            
        # Create DataFrame and save to CSV
        df = pd.DataFrame(all_places)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{search_term}_{location}_{timestamp}.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Save with UTF-8 encoding and proper handling of special characters
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        return filename, len(all_places)
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching data: {str(e)}")

# Streamlit UI
st.title("Google Maps Scraper")

# Input form for search
st.header("Input Search Parameters")
search_term = st.text_input("Search Term (e.g., Plumbers)")
location = st.text_input("Location (e.g., Ljubljana)")

# Get API key
api_key = get_api_key()

if st.button("Run Scraper"):
    if not api_key:
        st.error("Please set up your Google Maps API key in environment variables or Streamlit secrets.")
    elif search_term and location:
        try:
            with st.spinner('Scraping data from Google Maps...'):
                filename, count = scrape_places(search_term, location, api_key)
                st.success(f"Scraping completed! Found {count} results. File saved as {filename}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please provide both search term and location.")

# File browser
st.header("Download Saved Files")
files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".csv")]
if files:
    selected_file = st.selectbox("Select a file to download:", files)
    if selected_file:
        file_path = os.path.join(OUTPUT_DIR, selected_file)
        with open(file_path, "rb") as f:
            st.download_button(
                label="Download CSV",
                data=f,
                file_name=selected_file,
                mime="text/csv"
            )
else:
    st.info("No files available for download.")
