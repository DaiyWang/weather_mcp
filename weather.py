# weather.py

from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP # Importação existente

# Initialize FastMCP server
mcp = FastMCP("weather") # Inicialização existente

# Constants
NWS_API_BASE = "https://api.weather.gov" # Constante existente
USER_AGENT = "weather-app/1.0" # Constante existente

async def make_nws_request(url: str) -> dict[str, Any] | None: # Função existente
    """Make a request to the NWS API with proper error handling.""" # Docstring existente
    headers = { # Headers existentes
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client: # Cliente HTTPX existente
        try: # Bloco try existente
            response = await client.get(url, headers=headers, timeout=30.0) # Requisição GET existente
            response.raise_for_status() # Verificação de status existente
            return response.json() # Retorno JSON existente
        except Exception: # Bloco except existente
            return None # Retorno None em caso de erro existente

def format_alert(feature: dict) -> str: # Função existente
    """Format an alert feature into a readable string.""" # Docstring existente
    props = feature["properties"] # Propriedades existentes
    return f""" # Formatação de string existente
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool() # Decorador de tool existente
async def get_alerts(state: str) -> str: # Função existente
    """Get weather alerts for a US state. # Docstring existente

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}" # URL de alertas existente
    data = await make_nws_request(url) # Requisição de alertas existente

    if not data or "features" not in data: # Verificação de dados existente
        return "Unable to fetch alerts or no alerts found." # Mensagem de erro existente

    if not data["features"]: # Verificação de features existente
        return "No active alerts for this state." # Mensagem de ausência de alertas existente

    alerts = [format_alert(feature) for feature in data["features"]] # Formatação de alertas existente
    return "\n---\n".join(alerts) # Retorno de alertas formatados existente

@mcp.tool() # Decorador de tool existente
async def get_forecast(latitude: float, longitude: float) -> str: # Função existente
    """Get weather forecast for a location. # Docstring existente

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}" # URL de pontos existente
    points_data = await make_nws_request(points_url) # Requisição de pontos existente

    if not points_data: # Verificação de dados de pontos existente
        return "Unable to fetch forecast data for this location." # Mensagem de erro existente

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"] # URL de previsão existente
    forecast_data = await make_nws_request(forecast_url) # Requisição de previsão existente

    if not forecast_data: # Verificação de dados de previsão existente
        return "Unable to fetch detailed forecast." # Mensagem de erro existente

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"] # Períodos de previsão existente
    forecasts = [] # Lista de previsões existente
    for period in periods[:5]:  # Only show next 5 periods # Loop de períodos existente
        forecast = f""" # Formatação de previsão existente
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast) # Adição à lista de previsões existente

    return "\n---\n".join(forecasts) # Retorno de previsões formatadas existente

# --- AQUI ESTÁ A CHAVE ---
# O objeto `mcp` da classe `FastMCP` JÁ É a sua aplicação FastAPI (ASGI)
# Vamos renomeá-lo ou referenciá-lo como 'app' para que o Uvicorn o encontre.
app = mcp # 'app' agora é a instância da aplicação FastAPI/ASGI

if __name__ == "__main__":
    import uvicorn
    # Executa a aplicação ASGI com uvicorn.
    uvicorn.run(app, host="0.0.0.0", port=8000)
