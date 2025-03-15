import azure.functions as func
import azure.durable_functions as df
import logging
import json
import time
import requests
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

### 1. Blob Trigger Function (Detects New Data) ###
@app.function_name("BlobTriggerFunction")
@app.blob_trigger(arg_name="blob",
                  path="my-container/{name}",
                  connection="AzureWebJobsStorage")
def blob_trigger_function(blob: func.InputStream):
    logging.info(f"New blob detected: {blob.name}")
    return f"Blob {blob.name} processed."

### 2. Orchestrator Function (Manages Workflow) ###
@app.function_name("OrchestratorFunction")
@app.durable_function()
def orchestrator_function(context: df.DurableOrchestrationContext):
    input_data = context.get_input()
    
    # Call Activity Function to check indexer status
    result = yield context.call_activity("ActivityFunction", input_data)
    
    return result

### 3. Activity Function (Check Indexer Status) ###
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

### 4. Durable Function Starter (HTTP Trigger) ###
@app.function_name("DurableFunctionStarter")
@app.route(route="start")
@app.durable_client_input(client_name="client")
def durable_function_starter(req: func.HttpRequest, client: df.DurableOrchestrationClient):
    request_body = req.get_json()
    
    instance_id = client.start_new("OrchestratorFunction", None, request_body)
    
    return func.HttpResponse(f"Started orchestration with ID = '{instance_id}'")
