from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import dotenv_values

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
WEATHER_API_BASE = "https://api.weatherapi.com/v1/"
config = dotenv_values(".env")
WEATHER_API_KEY = config.get("WEATHER_API_KEY", "")
USER_AGENT = "weather-app/1.0"

async def make_weather_request(url: str) -> dict[str, Any] | None:
    """Make a request to the weatherapi API call with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(alert: dict) -> str:
    """Format an alert feature into a readable string."""
    return f"""
Headline: {alert.get('headline', 'No headline available')}
Event: {alert.get('event', 'Unknown')}
Severity: {alert.get('severity', 'Unknown')}
Urgency: {alert.get('urgency', 'Unknown')}
Certainty: {alert.get('certainty', 'Unknown')}
Category: {alert.get('category', 'Unknown')}
Effective: {alert.get('effective', 'Unknown')}
Expires: {alert.get('expires', 'Unknown')}
Description: {alert.get('desc', 'No description available')}
Instructions: {alert.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(latitude: float, longitude: float) -> str:
    """Get weather alerts for a given location.
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    url = f"{WEATHER_API_BASE}/forecast.json?q={str(latitude)},{str(longitude)}&days=3&alerts=yes&key={WEATHER_API_KEY}"
    data = await make_weather_request(url)

    if not data or "alerts" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["alerts"]["alert"]:
        return "No active alerts for this location."

    alerts = [format_alert(alert) for alert in data["alerts"]["alert"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location anywhere in the world.
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    forecast_url = f"{WEATHER_API_BASE}/forecast.json?q={str(latitude)},{str(longitude)}&days=3&key={WEATHER_API_KEY}"
    forecast_data = await make_weather_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch forecast data for this location."

    # Format the periods into a readable forecast
    periods = forecast_data["forecast"]["forecastday"]
    forecasts = []
    for period in periods:
        forecast = f"""
{period['date']}:
MaxTemperature: {period['day']['maxtemp_c']}°C
MinTemperature: {period['day']['mintemp_c']}°C
Condition: {period['day']['condition']['text']}
Wind: {period['day']['maxwind_kph']} kph
Humidity: {period['day']['avghumidity']}%
Chance of Rain: {period['day']['daily_chance_of_rain']}%
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
