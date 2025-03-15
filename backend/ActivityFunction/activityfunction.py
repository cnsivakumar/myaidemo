@app.function_name("ActivityFunction")
@app.durable_activity_trigger(input_name="input_data")
def activity_function(input_data: dict):
    indexer_name = input_data.get("indexer_name", "my-indexer")
    search_service_url = input_data.get("search_service_url")
    api_key = input_data.get("api_key")

    headers = {"Content-Type": "application/json", "api-key": api_key}
    response = requests.get(f"{search_service_url}/indexers/{indexer_name}/status", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to get indexer status: {response.text}")
        return {"error": "Failed to retrieve indexer status"}