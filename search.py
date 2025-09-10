# search.py
# A Python script to perform a search using the OpenRouter API.

import os
import json
import requests
import time

# OpenRouter API Endpoint
# You can change the model name in the URL to use a different one.
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Get the API key and query from environment variables set by the GitHub Action
API_KEY = os.environ.get("OPENROUTER_API_KEY")
USER_QUERY = os.environ.get("SEARCH_QUERY")

if not API_KEY:
    print("Error: OPENROUTER_API_KEY environment variable is not set.", file=os.stderr)
    exit(1)

if not USER_QUERY:
    print("Error: SEARCH_QUERY environment variable is not set.", file=os.stderr)
    exit(1)

# Construct the payload for the OpenRouter API request.
# The ":online" suffix enables the built-in web search feature.
# This may incur an additional cost.
payload = {
    "model": "google/gemini-flash-1.5:online", # The :online suffix enables web search
    # An alternative is to use the plugins parameter for more control:
    # "model": "google/gemini-flash-1.5",
    # "plugins": [{"id": "web"}],
    "messages": [
        {
            "role": "user",
            "content": USER_QUERY
        }
    ]
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def perform_search():
    """Performs the API request with exponential backoff for retries."""
    retries = 0
    max_retries = 3
    delay = 1  # seconds

    while retries < max_retries:
        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}", file=os.stderr)
            print(f"Retrying in {delay} seconds...", file=os.stderr)
            retries += 1
            time.sleep(delay)
            delay *= 2
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}", file=os.stderr)
            exit(1)
    
    print("Failed to get a response after multiple retries.", file=os.stderr)
    exit(1)

# Execute the search
try:
    result = perform_search()
    candidate = result.get('choices', [None])[0]

    if candidate and candidate.get('message') and candidate['message'].get('content'):
        generated_text = candidate['message']['content']
        
        # Print the generated text for the GitHub Action to use.
        print("Response:")
        print(generated_text)

        # Check for and print citations from the annotations
        annotations = candidate['message'].get('annotations', [])
        sources = [anno['url_citation'] for anno in annotations if anno['type'] == 'url_citation']

        if sources:
            print("\nSources:")
            for source in sources:
                print(f"- {source.get('title', 'No Title')} ({source.get('url', '#')})")
    else:
        print("No valid response from the API.", file=os.stderr)

except Exception as e:
    print(f"An unexpected error occurred: {e}", file=os.stderr)
    exit(1)
