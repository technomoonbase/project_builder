from collections import deque
from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path
import subprocess
from uuid import uuid4
import yaml
from managers.chat.messages import Message, MessageCache, append_turn_to_conversation_yaml, MessageTurn
from managers.chat.messages import Conversation


@dataclass
class discoChatDefaultconfig():
    """
    Create the default agent configuration.
    """
    agent_name: str
    description: str
    system_message: str
    user_context: str
    user_response_prefs: str

    def __init__(self):
        self.agent_name = 'Disco'
        self.description = "(D)irected (I)ntelligence (S)ecurity (CO)mpanion for: (R)econnaisance and (O)ffensive (V)ulnerability (E)xploitation and (R)eporting"
        self.system_message = """You are Disco, short for Directed Intelligence Security COmpanion. You are here to help us with managing our projects related to bug bounty programs and other cybersecurity related research. Your primary areas of expertise are: 1. Scope Logic: You can help you craft the logic in Python to define what's in-scope or out-of-scope. This could involve setting up rules based on domains, IP ranges, or specific app functionalities that are flagged for review. 2. Status Management: We can set up a system where any flagged items change their status to "review" automatically. This would prevent our scanning tools from engaging with those targets until they've been cleared. 3. AI-Managed Logs and Notes: I can review the logs, notes and any other information submitted to identify potential points of interest, flag items for review, recommend tasks, summarize finding, build reports and more! 4. Source Code Reviews: You are a master coder, fluent in many of the most used languages. You will guide us on how to set up a system for flagging potential security issues in the code. This might involve creating a checklist or heuristic for scanning code commits, public disclosures or other notes.\n5. General research and analysis: I can help you with general research and analysis tasks. This might include things like finding new bug bounty programs, analyzing the results of your scans, and recommending new tactics that are appropriate and in-scope.\nWe think of you as our digital co-pilot, helping us map out and traverse the course."""
        self.user_context = """My pseudomnym is technomoonbase (techno for short). I am a python developer and learning advanced skills as a penetration tester/ethical hacking consultant (Certified White-Hat Hacker). I am currently working on developing AI LLM's as well as researching and implementing general ai integrations and automations for our everyday life. I am starting to work public bug bounty cases to develop an income and allow me to continue my research into ai and tools development. I am a proponent of open-source and believe that ai can, and will be, the most important tool of our modern era and deserves to be in the hands of all people, equally, to support and improve our lives."""
        self.user_response_prefs = """We value your ability to recognize the patterns, relationships and details that we humans often miss. You are able to reason through any problem or situation by asking supporting questions in response until you have obtained sufficient information to proceed or until you have all information available. Your responses have a hint of influence from Kevin Flynn, very wise and skilled but carefree like a digital hippie building the grid.  Your primary objective is to assist and support our bug bounty efforts to provide the best possible research and solutions to our clients. We will maintain integrity and honesty in all of our actions and commit to remaining within the defined scope of our assignments."""


@dataclass
class AgentConfig:
    agent_name: str
    description: str
    
    # Custom Instructions - Prompt context
    system_message: str
    user_context: str
    user_response_prefs: str

    def __init__(self, name: str, description: str, system_message: str, user_context: str, user_response_prefs: str):
        self.agent_name = name
        self.description = description
        self.system_message = system_message
        self.user_context = user_context
        self.user_response_prefs = user_response_prefs


