@app.function_name("DurableFunctionStarter")
@app.route(route="start")
@app.durable_client_input(client_name="client")
def durable_function_starter(req: func.HttpRequest, client: df.DurableOrchestrationClient):
    request_body = req.get_json()
    
    instance_id = client.start_new("OrchestratorFunction", None, request_body)
    
    return func.HttpResponse(f"Started orchestration with ID = '{instance_id}'")