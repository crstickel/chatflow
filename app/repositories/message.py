
from abc import ABC, abstractmethod
from datetime import datetime
from sqlmodel import select, func, Session
from typing import Optional, List

from app.models.message import Message
from shared.time import get_current_time


class MessageRepository(ABC):

    @abstractmethod
    def create_message(
        self,
        conversation_id: str,
        sender_id: str,
        content: str,
        created_at: Optional[datetime] = None
    ) -> Message:
        '''
        Creates and adds a new message to the specified conversation
        '''
        raise NotImplementedError()


    @abstractmethod
    def get_messages_for_conversation(self, id: str) -> List[Message]:
        '''
        Retrieves all messages for the specified
        '''
        raise NotImplementedError()


class InMemoryMessageRepository(MessageRepository):
    # TODO: Skipped for the sake of time but should definitely be here for testing
    pass


class DbMessageRepository(MessageRepository):

    def __init__(self, session: Session):
        self.session = session


    def create_message(
        self,
        conversation_id: str,
        sender_id: str,
        content: str,
        created_at: Optional[datetime] = None
    ) -> Message:
        '''
        Creates and adds a new message to the specified conversation
        '''

        if created_at is None:
            created_at = get_current_time()

        message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content,
            created_at=created_at
        )
        self.session.add(message)
        self.session.commit()
        return message



    def get_messages_for_conversation(self, id: str) -> List[Message]:
        '''
        Retrieves all messages for the specified
        '''

        query = select(Message).where(Message.conversation_id == id)
        results = self.session.execute(query)
        return [x[0] for x in results.all()]

