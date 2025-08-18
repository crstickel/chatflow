
from fastapi import APIRouter, Depends
from typing import Any, Annotated

router = APIRouter(prefix='/conversations', tags=['conversations'])

from app.dependencies import AppDependencyCollection, engine, CurrentUserDependency
from app.dto.conversation import PublicConversationDTO, NewConversationRequestDTO
from app.services.conversation import ConversationService


@router.get('/')
async def list_conversations(
    app_engine: Annotated[AppDependencyCollection, Depends(engine)],
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
    app_engine: Annotated[AppDependencyCollection, Depends(engine)],
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


