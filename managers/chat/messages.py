from collections import deque
from dataclasses import asdict, dataclass, field
from typing import List, Optional, Dict

import yaml


@dataclass
class Message:
    """
    The Message dataclass standardizes the format for all messages to be included in the message cache for context.
    """
    uuid: str
    role: str
    speaker_name: str
    timestamp: str
    project: str  # this is the project name
    content: str
    metadata: Optional[Dict] = None

    def message_to_yaml(self, file_path: Optional[str] = None) -> str:
        """
        Converts a Message dataclass instance to YAML.

        :param message: The Message instance to convert.
        :param file_path: Optional path to a file to save the YAML.
        :return: YAML string representation
        """
        # Convert the Message dataclass instance to a dictionary
        message_dict = asdict(self)
        
        # Convert the dictionary to a YAML string
        yaml_str = yaml.safe_dump(message_dict)

        # If a file_path is provided, write to the file, otherwise return the YAML string
        if file_path:
            with open(file_path, 'w') as file:
                file.write(yaml_str)
        else:
            return yaml_str

    def to_dict(self):
        """
        Exports the Message container to an iterable

        :param self: The message instance to convert
        :return: dict representation
        """

        base_dict = {
            "uuid": self.uuid,
            "role": self.role,
            "speaker_name": self.speaker_name,
            "timestamp": self.timestamp,
            "project": self.project,
            "content": self.content,
        }

        if self.metadata:
            base_dict["metadata"] = self.metadata

        return base_dict

    def to_conversation_dict(self):
        """
        Exports Message to a conversation dictionary to standardize format before appending to history.

        :param self: Message instance to convert
        :return: dict representation
        """

        return {
            "role": self.role,
            "content": f'Speaker: {self.speaker_name} || Project: {self.project} || Timestamp: {self.timestamp} || Content: {self.content}'
        }

    def to_knowledge_dict(self):
        """
        Exports Message to a dictionary formatted to hold source and content for knowledge base documents
        """

        return {
            "role": "user",
            "content": f'Project: {self.project} || Published Date: {self.timestamp} || Speaker: {self.speaker_name} || Content: {self.content}'
        }


class MessageCache:
    """
    This class manages the conversation history for inclusion in prompt context injection as a deque with structural
    preservation on i/o
    """

    def __init__(self, capacity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capacity = capacity
        self.cache = deque(maxlen=capacity)

    def add_message(self, message: Message):
        self.cache.append(message)

    def get_message_cache(self):
        message_cache = list(self.cache)
        return message_cache
    
    def get_n_messages(self, n):
        message_cache = list(self.cache)[-n:]
        return message_cache


@dataclass
class MessageTurn:
    conversation: str
    uuid: str
    request: Message
    response: Message

    def to_dict(self):
        """
        Converts the Turn dataclass instance to a dictionary.
        """
        return {
            "uuid": self.uuid,
            "created_at": self.created_at,
            "request": asdict(self.request),
            "response": asdict(self.response),
        }


@dataclass
class Conversation:
    uuid: str
    created_at: str
    last_active: str
    turns: List[MessageTurn] = field(default_factory=list)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "created_at": self.created_at,
            "last_active": self.last_active,
            "turns": [turn.to_dict() for turn in self.turns],
        }


def append_turn_to_conversation(conversation: Conversation, turn: MessageTurn):
    """
    Appends a new turn to the conversation.

    :param conversation: The Conversation object to append the turn to.
    :param turn: The MessageTurn object representing the new turn.
    """
    conversation.turns.append(turn)
    conversation.last_active = turn.response.timestamp  # Update last_active to the timestamp of the latest response