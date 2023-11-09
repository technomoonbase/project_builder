from dataclasses import asdict
from datetime import datetime
import json
from uuid import uuid4
from managers.agents.agent_manager import AgentConfig, discoChatDefaultconfig, Agent
from managers.agents import default_messages
from managers.chat.messages import Message, MessageTurn, Conversation, append_turn_to_conversation
from ai3j.ai_initial_review import ai_assist_bounty_listing_to_yaml
from pathlib import Path


def managers_agents_agent_manager_AgentConfig():
    discoconfig = AgentConfig(
        name='disco',
        description=default_messages.description1, 
        system_message=default_messages.system_message1, 
        user_context=default_messages.user_context1, 
        user_response_prefs=default_messages.user_response_prefs1
    )
    print("Agent Config:\n")
    print(asdict(discoconfig))
    print("\n=====  PASS  =====\n")

def managers_agents_agent_manager_discoChatDefaultConfig():
    discoconfig = discoChatDefaultconfig()
    print("Agent Config:\n")
    print(asdict(discoconfig))
    print("\n=====  PASS  =====\n")

def managers_agents_agent_manager_Agent(config):
    disco = Agent(config)
    disco_attrs = vars(disco)
    print("Disco Class Attrs:\n")
    print(disco_attrs)
    print("\n=====  PASS  =====\n")

def managers_agents_agent_manager_build_prompt():
    config = discoChatDefaultconfig()
    agent = Agent(config)
    request = "What is the meaning of life?"

    # process incoming message
    incoming_message = Message(
        uuid=str(uuid4()),
        role='user',
        speaker_name='techno',
        timestamp=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
        project='all',
        content=request
    )
    print("Incoming Message:\n")
    print(asdict(incoming_message))
    print("\n=====  INCOMING MESSAGE PASS  =====\n")

    # Get recent history from message cache
    chat_history = agent.message_cache.get_n_messages(25)
    chat_history_json = [json.dumps(turn.to_dict()) for turn in chat_history]
    print("Chat History:\n")
    print(chat_history_json)
    print("\n=====  CHAT HISTORY PASS  =====\n")

    # Get response
    response = Message(
        uuid=str(uuid4()),
        role='assistant',
        speaker_name='Disco',
        timestamp=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
        project='all',
        content="42"
    )
    print("Response Message:\n")
    print(asdict(response))
    print("\n=====  RESPONSE MESSAGE PASS  =====\n")

    # Create MessageTurn
    request = incoming_message

    message_turn = MessageTurn(
        conversation='testing',
        uuid=str(uuid4()),
        request=incoming_message,
        response=response
    )
    print("Message Turn:\n")
    print(asdict(message_turn))
    print("\n=====  MESSAGE TURN PASS  =====\n")

# Add Turn to Conversation
def managers_chat_messages_append_turn_to_conversation():
    conversation = Conversation(
        uuid=str(uuid4()),
        created_at=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
        last_active=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
        turns=[]
    )

    # Create MessageTurn
    request = Message(
        uuid=str(uuid4()),
        role='user',
        speaker_name='techno',
        timestamp=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
        project='all',
        content="What is the meaning of life?"
    )

    response = Message(
        uuid=str(uuid4()),
        role='assistant',
        speaker_name='Disco',
        timestamp=str(datetime.now().strftime('%Y-%m-%d @ %H:%M')),
        project='all',
        content="42"
    )

    message_turn = MessageTurn(
        conversation='testing',
        uuid=str(uuid4()),
        request=request,
        response=response
    )
    print("Message Turn:\n")
    print(asdict(message_turn))
    print("\n=====  MESSAGE TURN PASS  =====\n")

    # Add Turn to Conversation
    append_turn_to_conversation(conversation, message_turn)
    print("Conversation:\n")
    print(asdict(conversation))
    print("\n=====  CONVERSATION PASS  =====\n")


def managers_agents_agent_manager_chat_with_agent():
    config = discoChatDefaultconfig()
    agent = Agent(config)
    agent.chat_with_agent(project=None)


def ai_ai_initial_review_ai_assist_bounty_listing_to_yaml():
    print("AI Initial Review Result:\n")
    result = ai_assist_bounty_listing_to_yaml('kiteworks')
    print(result)
    print("\n=====  AI INITIAL REVIEW PASS  =====\n")


if __name__ == '__main__':
    #config = managers_agents_agent_manager_discoChatDefaultConfig()
    #managers_agents_agent_manager_AgentConfig()
    #managers_agents_agent_manager_Agent(config)
    #managers_agents_agent_manager_chat_with_agent()
    #managers_agents_agent_manager_build_prompt()
    #managers_chat_messages_append_turn_to_conversation()
    #ai_ai_initial_review_ai_assist_bounty_listing_to_yaml()
    import torch
    x = torch.rand(5, 3)
    print(x)
    print(torch.version.cuda)
    print(torch.cuda.is_available())