import os
import json
import httpx
from typing import Optional
from plugins.utils.utils import current_request, require_permission, Permission

# API Configuration
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
API_KEY_ENV_VAR = "ALPHA_VANTAGE_API_KEY"

async def fetch_market_data(function: str, symbol: str) -> Optional[dict]:
    """Fetch data from Alpha Vantage API with proper error handling."""
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        print(f"Warning: {API_KEY_ENV_VAR} not set. Financial data functionality disabled.")
        return None
        
    # Build request parameters
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
        "datatype": "json"
    }
    
    # Make the API request
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            # Check for API error messages
            if "Error Message" in data:
                return {"error": data["Error Message"]}
                
            return data
        except Exception as e:
            return {"error": f"Failed to fetch market data: {str(e)}"}

def register_tool(mcp):
    """Register financial data tools with the MCP server"""
    
    @mcp.tool()
    @require_permission(Permission.READ_DATA)
    async def get_stock_quote(symbol: str) -> str:
        """
        Get real-time stock quote data for a given ticker symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
        """
        # Get user context
        request = current_request.get()
        user = getattr(request.state, "user", {})
                
        # Fetch the stock quote data
        data = await fetch_market_data("GLOBAL_QUOTE", symbol)
        
        if not data:
            return "Error: Financial data service unavailable. Make sure symbol exists and ALPHA_VANTAGE_API_KEY is set correctly."
            
        if "error" in data:
            return f"Error: {data['error']}"
            
        if "Global Quote" not in data or not data["Global Quote"]:
            return f"No quote data found for symbol: {symbol}"
            
        # Format the response
        quote = data["Global Quote"]
        return json.dumps({
            "symbol": quote.get("01. symbol", ""),
            "price": quote.get("05. price", ""),
            "change": quote.get("09. change", ""),
            "change_percent": quote.get("10. change percent", ""),
            "volume": quote.get("06. volume", ""),
            "latest_trading_day": quote.get("07. latest trading day", "")
        }, indent=2)

    @mcp.tool()
    @require_permission(Permission.READ_DATA)
    async def get_company_overview(symbol: str) -> str:
        """
        Get company overview data including financial metrics and company information.
        
        Args:
            symbol: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
        """
        # Get user context for potential tenant-specific logic
        request = current_request.get()
        user = getattr(request.state, "user", {})
        
        # Fetch the company overview data
        data = await fetch_market_data("OVERVIEW", symbol)
        
        if not data:
            return "Error: Financial data service unavailable. Make sure symbol exists and ALPHA_VANTAGE_API_KEY is set correctly."
            
        if "error" in data:
            return f"Error: {data['error']}"
            
        if not data or len(data) <= 1:
            return f"No company data found for symbol: {symbol}"
            
        # Return the formatted data
        essential_fields = [
            "Symbol", "Name", "Description", "Exchange", "Industry", 
            "PERatio", "MarketCapitalization", "DividendYield",
            "52WeekHigh", "52WeekLow", "EPS", "RevenueTTM"
        ]
        
        filtered_data = {k: v for k, v in data.items() if k in essential_fields}
        return json.dumps(filtered_data, indent=2)
