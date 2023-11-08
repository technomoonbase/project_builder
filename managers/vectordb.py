import pinecone
import os
from datetime import datetime
from chat.messages import Message, MessageCache


class PineconeClient:
    def __init__(self):
        self.api_key = os.getenv('PINECONE_API_KEY')
        self.environment = os.getenv('PINECONE_ENVIRONMENT')

    def create_index(self, index_name):
        pinecone.init(api_key=self.api_key, environment=self.environment)
        active_indexes = pinecone.list_indexes()
        if index_name in active_indexes:
            print(f"==== Index {index_name} already exists ====")
            return
        else:
            pinecone.create_index(index_name, dimension=1536, metric='cosine', pods=1, replicas=0, pod_type='s1')

    def delete_index(self, index_name):
        pinecone.init(api_key=self.api_key, environment=self.environment)
        active_indexes = pinecone.list_indexes()
        if index_name in active_indexes:
            pinecone.delete_index(index_name)
            print(f"==== Index {index_name} deleted ====")
            return
        else:
            print(f"==== Index {index_name} does not exist ====")
            return

    def upsert_new_message(self, new_message: Message, embeddings, index_name):
        pinecone.init(api_key=self.api_key, environment=self.environment)
        index = pinecone.Index(index_name=index_name)
        timestamp = str(datetime.now().strftime('%d-%b-%Y @ %I:%M%p'))
        role = 'assistant' if new_message.speaker_is_bot else 'user'
        metadata = {'id': new_message.uuid, 'author': new_message.speaker_name, 'content': new_message.content,
                    'created_at': timestamp, 'source': new_message.source, 'role': role}
        upsert_response = index.upsert([(new_message.uuid, embeddings, metadata)],
                                       namespace=f'alpha:discord:{new_message.source}')
        print(f"==== Upsert Response: {upsert_response}")
        return upsert_response

    def vector_search(self, embedding, top_k, include_metadata=True, namespace=None,
                      message_cache: MessageCache = None):
        pinecone.init(api_key=self.api_key, environment=self.environment)
        index = pinecone.Index(index_name='juliet42d')
        matches = index.query(vector=embedding, top_k=top_k, include_metadata=include_metadata,
                              namespace=namespace)

        context_list = []
        # for loop - Results in vector_search
        for m in matches['matches']:
            if m['uuid'] in message_cache.get_message_cache():
                print('Message already in chat history')
                continue
            else:
                context_list.append(m['metadata']['content'])

        return context_list