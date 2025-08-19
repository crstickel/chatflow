
from fastapi import APIRouter, Depends
from typing import Any, Annotated

router = APIRouter(prefix='/conversations', tags=['conversations'])

from app.dependencies import get_engine, AppDependencyCollection, CurrentUserDependency
from app.dto.conversation import (
    PublicConversationDTO,
    NewConversationRequestDTO,
    SendMessageDTO,
    ConversationMessageDTO
)
from app.services.conversation import ConversationService


@router.get('/')
async def list_conversations(
    app_engine: Annotated[AppDependencyCollection, Depends(get_engine)],
    current_user: CurrentUserDependency
) -> Any:
    service = ConversationService(app_engine)
    ids = app_engine.membership_repository.get_conversations_for_user(current_user.id)
    conversations = [app_engine.conversation_repository.get_conversation_by_id(x) for x in ids]

    response = {}
    for conversation in conversations:
        response[conversation.id] = {
            'name': conversation.name,
            'participants': service.get_conversation_member_names(conversation.id)
        }

    return response


@router.post('/', response_model=PublicConversationDTO)
async def new_conversation(
    app_engine: Annotated[AppDependencyCollection, Depends(get_engine)],
    current_user: CurrentUserDependency,
    body: NewConversationRequestDTO
) -> Any:
    service = ConversationService(app_engine)
    conversation = service.start_new_conversation(
        name=body.name,
        users=body.participants
    )

    return PublicConversationDTO(
        name=conversation.name,
        participants=service.get_conversation_member_names(conversation.id)
    )



@router.get('/{id}/messages')
async def get_messages_for_conversation(
    app_engine: Annotated[AppDependencyCollection, Depends(get_engine)],
    current_user: CurrentUserDependency,
    id: str,
) -> Any:
    # TODO : this can be sped up and simplified substantially with caching
    participants = app_engine.membership_repository.get_users_for_conversation(id)
    names = [app_engine.user_repository.get_user_by_id(x).username for x in participants]
    participant_names = dict(zip(participants, names))

    messages = ConversationService(app_engine).get_messages_for_conversation(id)
    return [ConversationMessageDTO(**x.model_dump(), sender=participant_names[x.sender_id]) for x in messages]


@router.post('/{id}/messages')
async def send_message_to_conversation(
    app_engine: Annotated[AppDependencyCollection, Depends(get_engine)],
    current_user: CurrentUserDependency,
    id: str,
    body: SendMessageDTO
) -> Any:
    message = ConversationService(app_engine).post_message_to_conversation(
        id=id,
        sender=current_user,
        content=body.content
    )
    return message

