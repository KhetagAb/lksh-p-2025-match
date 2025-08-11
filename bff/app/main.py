from fastapi import FastAPI
from app.bot import router as bot_router
from app.database import engine, Base

# Create all tables on startup
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()
app.include_router(bot_router)

@app.on_event("startup")
async def on_startup():
    await create_tables()
