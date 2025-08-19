
from abc import ABC, abstractmethod
from datetime import datetime
from sqlmodel import Session
from typing import Optional, List

from app.models.conversation import Conversation
from shared.time import get_current_time

class ConversationRepository(ABC):

    @abstractmethod
    def create_conversation(
        self,
        name: str,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ) -> Conversation:
        '''
        Creates and adds a new Conversation instance to the repository
        '''
        raise NotImplementedError()


    @abstractmethod
    def get_conversation_by_id(self, id: str) -> Optional[Conversation]:
        '''
        Retrieves a Conversation record based on the specified ID
        '''
        raise NotImplementedError()



    @abstractmethod
    def delete_conversation(self, id: str) -> None:
        '''
        Removes a conversation
        '''
        raise NotImplementedError()



class InMemoryConversationRepository(ConversationRepository):

    def __init__(self):
        self.conversations_by_id = {}


    def create_conversation(
        self,
        name: str,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ) -> Conversation:
        '''
        Creates and adds a new Conversation instance to the repository
        '''

        if id is None:
            id = Conversation.generate_id()
        if created_at is None:
            created_at = get_current_time()

        conversation = Conversation(
            id=id,
            name=name,
            created_at=created_at
        )

        self.conversations_by_id[id] = conversation
        return conversation


    def get_conversation_by_id(self, id: str) -> Optional[Conversation]:
        '''
        Retrives a conversation record based on the specified ID
        '''
        return self.conversations_by_id.get(id, None)


    def delete_conversation(self, id: str) -> None:
        '''
        Removes a conversation
        Raises KeyError if the conversation does not exist in the repository
        '''
        del self.conversations_by_id[id]



class DbConversationRepository(ConversationRepository):

    def __init__(self, session: Session):
        self.session = session

    def create_conversation(
        self,
        name: str,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ) -> Conversation:
        '''
        Creates and adds a new Conversation instance to the repository
        '''
        if id is None:
            id = Conversation.generate_id()
        if created_at is None:
            created_at = get_current_time()

        conversation = Conversation(
            id=id,
            name=name,
            created_at=created_at,
        )
        self.session.add(conversation)
        self.session.commit()
        return conversation


    def get_conversation_by_id(self, id: str) -> Optional[Conversation]:
        '''
        Retrives a conversation record based on the specified ID
        '''
        return self.session.get(Conversation, id)


    def delete_conversation(self, id: str) -> None:
        '''
        Removes a conversation
        Raises KeyError if the conversation does not exist in the repository
        '''
        conversation = self.get_conversation_by_id(id)
        self.session.delete(conversation)
        self.session.commit()

