
import argparse
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
import uvicorn

from app.config import settings
from app.routes import auth, conversations, users
from app.dependencies import get_engine, AppDependencyCollection, db_engine

from shared.password import hash_password

@asynccontextmanager
async def lifespan(app: FastAPI):

    # @@@ DEBUG ONLY - seed repositories with test data

    # Finally, we can yield execution and start running the app
    yield

    # TODO: any app cleanup here

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(conversations.router)
app.include_router(users.router)

@app.get('/')
async def root() -> str:
    return 'ChatFlow'


if __name__ == '__main__':

    # Create main parser and subparsers for commands
    parser = argparse.ArgumentParser(description='Simple Chat Service')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    subparsers.required = True

    # Add commands
    subparsers.add_parser('run', help='Run the application')
    subparsers.add_parser('dbsetup', help='Setup the database')
    subparsers.add_parser('seed', help='Seed the database')

    # Parse arguments
    args = parser.parse_args()

    # Execute the appropriate command
    if args.command == 'run':
        uvicorn.run('main:app', host='0.0.0.0', port=settings.SERVER_PORT, reload=True)

    elif args.command == 'dbsetup':
        from app.models.user import User
        SQLModel.metadata.create_all(db_engine)

    elif args.command == 'seed':
        engine = next(get_engine())
        engine.user_repository.create_user(
            username='test',
            email='test@example.com',
            pwhash=hash_password('password')
        )
        engine.user_repository.create_user(
            username='alice',
            email='alice@example.com',
            pwhash=hash_password('password')
        )
        engine.user_repository.create_user(
            username='bob',
            email='bob@example.com',
            pwhash=hash_password('password')
        )

    else:
        parser.print_help()


