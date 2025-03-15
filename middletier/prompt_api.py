from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI

# Initialize FastAPI
app = FastAPI()

# Azure AI Search Credentials
SEARCH_SERVICE = "your-search-service"
INDEX_NAME = "tickets-index"
SEARCH_API_KEY = "your-api-key"

# Azure OpenAI Credentials
OPENAI_API_KEY = "your-openai-key"
DEPLOYMENT_NAME = "gpt-4"
ENDPOINT = "https://your-openai-instance.openai.azure.com"

# Initialize Azure Clients
search_client = SearchClient(f"https://{SEARCH_SERVICE}.search.windows.net", 
                             INDEX_NAME, 
                             AzureKeyCredential(SEARCH_API_KEY))

openai_client = AzureOpenAI(api_key=OPENAI_API_KEY, azure_endpoint=ENDPOINT)

# Request Model
class QueryRequest(BaseModel):
    question: str

# Function to Fetch Relevant Tickets
def fetch_relevant_tickets(user_query):
    results = search_client.search(user_query, top=3)  # Fetch top 3 relevant tickets
    formatted_results = "\n\n".join(
        [f"- {result['summary']}: {result['description']}" for result in results]
    )
    return formatted_results or "No relevant tickets found!."

# Function to Generate Answer Using Azure OpenAI
def generate_response(user_query):
    search_results = fetch_relevant_tickets(user_query)

    prompt = f"""
    You are an AI assistant helping application support engineers resolve tickets.

    Here are some similar resolved tickets:

    {search_results}

    Based on this information, answer the following question concisely:

    {user_query}
    """

    response = openai_client.completions.create(
        model=DEPLOYMENT_NAME,
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
    )

    return response.choices[0].text.strip()

# API Endpoint to Answer Questions
@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        answer = generate_response(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

