import json
import OpenAI
from dotenv import load_dotenv

load_dotenv()


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
async def openai_chat_completion(self, messages):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI()
    print('==== Contacting OpenAI Chat Completion API ====')
    try:
        response = openai.ChatCompletion.create(messages=messages, model="gpt-4", api_key=openai_api_key, temperature=0)
        response_content = response['choices'][0]['message']['content']
        print('============= Response Received =============')
        print(response_content)
    except Exception as e:
        response_content = f"Sorry, I'm not feeling well, I just need a moment, please... @technomoonbase @JIWallin3 {e}"

    return response_content
