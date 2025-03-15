import azure.durable_functions as df
import requests
import time

SEARCH_SERVICE = "your-search-service"
API_KEY = "your-api-key"
INDEXER_NAME = "blob-indexer"

def orchestrator_function(context: df.DurableOrchestrationContext):
    # Step 1: Trigger AI Search Indexer
    url = f"https://{SEARCH_SERVICE}.search.windows.net/indexers/{INDEXER_NAME}/run?api-version=2023-07-01-Preview"
    headers = {"Content-Type": "application/json", "api-key": API_KEY}

    response = requests.post(url, headers=headers)

    if response.status_code == 202:
        # Step 2: Check indexer status periodically
        for _ in range(10):  # Retry for a few minutes
            status = yield context.call_activity("check_indexer_status")
            if status == "success":
                return "Indexing completed successfully"
            time.sleep(30)  # Wait before checking again

    return "Indexing failed or timed out"

main = df.Orchestrator.create(orchestrator_function)
