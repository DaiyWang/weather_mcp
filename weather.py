# weather.py

from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import logging # Adicione esta linha para logging

# Configure basic logging to stdout (Easypanel will capture this)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    logger.info("Initializing FastMCP server...")
    mcp = FastMCP("weather")
    logger.info("FastMCP server initialized successfully.")
except Exception as e:
    logger.error(f"Error during FastMCP initialization: {e}", exc_info=True)
    # Re-raise the exception to make sure the process fails if this happens
    raise

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Funções auxiliares (make_nws_request, format_alert) - MANTENHA-AS IGUAIS
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error in make_nws_request for URL {url}: {e}", exc_info=True)
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

# Implementação das ferramentas (get_alerts, get_forecast) - MANTENHA-AS IGUAIS
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.
    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    logger.info(f"Calling get_alerts for state: {state}")
    try:
        url = f"{NWS_API_BASE}/alerts/active/area/{state}"
        data = await make_nws_request(url)

        if not data or "features" not in data:
            return "Unable to fetch alerts or no alerts found."

        if not data["features"]:
            return "No active alerts for this state."

        alerts = [format_alert(feature) for feature in data["features"]]
        return "\n---\n".join(alerts)
    except Exception as e:
        logger.error(f"Error in get_alerts tool for state {state}: {e}", exc_info=True)
        return "An internal error occurred while fetching alerts."

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    logger.info(f"Calling get_forecast for lat: {latitude}, lon: {longitude}")
    try:
        # First get the forecast grid endpoint
        points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
        points_data = await make_nws_request(points_url)

        if not points_data:
            return "Unable to fetch forecast data for this location."

        # Get the forecast URL from the points response
        forecast_url = points_data["properties"]["forecast"]
        forecast_data = await make_nws_request(forecast_url)

        if not forecast_data:
            return "Unable to fetch detailed forecast."

        # Format the periods into a readable forecast
        periods = forecast_data["properties"]["periods"]
        forecasts = []
        for period in periods[:5]:  # Only show next 5 periods
            forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
            forecasts.append(forecast)

        return "\n---\n".join(forecasts)
    except Exception as e:
        logger.error(f"Error in get_forecast tool for lat {latitude}, lon {longitude}: {e}", exc_info=True)
        return "An internal error occurred while fetching forecast."

# --- AQUI É A CHAVE ---
# 'mcp' em si deve ser o callable ASGI para a versão mais recente do mcp[cli].
# Se isso não funcionar, é uma limitação da biblioteca ou ambiente.
app = mcp

if __name__ == "__main__":
    import uvicorn
    logger.info("Attempting to run Uvicorn server locally...")
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.critical(f"Fatal error running Uvicorn: {e}", exc_info=True)
