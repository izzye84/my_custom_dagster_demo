from datetime import datetime
from pydantic import PrivateAttr
import requests
import time
from typing import Any, Dict, List

from dagster import asset, AssetExecutionContext, Config, ConfigurableResource, Field, MetadataValue
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd


class GoogleSheetsResource(ConfigurableResource):
    credentials_file: str = "/Users/izzy/Downloads/google_credentials.json"
    spreadsheet_id: str = "1Qlp3HVaJd0PHvb546rA0SgqtMsTO56Yp5fPWm6M04YU"
    scopes: list[str] = ["https://www.googleapis.com/auth/spreadsheets"]
    _service: Any = PrivateAttr(default=None)
    
    def setup_resource(self):
        """Initialize the Google Sheets service."""
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file,
            scopes=self.scopes
        )
        self._service = build('sheets', 'v4', credentials=credentials)
    
    def get_values(self, range_name: str) -> Dict:
        """Read values from a Google Sheet."""
        if self._service is None:
            self.setup_resource()
        
        result = self._service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_name
        ).execute()
        return result
    
    def update_values(self, range_name: str, values: list) -> Dict:
        """Write values to a Google Sheet."""
        if self._service is None:
            self.setup_resource()
        body = {"values": values}
        result = self._service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED", # Alternatively, can specify RAW
            body=body
        ).execute()
        return result


@asset(config_schema={"range": Field(str, default_value="A3:B6")},
       kinds={"python", "googlesheets"})
def get_lat_long(context, google_sheets: GoogleSheetsResource) -> Dict:
    """
    Reads a Google sheet and returns values as a dictionary
    """
    # Get range from asset config
    range_value = context.op_config["range"]
    
    # Use the resource's method to get values
    result = google_sheets.get_values(range_value)
    
    # Log the result for debugging
    context.log.info(f"Read data: {result}")
    
    return result


class WeatherAPIConfig(Config):
    """Configuration for the weather API call"""
    temperature_unit: str = "fahrenheit"
    wind_speed_unit: str = "mph"
    timezone: str = "PST"


@asset(kinds={"python", "api"})
def get_weather_details(context: AssetExecutionContext,
                        get_lat_long: Dict,
                        config: WeatherAPIConfig) -> List:
    """
    Fetches weather data for each location from the Open-Meteo API.
    """
    weather_data = []
    values = get_lat_long.get('values', [])
    
    for row in values[0:]:  # Start from index 1 to skip header
        # Extract latitude and longitude from the row
        lat = row[0]
        lng = row[1]
        
        context.log.info(f"Fetching weather for location: {lat}, {lng}")
        
        # Construct the API URL
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lng}"
            f"&current_weather=true"
            f"&temperature_unit={config.temperature_unit}"
            f"&wind_speed_unit={config.wind_speed_unit}"
            f"&timezone={config.timezone}"
        )
        
        # Make the API request
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            current = data.get('current_weather', {})
            
            time_str = current.get('time')  # Defaults to ISOS: "2025-03-02T22:15"
            # Parse and convert to desired format
            if time_str:
                # Parse the ISO format time
                dt = datetime.fromisoformat(time_str)
                
                # Format to YYYY-MM-DD HH:MM AM/PM
                formatted_time = dt.strftime('%Y-%m-%d %I:%M %p')
            else:
                formatted_time = ""
            
            weather_info = {
                'latitude': lat,
                'longitude': lng,
                'temperature': f"{current.get('temperature')} F",
                'wind_speed': f"{current.get('windspeed')} mph",
                'timestamp': formatted_time
            }
            
            weather_data.append(weather_info)
            
            # Add a small delay to avoid hitting API rate limits
            time.sleep(0.5)
        else:
            context.log.error(f"Error fetching weather for {lat},{lng}: {response.status_code}")

    # Convert weather_data to a DataFrame
    df = pd.DataFrame(weather_data)
    
    # Attach the DataFrame as metadata
    context.add_output_metadata({
        "weather_data": MetadataValue.md(df.to_markdown())
    })
    
    return weather_data


class UpdateGoogleSheetConfig(Config):
    range: str = "C3:E6"

@asset(
    kinds={"python", "googlesheets"},
    metadata={
        "google_sheet_link": MetadataValue.url("https://docs.google.com/spreadsheets/d/1Qlp3HVaJd0PHvb546rA0SgqtMsTO56Yp5fPWm6M04YU/edit?gid=0#gid=0")
    }
)
def update_google_sheet(context: AssetExecutionContext,
                        get_weather_details: List[Dict],
                        google_sheets: GoogleSheetsResource,
                        config: UpdateGoogleSheetConfig) -> None:
    """
    Updates the Google Sheet with the current temperature, wind speed, and last updated time.
    """
    # Prepare the data to update in the sheet
    values_to_update = []
    for data in get_weather_details:
        values_to_update.append([
            data['temperature'],
            data['wind_speed'],
            data['timestamp']
        ])
    
    # Define the range to update in the Google Sheet
    range_name = config.range
    
    # Use the resource's method to update values
    google_sheets.update_values(range_name, values_to_update)
    
    # Log the update for debugging
    context.log.info(f"Updated Google Sheet with weather data: {values_to_update}")


# Instantiate the resource
google_sheets_resource = GoogleSheetsResource()