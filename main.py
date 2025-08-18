
from fastapi import FastAPI

from app.dependencies import engine, AppDependencyCollection

app = FastAPI()

@app.get('/')
async def root() -> str:
    return 'ChatFlow'


# @@@ DEBUG ONLY - seed repositories with test data
engine.user_repository.create_user(
    username='test',
    email='test@example.com',
    pwhash='dummydatafornow'
)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)

