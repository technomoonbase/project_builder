from collections import deque
from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path
import subprocess
from uuid import uuid4

import yaml
from managers.chat.messages import Message, MessageCache


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
    tasks: list()
    whoami_path: str
    whoami: dict()
    conversation_path: str

    def __init__(self, config: AgentConfig):
        # Load config attributes
        self.config: dict = config
        # Agent identity context - for prompt inclusion when the bot has an identity crisis... jk
        self.whoami_path: str = Path(f'{config.agent_name}/whoami.yml')
        # Conversation history
        self.conversation_path = Path(f'{config.agent_name}/conversation_history.yml')
        self.message_cache = MessageCache(capacity=50)
    
    def load_identity(self):
        if not self.whoami_path.exists():
            self.whoami = {
                'agent_name': self.config.agent_name,
                'description': self.config.description
            }
            with open(self.whoami_path, 'w') as f:
                yaml.dump(self.whoami, f)

    def chat_with_agent(self, project: str or None):
        chat_banner = subprocess.run(['toilet', '--filter', 'border:metal', 'DISCO Chat'], stdout=subprocess.PIPE)
        print(chat_banner.stdout.decode('utf-8'))
        response_num = 1
        conversation = conversation

        while True:
            # Get the user's request
            request = input("user@chat> ")
            # Convert to Message class
            new_request_message = Message(
                uuid=str(uuid4()),
                role='user',
                speaker_name='user',
                timestamp=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
                project='all' if project is None else project,
                content=request
            )
            #print("Incoming Message:\n")
            #print(asdict(new_request_message))
            print("\n=====  INCOMING MESSAGE PASS  =====\n")

            # Get the recent history from the message cache
            chat_history = self.message_cache.get_message_cache()
            for message in chat_history:
                print(message.to_conversation_dict())
            print(chat_history)

            # Build the prompt
            prompt = self.build_prompt(new_request_message, chat_history)
            print("Prompt:\n")
            #print(prompt)

            # Get the response
            response = Message(
                uuid=str(uuid4()),
                role='assistant',
                speaker_name='Disco',
                timestamp=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
                project='all' if project is None else project,
                content=f'This is response number {response_num}. Thank you for your request.'
            )
            response_num += 1
            # Add turn to chat history
            

    
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
