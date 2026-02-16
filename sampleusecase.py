import os
from dotenv import load_dotenv
from groq import Groq
import wikipedia
import requests


# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = Groq(api_key=API_KEY)

def fetch_from_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options}"
    except wikipedia.exceptions.PageError:
        return "No Wikipedia page found for the query."

def fetch_from_google(query):
    # Example Google Search API (replace with actual implementation if needed)
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key=YOUR_GOOGLE_API_KEY"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("items", [{}])[0].get("snippet", "No relevant result found.")
    return "Failed to fetch data from Google."

def main():
    question = input("Ask a general knowledge question: ")
    print("Fetching data...")
    
    # Fetch data from Wikipedia
    wiki_data = fetch_from_wikipedia(question)
    if "No Wikipedia page found" not in wiki_data:
        print("Answer from Wikipedia:")
        print(wiki_data)
        return
    
    # If Wikipedia fails, fetch from Google
    google_data = fetch_from_google(question)
    if "Failed to fetch data" not in google_data:
        print("Answer from Google:")
        print(google_data)
        return
    
    # If all fails, use Groq LLM
    print("Using Groq LLM to rethink the answer...")
    # response = llm.complete(prompt=f"Answer this question accurately: {question}")
    # print("Answer from Groq LLM:")
    # print(response)
    chat_completion = llm.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {"role": "system", "content": "Answer accurately and concisely."},
        {"role": "user", "content": f"Answer this question accurately: {question}"},
    ],
)

response_text = chat_completion.choices[0].message.content
print(response_text)

if __name__ == "__main__":
    main()