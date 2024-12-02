import os
import pandas as pd
import streamlit as st
from datetime import datetime
import requests
from time import sleep
from dotenv import load_dotenv

# Directory for results
OUTPUT_DIR = "scraper_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_api_key():
    load_dotenv()
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key and 'GOOGLE_MAPS_API_KEY' in st.secrets:
        api_key = st.secrets['GOOGLE_MAPS_API_KEY']
    return api_key

def search_places(query, api_key):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount'
    }
    
    data = {
        'textQuery': query,
        'maxResultCount': 20  # Adjust as needed
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get('places', [])
    except Exception as e:
        st.error(f"Error searching places: {str(e)}")
        return []

def get_place_details(place_id, api_key):
    base_url = f"https://places.googleapis.com/v1/places/{place_id}"
    fields = [
        "id",
        "displayName",
        "formattedAddress",
        "nationalPhoneNumber",
        "internationalPhoneNumber",
        "websiteUri",
        "regularOpeningHours",
        "rating",
        "userRatingCount",
        "googleMapsUri",
        "primaryTypeDisplayName"
    ]
    
    headers = {
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': ','.join(fields)
    }
    
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        # Format opening hours into a single line
        opening_hours = []
        if 'regularOpeningHours' in result:
            opening_hours = result.get('regularOpeningHours', {}).get('weekdayDescriptions', [])
        formatted_hours = ' | '.join(opening_hours) if opening_hours else ''
        
        # Clean and format the data
        return {
            'Business Name': result.get('displayName', {}).get('text', '').strip(),
            'Type': result.get('primaryTypeDisplayName', '').strip(),
            'Address': result.get('formattedAddress', '').strip(),
            'Phone': (result.get('nationalPhoneNumber', '') or result.get('internationalPhoneNumber', '')).strip(),
            'Website': result.get('websiteUri', '').strip(),
            'Opening Hours': formatted_hours.strip(),
            'Maps URL': result.get('googleMapsUri', '').strip(),
            'Rating': str(result.get('rating', '')).strip(),
            'Reviews Count': str(result.get('userRatingCount', '')).strip()
        }
    except Exception as e:
        st.error(f"Error fetching details: {str(e)}")
        return None

def paginate(items, page_size=10, page_num=1):
    """Return a slice of items for the given page number."""
    start = (page_num - 1) * page_size
    end = start + page_size
    total_pages = (len(items) + page_size - 1) // page_size
    return items[start:end], total_pages

def main():
    st.set_page_config(page_title="Places Data Gatherer", layout="wide")
    
    # Custom CSS for layout
    st.markdown("""
        <style>
        /* Reset Streamlit defaults */
        .main {
            padding: 0 !important;
        }
        .block-container {
            padding: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Card styling */
        .card {
            background-color: #1E1E1E;
            border-radius: 0.5rem;
            padding: 1.5rem;
            border: 1px solid #333;
            margin-bottom: 1rem;
            height: fit-content;
        }
        
        /* Search parameters card */
        .search-card {
            margin-bottom: 2rem;
        }
        
        /* Results container */
        .results-container {
            height: calc(100vh - 300px);
            overflow-y: auto;
            padding-right: 1rem;
            /* Scrollbar styling */
            scrollbar-width: thin;
            scrollbar-color: #4CAF50 #1E1E1E;
        }
        .results-container::-webkit-scrollbar {
            width: 8px;
        }
        .results-container::-webkit-scrollbar-track {
            background: #1E1E1E;
            border-radius: 4px;
        }
        .results-container::-webkit-scrollbar-thumb {
            background-color: #4CAF50;
            border-radius: 4px;
        }
        
        /* Result card styling */
        .result-item {
            background-color: #2E2E2E;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
            border: 1px solid #363636;
        }
        .result-item:hover {
            border-color: #4CAF50;
        }
        .result-content h4 {
            margin: 0;
            color: #fff;
        }
        .result-content p {
            margin: 0.25rem 0;
            color: #ccc;
        }
        .result-meta {
            font-size: 0.8rem;
            color: #aaa;
        }
        
        /* Export card */
        .export-card {
            height: calc(100vh - 300px);
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'selected_places' not in st.session_state:
        st.session_state.selected_places = []

    # Search Parameters Card
    st.markdown('<div class="card search-card">', unsafe_allow_html=True)
    st.markdown("### Search Parameters")
    
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "Search Query",
            placeholder="e.g., 'restaurants in Ljubljana' or 'hotels near city center'"
        )
    
    with col2:
        max_results = st.number_input("Max Results", 1, 100, 20)
    
    with col3:
        min_rating = st.slider("Min Rating", 0.0, 5.0, 0.0, 0.5)
    
    with col4:
        if st.button("🔍 Search", type="primary", use_container_width=True):
            if search_query:
                with st.spinner("Searching..."):
                    results = search_places(search_query, api_key)
                    if min_rating > 0:
                        results = [r for r in results if float(r.get('rating', 0) or 0) >= min_rating]
                    results = results[:max_results]
                    st.session_state.search_results = results
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Results and Export Area
    if st.session_state.search_results:
        col1, col2 = st.columns([2, 1])
        
        # Results Column
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"### Search Results ({len(st.session_state.search_results)} found)")
            
            # Select all checkbox
            all_selected = st.checkbox(
                "Select All",
                value=len(st.session_state.selected_places) == len(st.session_state.search_results)
            )
            
            if all_selected:
                st.session_state.selected_places = list(range(len(st.session_state.search_results)))
            elif not all_selected and len(st.session_state.selected_places) == len(st.session_state.search_results):
                st.session_state.selected_places = []
            
            # Scrollable results
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            for idx, place in enumerate(st.session_state.search_results):
                cols = st.columns([0.1, 0.9])
                with cols[0]:
                    selected = st.checkbox("", key=f"select_{idx}", value=idx in st.session_state.selected_places)
                    if selected and idx not in st.session_state.selected_places:
                        st.session_state.selected_places.append(idx)
                    elif not selected and idx in st.session_state.selected_places:
                        st.session_state.selected_places.remove(idx)
                
                with cols[1]:
                    display_name = place.get('displayName', {}).get('text', 'Unknown')
                    address = place.get('formattedAddress', 'No address')
                    rating = place.get('rating', 'N/A')
                    reviews = place.get('userRatingCount', 0)
                    
                    st.markdown(f"""
                    <div class="result-item">
                        <div class="result-content">
                            <h4>{idx + 1}. {display_name}</h4>
                            <p>{address}</p>
                            <div class="result-meta">
                                Rating: {rating}⭐ ({reviews} reviews)
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Export Column
        with col2:
            st.markdown('<div class="card export-card">', unsafe_allow_html=True)
            st.markdown("### Export Options")
            
            export_format = st.selectbox(
                "Export Format",
                ["CSV", "Excel"],
                help="Choose the format for your exported data"
            )
            
            if st.session_state.selected_places:
                st.info(f"Selected {len(st.session_state.selected_places)} places")
                
                if st.button("📥 Export Selected", type="primary", use_container_width=True):
                    with st.spinner("Gathering detailed data..."):
                        detailed_data = []
                        progress = st.progress(0)
                        
                        for i, idx in enumerate(st.session_state.selected_places):
                            place = st.session_state.search_results[idx]
                            details = get_place_details(place['id'], api_key)
                            if details:
                                detailed_data.append(details)
                            progress.progress((i + 1) / len(st.session_state.selected_places))
                            sleep(0.1)
                        
                        if detailed_data:
                            df = pd.DataFrame(detailed_data)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"places_data_{timestamp}"
                            
                            if export_format == "CSV":
                                filepath = os.path.join(OUTPUT_DIR, f"{filename}.csv")
                                df.to_csv(filepath, index=False, encoding='utf-8')
                                ext = "csv"
                                mime = "text/csv"
                            else:
                                filepath = os.path.join(OUTPUT_DIR, f"{filename}.xlsx")
                                df.to_excel(filepath, index=False)
                                ext = "xlsx"
                                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            
                            with open(filepath, "rb") as f:
                                st.download_button(
                                    label=f"⬇️ Download {export_format}",
                                    data=f,
                                    file_name=f"{filename}.{ext}",
                                    mime=mime
                                )
                            
                            st.success("✅ Export complete!")
                            
                            with st.expander("Preview Data"):
                                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Select places to export")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    api_key = get_api_key()
    if not api_key:
        st.error("Please set up your Google Maps API key in .streamlit/secrets.toml")
    else:
        main()
