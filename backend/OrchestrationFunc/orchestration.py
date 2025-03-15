@app.function_name("OrchestratorFunction")
@app.durable_function()
def orchestrator_function(context: df.DurableOrchestrationContext):
    input_data = context.get_input()
    
    # Call Activity Function to check indexer status
    result = yield context.call_activity("ActivityFunction", input_data)
    
    return result