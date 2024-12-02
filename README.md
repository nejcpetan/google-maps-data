# Places Data Gatherer

A FastAPI-based web application that allows users to search and export business information from Google Maps using the Google Places API v1. The application provides a modern, responsive interface for searching businesses and exporting detailed information in multiple formats.

## Features

- Search businesses by keyword with customizable parameters:
  - Maximum number of results
  - Minimum rating filter
- Detailed business information export including:
  - Business Name
  - Business Type
  - Address
  - Phone Number
  - Website
  - Opening Hours
  - Rating and Review Count
  - Google Maps URL
- Export options:
  - CSV format
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

- Python 3.8 or higher
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
3. Adjust the maximum results and minimum rating if desired
4. Click Search
5. Select the businesses you want to export
6. Choose your export format (CSV or Excel)
7. Click Export Selected
8. Access your exports from the Exports page

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

## API Endpoints

- `GET /`: Main search interface
- `GET /api/search`: Search places
- `POST /api/export`: Export selected places
- `GET /exports`: View export history
- `GET /settings`: API key configuration

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
