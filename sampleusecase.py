import os  # Import built-in OS module to access environment variables and OS utilities
from dotenv import load_dotenv  # Import helper to load environment variables from a .env file
from groq import Groq  # Import Groq client to call the Groq LLM API
import wikipedia  # Import wikipedia library to query Wikipedia summaries
import requests  # Import requests library to make HTTP calls (Google API request) 
#All these imports are necessary for the functionality of the program, including environment management, LLM interaction, and data fetching from external sources.


# Load API key from .env file  # Comment describing the purpose of loading secrets from .env
load_dotenv()  # Load variables from .env into the process environment
API_KEY = os.getenv("GROQ_API_KEY")  # Read the GROQ API key from environment variables

# Initialize Groq LLM  # Comment describing the LLM client initialization
llm = Groq(api_key=API_KEY)  # Create a Groq client instance using the API key

def fetch_from_wikipedia(query):  # Define a function to fetch a short answer from Wikipedia
    try:  # Start a try block to handle Wikipedia lookup errors safely
        return wikipedia.summary(query, sentences=2)  # Return a 2-sentence summary for the query
    except wikipedia.exceptions.DisambiguationError as e:  # Handle ambiguous queries with multiple possible pages
        return f"Multiple results found: {e.options}"  # Return the list of disambiguation options as a message
    except wikipedia.exceptions.PageError:  # Handle the case where no page exists for the query
        return "No Wikipedia page found for the query."  # Return a friendly "not found" message

def fetch_from_google(query):  # Define a function to fetch a result snippet from Google Custom Search
    # Example Google Search API (replace with actual implementation if needed)  # Note that this is a placeholder approach
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key=YOUR_GOOGLE_API_KEY"  # Build the Google API URL (API key is a placeholder)
    response = requests.get(url)  # Send an HTTP GET request to the Google Search API endpoint
    if response.status_code == 200:  # Check if the HTTP response indicates success
        data = response.json()  # Parse the JSON response into a Python dictionary
        return data.get("items", [{}])[0].get("snippet", "No relevant result found.")  # Safely pull the first item's snippet (or fallback text)
    return "Failed to fetch data from Google."  # Return an error message if the request failed

def main():  # Define the main entry point function for user interaction
    question = input("Ask a general knowledge question: ")  # Prompt the user to type a question
    print("Fetching data...")  # Inform the user that the program is searching for an answer
    
    # Fetch data from Wikipedia  # Comment indicating the first fallback source (Wikipedia)
    wiki_data = fetch_from_wikipedia(question)  # Call Wikipedia fetch function using the user's question
    if "No Wikipedia page found" not in wiki_data:  # If Wikipedia returned a real answer (not the "not found" message)
        print("Answer from Wikipedia:")  # Print a label for the Wikipedia answer
        print(wiki_data)  # Print the returned Wikipedia summary text
        return  # Exit main early since we already found an answer
    
    # If Wikipedia fails, fetch from Google  # Comment indicating the second fallback source (Google)
    google_data = fetch_from_google(question)  # Call Google fetch function using the user's question
    if "Failed to fetch data" not in google_data:  # If Google returned something other than the failure message
        print("Answer from Google:")  # Print a label for the Google answer
        print(google_data)  # Print the Google snippet text
        return  # Exit main early since we found an answer
    
    # If all fails, use Groq LLM  # Comment indicating the final fallback source (LLM)
    print("Using Groq LLM to rethink the answer...")  # Tell the user you're calling the LLM now
    # response = llm.complete(prompt=f"Answer this question accurately: {question}")  # (Commented out) Example of a different Groq completion API call
    # print("Answer from Groq LLM:")  # (Commented out) Label for printing the LLM answer
    # print(response)  # (Commented out) Print the LLM raw response
    chat_completion = llm.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Answer accurately and concisely."},
            {"role": "user", "content": f"Answer this question accurately: {question}"},
        ],
    )

    response_text = chat_completion.choices[0].message.content
    print(response_text)


if __name__ == "__main__":  # Standard Python entry-point check to run only when executed directly
    main()  # Call main() to start the program flo