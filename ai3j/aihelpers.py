import os
import requests
from tenacity import wait_random_exponential, retry, stop_after_attempt
from dotenv import load_dotenv

load_dotenv()


@retry(wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(6))
def openai_chat_completion_http(messages):
    api_key = os.getenv('OPENAI_API_KEY')
    api_url = "https://api.openai.com/v1/chat/completions"

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    payload = {
        'model': 'gpt-4',
        'messages': messages,
    }

    completion_content = "No response received yet."
    try:
        response = requests.post(url=api_url, headers=headers, json=payload)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        completion_content = response.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as http_err:
        completion_content = f"HTTP error occurred: {http_err}"  # HTTP error
    except Exception as err:
        completion_content = f"Other error occurred: {err}"  # Other error

    return completion_content


def print_openai_completion_token_counts(response):
    response_usage = response.json()['usage']
    print('============= OpenAI Request Token Counts =============')
    print(response_usage)
    print(f"Prompt     Tokens: {response.json()['usage']['prompt_tokens']}")
    print(f"Completion Tokens: {response.json()['usage']['completion_tokens']}")
    print(f"Total      Tokens: {response.json()['usage']['total_tokens']}")
