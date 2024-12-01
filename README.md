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
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

### Option 2: Streamlit Secrets
Create a `.streamlit/secrets.toml` file:
```toml
GOOGLE_MAPS_API_KEY = "your_api_key_here"
```

## Usage

1. Start the application using the appropriate run script
2. Enter a search term (e.g., "restaurants", "plumbers", "nail salon")
3. Enter a location (e.g., "New York", "Berlin", "Ljubljana")
4. Click "Run Scraper"
5. Wait for the scraping to complete
6. Download the results using the file browser section

## Cost Considerations

The application uses the Google Places API, which has associated costs:
- Text Search: $0.017 per request (returns up to 20 results)
- Place Details: $0.017 per request (one per business)
- Free monthly credit: $200

The application is configured to limit results to 60 businesses per search to control costs.

## File Structure

```
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── setup.bat           # Windows setup script
├── setup.sh            # Unix setup script
├── run.bat             # Windows run script
├── run.sh              # Unix run script
├── .gitignore          # Git ignore file
└── scraper_results/    # Directory for CSV exports
```

## Output Format

The scraper generates CSV files with the following columns:
- Company Name
- Address
- Phone Number
- Website
- Email
- Opening Hours
- Google Maps URL
- Rating
- User Ratings Total

All files are saved with UTF-8 encoding to properly handle international characters.

## Error Handling

The application includes error handling for:
- Missing API key
- API request failures
- Rate limiting
- Network issues
- Invalid search parameters

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

Please ensure you comply with Google's Terms of Service and usage limits when using this application. The developer is not responsible for any misuse or violation of Google's terms of service.

## Support

If you encounter any issues or have questions, please open an issue in the GitHub repository.

## Acknowledgments

- Google Places API documentation
- Streamlit community
- Contributors and users who provide feedback
