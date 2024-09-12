import requests
import json
import os
import logging
from sentiment import SentimentAnalyzer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Configuration
API_KEY = os.environ.get('API_KEY')
ENDPOINT = "https://teamfireopenapi.openai.azure.com/openai/deployments/teamfiredeployment01/chat/completions?api-version=2024-02-15-preview"

sentiment_analyzer = SentimentAnalyzer()

def chat_with_ai(client_input):
    # Get the score of input
    label, score = sentiment_analyzer.analyze(client_input)
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    # Adding sentiment label on client input and send to model
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant that helps people find information."
            },
            {
                "role": "user",
                "content": f"User input (Sentiment: {label} with score {score:.2f}): {client_input}"            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 2000
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return "I'm sorry, because there is a problem with request"

def main():
    print("Chat with TeamFire Agent (type 'bye' to exit)")
    while True:
        client_input = input("You: ")
        if client_input.lower() == 'bye':
            print("Goodbye!")
            break

        label, score = sentiment_analyzer.analyze(client_input)
        print(f"Sentiment: {label} (score: {score:.2f})")
        ai_response = chat_with_ai(client_input)
        print(f"AI: {ai_response}")

if __name__ == "__main__":
    main()