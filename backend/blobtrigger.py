import azure.functions as func
import azure.durable_functions as df

async def main(blob: func.InputStream, starter: str):
    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("orchestrate_indexing", None)
    
    return f"Orchestration started with ID: {instance_id}"
