
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import settings
from app.routes import auth, user
from app.dependencies import engine, AppDependencyCollection

from shared.password import hash_password

@asynccontextmanager
async def lifespan(app: FastAPI):

    # @@@ DEBUG ONLY - seed repositories with test data
    engine.user_repository.create_user(
        username='test',
        email='test@example.com',
        pwhash=hash_password('password')
    )

    # Finally, we can yield execution and start running the app
    yield

    # TODO: any app cleanup here

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(user.router)

@app.get('/')
async def root() -> str:
    return 'ChatFlow'




if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=settings.SERVER_PORT, reload=True)

