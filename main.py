import os
import random
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher, types, F
from contextlib import asynccontextmanager

# --- CONFIGURATION ---
TOKEN = os.getenv("8434194192:AAHN9cfpMobIStNfQ0q02kPgt1MDByVsS6s")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- FASTAPI SETUP ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start bot polling when FastAPI starts
    asyncio.create_task(dp.start_polling(bot))
    yield
    # Cleanup on shutdown
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- BINGO API ---
@app.get("/generate_card")
async def generate_card():
    # 25 random numbers for a 5x5 grid
    numbers = random.sample(range(1, 76), 25)
    return {"card": numbers}

# --- BOT LOGIC ---
@dp.message(F.web_app_data)
async def handle_bingo_win(message: types.Message):
    import json
    data = json.loads(message.web_app_data.data)
    if data.get("event") == "bingo_win":
        nums = ", ".join(data.get("numbers"))
        await message.answer(f"🎉 BINGO! {message.from_user.first_name} claimed victory with: {nums}")

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("Tap the button below to play Bingo!")