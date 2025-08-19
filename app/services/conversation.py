
from typing import Optional, List

from app.dependencies import AppDependencyCollection
from app.models.conversation import Conversation
from app.models.membership import Membership
from app.models.user import User


class ConversationService:

    def __init__(self, engine: AppDependencyCollection):
        self.engine = engine


    def start_new_conversation(self, name: str, users: List[str]) -> Optional[Conversation]:
        '''
        Creates a new conversation and adds the specified users to it
        '''

        # Gather and validate our user accounts
        user_ids = []
        for username in users:
            user = self.engine.user_repository.get_user_by_username(username)
            if not user:
                raise ValueError(f"No user with name '{username}'")
            user_ids.append(user.id)

        # Create the new conversation
        conversation = self.engine.conversation_repository.create_conversation(name)

        # Add the specified users as members of this conversation
        for user_id in user_ids:
            self.engine.membership_repository.create_membership(conversation.id, user_id)

        # Finished
        return conversation


    def get_conversation_member_names(self, id: str) -> List[str]:
        user_ids = self.engine.membership_repository.get_users_for_conversation(id)
        return [self.engine.user_repository.get_user_by_id(x).username for x in user_ids]

