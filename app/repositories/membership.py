
from abc import ABC, abstractmethod
from collections import defaultdict
from sqlmodel import Session, select
from typing import Optional, List

from app.models.membership import Membership

class MembershipRepository(ABC):

    @abstractmethod
    def create_membership(self, conversation_id: str, user_id: str) -> Membership:
        '''
        Creates and adds a new conversation 'Membership' instance to the repository
        '''
        raise NotImplementedError()


    @abstractmethod
    def get_conversations_for_user(self, user_id: str) -> List[str]:
        '''
        Returns a list of conversations the user is a member of
        '''
        raise NotImplementedError()


    @abstractmethod
    def delete_membership(self, conversation_id: str, user_id: str) -> None:
        '''
        Removes a user's membership from the specified conversation
        '''
        raise NotImplementedError()


class InMemoryMembershipRepository(MembershipRepository):

    def __init__(self):
        self.conversations_by_user = defaultdict(list)
        self.users_by_conversation = defaultdict(list)


    def create_membership(self, conversation_id: str, user_id: str) -> Membership:
        '''
        Creates and adds a new Conversation instance to the repository
        '''
        conversations = self.conversations_by_user.get(user_id, [])
        if conversation_id in conversations:
            raise ValueError(f'Already in conversation')

        conversations.append(conversation_id)
        self.conversations_by_user[user_id] = conversations
        self.users_by_conversation[conversation_id].append(user_id)
        return Membership(user_id=user_id, conversation_id=conversation_id)


    def get_conversations_for_user(self, user_id: str) -> List[str]:
        '''
        Returns a list of conversations the user is a member of
        '''
        return self.conversations_by_user.get(user_id, [])


    def get_users_for_conversation(self, conversation_id: str) -> List[str]:
        '''
        Returns a list of user IDs for the specified conversation
        '''
        return self.users_by_conversation.get(conversation_id, [])


    def delete_membership(self, conversation_id: str, user_id: str) -> None:
        '''
        Removes a user's membership from the specified conversation
        Raises KeyError if the specified membership doesn't exist
        '''

        conversations = self.conversations_by_user.get(user_id, None)
        if conversations is None:
            raise KeyError('User not a member of this conversation')

        try:
            conversations.remove(conversation_id)
            self.users_by_conversation[conversation_id].remove(user_id)
        except ValueError:
            raise KeyError('User not a member of this conversation')


class DbMembershipRepository(MembershipRepository):

    def __init__(self, session: Session):
        self.session = session


    def create_membership(self, conversation_id: str, user_id: str) -> Membership:
        '''
        Creates and adds a new Conversation instance to the repository
        '''
        membership = Membership(user_id=user_id, conversation_id=conversation_id)
        self.session.add(membership)
        self.session.commit()
        return membership


    def get_conversations_for_user(self, user_id: str) -> List[str]:
        '''
        Returns a list of conversations the user is a member of
        '''
        query = select(Membership.conversation_id).where(Membership.user_id == user_id)
        results = self.session.execute(query)
        return [x[0] for x in results.all()]


    def get_users_for_conversation(self, conversation_id: str) -> List[str]:
        '''
        Returns a list of user IDs for the specified conversation
        '''
        query = select(Membership.user_id).where(Membership.conversation_id == conversation_id)
        results = self.session.execute(query)
        return [x[0] for x in results.all()]


    def delete_membership(self, conversation_id: str, user_id: str) -> None:
        '''
        Removes a user's membership from the specified conversation
        Raises KeyError if the specified membership doesn't exist
        '''

        query = select(Membership) \
            .where(Membership.conversation_id == conversation_id)   \
            .where(Membership.user_id == user_id)

        membership = self.session.execute(query).first()
        if membership is None:
            raise KeyError('Membership does not exist and cannot be deleted')

        self.session.delete(membership)
        self.session.commit()

