import json
import os
from datetime import datetime
import numpy as np
import openai
from tenacity import wait_random_exponential, stop_after_attempt, retry


def parse_chatgpt_response(bot_response, index=-1):
    response_split = bot_response.split('||')
    response_parse = response_split[index]
    bot_response_split = response_parse.replace('Content: ', '')

    return bot_response_split


class OpenAiHelper:
    def __init__(self):
        self.api_key: str = os.getenv('OPENAI_API_KEY')
        self.organization: str = os.getenv('OPENAI_ORGANIZATION')
        self.completion_engine: str = 'gpt-3.5-turbo-16k'
        self.embedding_engine: str = 'text-embedding-ada-002'
        self.max_tokens: int = 10000
        self.temperature: float = 0.75

    @retry(wait=wait_random_exponential(multiplier=1, max=3), stop=stop_after_attempt(8))
    def get_embedding(self, content):
        """
        this function gets the embedding from OpenAI

        :param content:
        :return:
        """
        print('==== Contacting OpenAI Embeddings API ====')
        openai_api_key = os.getenv("OPENAI_API_KEY")
        # fix any UNICODE errors
        embedding_message = json.dumps(content).encode(encoding='ASCII', errors='ignore').decode()
        try:
            # create the embedding
            response = openai.Embedding.create(
                input=embedding_message,
                engine=self.embedding_engine,
                api_key=self.api_key
            )
            # vectorize the embedding and return it
            vector = response['data'][0]['embedding']

            print("==== Embeddings Successfull ====")
            return np.array(vector).astype(np.float32)
        except Exception as e:
            print(f"Error while getting Open AI Embeddings: {e}")

    @retry(wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(8))
    async def chatgpt_completion(self, messages):
        openai_api_key = self.api_key
        print('==== Contacting OpenAI Chat Completion API ====')
        try:
            chatgpt_response = openai.ChatCompletion.create(messages=messages, model="gpt-4",
                                                            api_key=openai_api_key, temperature=self.temperature,
                                                            max_tokens=self.max_tokens)
            assistant_response = chatgpt_response['choices'][0]['message']['content']
            print('============= Response Received =============')
            print(assistant_response)
        except Exception as e:
            assistant_response = f"Sorry, I'm not feeling well, I just need a moment, please... @technomoonbase @JIWallin3 {e}"

        return assistant_response
