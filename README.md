# Weather Microservice

This project is a FastMCP-based weather microservice that fetches weather data and alerts from WeatherAPI.com. It can be run as a server for MCP integration or as a CLI for city-specific forecasts.

This project is based upon the MCP Server quickstart found [here](https://modelcontextprotocol.io/quickstart/server)

## Features
- Fetches 3-day weather forecasts and weather alerts for any location (by latitude/longitude)
- Exposes MCP tools for programmatic access
- Asynchronous HTTP requests for fast API calls

## Setup
- Python 3.10+
- Install dependencies with `uv` , if necessary:
  ```
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- Set your free WeatherAPI key from https://www.weatherapi.com in a `.env` file:
  ```
  WEATHER_API_KEY=your_api_key_here
  ```

NB. More details on the WeatherAPI can be found [here](https://app.swaggerhub.com/apis-docs/WeatherAPI.com/WeatherAPI/1.0.2)

- Set up the virtual python environment

```sh
# Create a new directory for our project
uv init weather
cd weather

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]" httpx dotenv
```


## Usage
Run the following command start the MCP server, which will listen for messages from MCP hosts.
```
uv run weather.py
```


## Key Files
- `weather.py`: Main logic,  MCP server, API integration
- `.env`: Stores API keys


---
This project is designed for easy integration and quick weather lookups. For more details, see the code in `weather.py`.
