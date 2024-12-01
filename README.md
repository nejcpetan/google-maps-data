# Google Maps Business Scraper

A Streamlit-based web application that allows users to scrape business information from Google Maps using the Google Places API. The application provides an easy-to-use interface for searching businesses by location and extracting relevant information into CSV files.

## Features

- Search businesses by keyword and location
- Extracts detailed business information including:
  - Company Name
  - Address
  - Phone Number
  - Website
  - Email (if available)
  - Opening Hours
  - Ratings and Reviews Count
  - Google Maps URL
- UTF-8 encoding support for international characters
- CSV export functionality
- Built-in file browser for downloading previous searches

## Tech Stack

- **Python 3.8+**
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and CSV handling
- **Requests**: HTTP requests to Google Places API
- **python-dotenv**: Environment variable management

## Prerequisites

- Python 3.8 or higher
- Google Maps API key with Places API enabled
- Internet connection

## Installation

### Windows Users

1. Clone this repository or download the files
2. Double-click `setup.bat`
3. Wait for the setup to complete
4. Add your Google Maps API key (see Configuration section)
5. Double-click `run.bat` to start the application

### Linux/Mac Users

1. Clone this repository or download the files
2. Open terminal in the project directory
3. Make the scripts executable:
   ```bash
   chmod +x setup.sh run.sh
   ```
4. Run the setup script:
   ```bash
   ./setup.sh
   ```
5. Add your Google Maps API key (see Configuration section)
6. Run the application:
   ```bash
   ./run.sh
   ```

## Configuration

Before running the application, you need to set up your Google Maps API key. You have two options:

### Option 1: Environment Variable
Create a `.env` file in the project root: 