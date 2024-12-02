# Places Data Gatherer with HubSpot Export

A FastAPI-based web application that allows users to search and export business information from Google Maps using the Google Places API v1. The application provides a modern, responsive interface for searching businesses and exporting detailed information in HubSpot-compatible formats.

## Features

- Advanced business search capabilities:
  - Search by keyword and location
  - Configurable maximum results (up to 1000)
  - Minimum rating filter
  - Pagination support for large result sets
- HubSpot-ready exports including:
  - Company record ID (using Google Place ID)
  - Company name
  - Phone number
  - Website URL
  - Street address
  - Business type
  - Business hours
  - Google Maps URL
  - Rating and review count
- Export options:
  - CSV format (HubSpot-compatible)
  - Excel format
- Modern, responsive UI with dark theme
- Export history management
- API key configuration interface

## Tech Stack

- **Python 3.12**
- **FastAPI**: Web application framework
- **Jinja2**: Template engine
- **HTTPX**: Async HTTP client
- **Pandas**: Data processing and export
- **DaisyUI + Tailwind CSS**: UI components and styling
- **JavaScript**: Client-side interactivity
- **Google Places API**: Business data source

## Prerequisites

- Python 3.12 or higher
- Google Maps API key with Places API enabled
- Internet connection

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd places-data-gatherer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Unix/MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your Google Maps API key (see Configuration section)

5. Run the application:
   ```bash
   python main.py
   ```
   or
   ```bash
   uvicorn main:app --reload
   ```

## Configuration

Before running the application, you need to set up your Google Maps API key. You have several options:

### Option 1: Environment Variable
Create a `.env` file in the project root:
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

### Option 2: Settings Interface
1. Start the application
2. Navigate to Settings
3. Enter your API key in the provided form

## Usage

1. Start the application and navigate to http://localhost:8000
2. Enter a search term (e.g., "restaurants in New York")
3. Set your desired maximum results (up to 1000)
4. Adjust the minimum rating if desired
5. Click Search
6. Select the businesses you want to export
7. Choose your export format (CSV for HubSpot)
8. Click Export Selected
9. Access your exports from the Exports page

## HubSpot Integration

The application generates CSV files that are ready for HubSpot import with:
- Proper field naming conventions
- Company record ID for deduplication
- Formatted phone numbers
- UTF-8 encoding with BOM
- Properly quoted fields
- Empty values handled correctly

## File Structure

```
├── app/
│   ├── __init__.py
│   ├── api.py          # Google Places API integration
│   ├── main.py         # FastAPI application
│   ├── static/         # Static assets
│   ├── templates/      # HTML templates
├── exports/            # Export files directory
├── main.py            # Application entry point
├── requirements.txt   # Python dependencies
└── .env              # Environment variables
```

## Error Handling

The application includes comprehensive error handling for:
- Missing or invalid API key
- API request failures
- Network issues
- Invalid search parameters
- Export processing errors

## Cost Considerations

The application uses the Google Places API v1, which has associated costs:
- Places Search: Costs apply per request
- Place Details: Costs apply per place
- Refer to Google's pricing documentation for current rates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided as-is. Users are responsible for complying with Google's Terms of Service and usage limits when using this application.

## Support

If you encounter any issues or have questions, please open an issue in the GitHub repository.
