from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from pathlib import Path
from .api import search_places, get_place_details
import os
from dotenv import load_dotenv
import pandas as pd
from typing import List
from pydantic import BaseModel
from io import BytesIO
import csv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Try to get API key from different sources
def get_api_key():
    # First try environment variable
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    # Then try .env file (should be handled by load_dotenv)
    if not api_key:
        try:
            with open('.env') as f:
                for line in f:
                    if line.startswith('GOOGLE_MAPS_API_KEY='):
                        api_key = line.split('=')[1].strip()
                        break
        except FileNotFoundError:
            pass
    
    # Finally try secrets.toml
    if not api_key:
        try:
            import tomli
            with open('.streamlit/secrets.toml', 'rb') as f:
                secrets = tomli.load(f)
                api_key = secrets.get('GOOGLE_MAPS_API_KEY')
        except:
            pass
    
    if not api_key:
        raise ValueError("No API key found in environment variables, .env file, or secrets.toml")
    
    return api_key

# Get API key
try:
    api_key = get_api_key()
except ValueError as e:
    print(f"Error: {e}")
    api_key = None

# Initialize FastAPI with error handling for missing API key
app = FastAPI(title="Places Data Gatherer")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Add this class for request validation
class ExportRequest(BaseModel):
    place_ids: List[str]
    format: str = "csv"

@app.get("/")
async def home(request: Request):
    if not api_key:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "title": "Error",
                "message": "API key not found. Please set GOOGLE_MAPS_API_KEY in your environment variables."
            }
        )
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Places Data Gatherer"}
    )

@app.get("/api/search")
async def search(query: str, max_results: int = 20, min_rating: float = 0):
    try:
        results = await search_places(query, api_key, max_results)
        if min_rating > 0:
            results = [r for r in results if float(r.get('rating', 0) or 0) >= min_rating]
        return JSONResponse(content={"results": results})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/export")
async def export_data(request: ExportRequest):
    try:
        detailed_data = []
        for place_id in request.place_ids:
            details = await get_place_details(place_id, api_key)
            if details:
                detailed_data.append(details)
        
        if not detailed_data:
            raise HTTPException(status_code=400, detail="No data to export")

        # Convert to DataFrame and export
        df = pd.DataFrame(detailed_data)
        
        # Save to exports directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"places_export_{timestamp}.{request.format}"
        filepath = os.path.join("exports", filename)
        os.makedirs("exports", exist_ok=True)
        
        if request.format == "csv":
            df.to_csv(filepath, index=False, encoding='utf-8-sig', 
                     quoting=csv.QUOTE_MINIMAL,
                     quotechar='"')
        else:
            df.to_excel(filepath, index=False, engine='openpyxl')
        
        # Return the file
        return FileResponse(
            filepath,
            filename=filename,
            media_type="text/csv" if request.format == "csv" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/settings")
async def settings_page(request: Request):
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "title": "Settings",
            "current_api_key": api_key[-8:] if api_key else None  # Only show last 8 chars
        }
    )

@app.post("/api/settings/apikey")
async def save_api_key(api_key_data: dict = Body(...)):
    new_api_key = api_key_data.get('api_key')
    if not new_api_key:
        raise HTTPException(status_code=400, detail="API key is required")
    
    # Save to .env file
    with open('.env', 'w') as f:
        f.write(f'GOOGLE_MAPS_API_KEY={new_api_key}\n')
    
    return {"message": "API key saved successfully"}

@app.get("/exports")
async def exports_page(request: Request):
    exports = []
    exports_dir = "exports"
    os.makedirs(exports_dir, exist_ok=True)
    
    for filename in os.listdir(exports_dir):
        filepath = os.path.join(exports_dir, filename)
        stat = os.stat(filepath)
        exports.append({
            "filename": filename,
            "date": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "format": filename.split('.')[-1].upper(),
            "size": f"{stat.st_size / 1024:.1f} KB"
        })
    
    return templates.TemplateResponse(
        "exports.html",
        {
            "request": request,
            "title": "Past Exports",
            "exports": sorted(exports, key=lambda x: x['date'], reverse=True)
        }
    )

@app.get("/exports/download/{filename}")
async def download_export(filename: str):
    filepath = os.path.join("exports", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Export not found")
    
    return FileResponse(
        filepath,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.delete("/exports/delete/{filename}")
async def delete_export(filename: str):
    filepath = os.path.join("exports", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Export not found")
    
    os.remove(filepath)
    return {"message": "Export deleted successfully"} 