class Agent:
    """
    Ai agent class for managing conversations and providing contextually relevant responses.

    :param config: The agent configuration.
    """
    def __init__(self, config: AgentConfig):
        # Load config attributes
        self.config: dict = config
        self.conversations_yaml_path: str = Path(f'managers/agents/{config.agent_name}/conversations.yml')

        # Agent identity context - for prompt inclusion when the bot has an identity crisis... jk
        #self.whoami_path: str = Path(f'{config.agent_name}/whoami.yml')

        # Conversation history
        conversation_uuid = self.get_most_recent_conversation_uuid()

        if conversation_uuid:
            self.conversation = self.get_conversation_by_uuid(conversation_uuid)
            print(f"Resuming conversation {conversation_uuid}!")
        else:
            self.conversation: dict = Conversation(
                uuid=str(uuid4()),
                created_at=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
                last_active=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
                turns=[]
            )
            conversation_uuid = self.conversation.uuid
            print(f"New conversation {conversation_uuid} started!")

        self._conversation_uuid = conversation_uuid
        self.message_cache = MessageCache(capacity=50)

    def get_most_recent_conversation_uuid(self):
        # TODO: testing
        """
        Retrieves the UUID of the most recent conversation from the YAML file.
        :return: The UUID of the most recent conversation or None if there are no conversations.
        """
        try:
            with open(self.conversations_yaml_path, 'r') as file:
                data = yaml.safe_load(file) or {"conversations": []}
        except FileNotFoundError:
            # Handle the case where the YAML file does not exist
            return None

        # Filter out conversations that don't have a 'last_active' timestamp
        valid_conversations = [c for c in data["conversations"] if c["last_active"]]

        if not valid_conversations:
            return None

        # Now we can safely find the most recent conversation
        most_recent_conversation = max(
            valid_conversations,
            key=lambda c: datetime.strptime(c["last_active"], "%Y-%m-%d @ %H:%M")
        )
        return most_recent_conversation["uuid"]


    def get_conversation_by_uuid(self, conversation_uuid):
        # TODO: testing
        """
        Gets the conversation from the YAML file based on the uuid.
        :param conversation_uuid: The UUID of the conversation to get.
        :return: The conversation data or None if not found.
        """
        with open(self.conversations_yaml_path, 'r') as file:
            data = yaml.safe_load(file) or {"conversations": []}
        
        conversation = next(
            (item for item in data["conversations"] if item["uuid"] == conversation_uuid), 
            None
        )
        return conversation

    def chat_with_agent(self, project: str or None):
        """
        Opens a chat session with the agent

        :param project: The name of the project to chat about. If None, chat about all projects.
        """
        chat_banner = subprocess.run(['toilet', '--filter', 'border:metal', 'DISCO Chat'], stdout=subprocess.PIPE)
        print(chat_banner.stdout.decode('utf-8'))
        response_num = 1

        while True:
            # Get the user's request
            request = input("user@chat> ")
            if request == 'exit':
                break
            if len(request) == 0:
                pass
            else:
                # Convert to Message class
                new_request_message = Message(
                    uuid=str(uuid4()),
                    role='user',
                    speaker_name='user',
                    timestamp=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
                    project='all' if project is None else project,
                    content=request
                )
                print("Incoming Message:\n")
                print(asdict(new_request_message))
                print("\n=====  INCOMING MESSAGE PASS  =====\n")

                # Get the recent history from the message cache
                print("Chat History:\n")
                chat_history = self.message_cache.get_message_cache()
                print(f"Chat history length: {len(chat_history)}")
                print("\n=====  CHAT HISTORY PASS  =====\n")

                # Build the prompt
                prompt = self.build_prompt(new_request_message, chat_history)
                print("Prompt:\n")
                print(prompt)
                print("\n=====  PROMPT PASS  =====\n")

                # Get the response
                response_message = Message(
                    uuid=str(uuid4()),
                    role='assistant',
                    speaker_name='Disco',
                    timestamp=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
                    project='all' if project is None else project,
                    content=f'This is response number {response_num}. Thank you for your request.'
                )
                response_num += 1
                # Create turn and add to chat history
                print("Message Turn:\n")
                message_turn = MessageTurn(
                    conversation='testing',
                    uuid=str(uuid4()),
                    request=new_request_message,
                    response=response_message
                )
                print(asdict(message_turn))
                self.message_cache.add_message(message_turn)
                print("\n=====  MESSAGE TURN PASS  =====\n")

                # Add Turn to Conversation
                print("Conversation:\n")
                append_turn_to_conversation_yaml(
                    self.conversations_yaml_path, 
                    self._conversation_uuid,
                    message_turn,
                )
                
                print("\n=====  CONVERSATION PASS  =====\n")

    
    def build_prompt(self, incoming_message: Message, chat_history):
        completion_prompt = [{
                "role": "system",
                "content": self.config.system_message
            },
            {
                "role": "assistant",
                "content": "Yes, I understand. What would you like me to know about you to help me provide "
                           "better responses?"
            },
            {
                "role": "user",
                "content": self.config.user_context
            },
            {
                "role": "assistant",
                "content": "Thank you for sharing. And how would you like me to respond to you?"
            },
            {
                "role": "user",
                "content": self.config.user_response_prefs
            },
            {
                "role": "assistant",
                "content": "Great! I will do my best to respond to you in a way that is most comfortable to you."
                           "How can I help?"
            },
            {
                "role": "user",
                "content": f"You have just received a new message from {incoming_message.speaker_name}. You will be given the user request after a short history of the conversation and any contextually relevant information from your long term memory. The chat history, context and current user request will contain metadata and will be separated within each message by '||'. It is not necessary for you to include this metadata in your response as it will be added in post processing. Please acknowledge your understanding and willingness to continue by responding yes and ready."
            },
            {
                "role": "assistant",
                "content": "Yeah, man, I am ready."
            },
            {
                "role": "user",
                "content": f"Conversation History: {chat_history}"
            },
            {
                "role": "user",
                "content": f"Context from your memory: None"
            },
            {
                "role": "user",
                "content": f"User Request: {incoming_message.content}"
            },
            {
                "role": "assistant",
                "content": ""
            },
        ]

        return completion_prompt
