import requests

SEARCH_SERVICE = "your-search-service"
API_KEY = "your-api-key"
INDEXER_NAME = "blob-indexer"

def main(name: str) -> str:
    url = f"https://{SEARCH_SERVICE}.search.windows.net/indexers/{INDEXER_NAME}/status?api-version=2023-07-01-Preview"
    headers = {"api-key": API_KEY}

    response = requests.get(url, headers=headers).json()

    if response.get("lastResult") and response["lastResult"].get("status") == "success":
        return "success"
    
    return "in_progress"
