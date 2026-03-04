from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import asyncio
from aiogram.types import FSInputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ContentType
import os

BOT_TOKEN = "8434194192:AAHN9cfpMobIStNfQ0q02kPgt1MDByVsS6s"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("play"))
async def play_handler(message: types.Message):
    # Create inline keyboard with web_app button
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎮 Play Bingo",
                web_app=WebAppInfo(url="https://bing-lemon-seven.vercel.app/")
            )
        ]
    ])

    await message.answer(
        "🎱 Tap the button below to open Bingo instantly!",
        reply_markup=keyboard
    )
   
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Create inline keyboard with 4 buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎮 Play",
                web_app=WebAppInfo(url="https://bing-lemon-seven.vercel.app/")
            ),
            InlineKeyboardButton(
                text="💰 Deposit",
                web_app=WebAppInfo(url="https://front-blond-kappa.vercel.app")
            )
        ],
        [
            InlineKeyboardButton(
                text="📖 Instructions",
                url="https://bing-lemon-seven.vercel.app/instructions"
            ),
            InlineKeyboardButton(
                text="🛠 Support",
                url="https://t.me/YourSupportUsername"
            )
        ]
    ])

    # Load local image from your project folder
    image_path = os.path.join(os.getcwd(), "images", "welcome.png")
    photo = FSInputFile(image_path)

    # Send the photo with caption and inline keyboard
    await message.answer_photo(
        photo=photo,
        caption="🎱 Welcome to Bingo Master!\n\nTap the buttons below to get started:",
        reply_markup=keyboard
    )

# deposite fuction

# ---- Deposit command ----
@dp.message(Command("deposit"))
async def deposit_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💳 Telebirr", callback_data="deposit_telebirr"),
            InlineKeyboardButton(text="🏦 CBE", callback_data="deposit_cbe")
        ]
    ])
    await message.answer(
        "💰 እባክዎን የሚፈልጉትን የተክል አገልግሎት ይምረጡ።",
        reply_markup=keyboard
    )

# ---- Handle Telebirr and CBE buttons ----
@dp.callback_query(lambda c: c.data and c.data.startswith("deposit_"))
async def process_deposit_option(callback_query: types.CallbackQuery):
    option = callback_query.data  # deposit_telebirr or deposit_cbe

    if option == "deposit_telebirr":
        text = (
            "🎯 የ Telebirr አካውንት\n"
            "```\n0921178262\n```\n\n"
            "መመሪያ:\n"
            "1. ከላይ ባለው የ Telebirr አካውንት ገንዘቡን ያስገቡ\n"
            "2. ብሩን ስትልኩ የከፈላችሁበትን መረጃ የያዝ አጭር የጹሁፍ መልክት(sms) ከ Telebirr ይደርሳችላል\n"
            "3. የደረሳችሁን አጭር የጹሁፍ መለክት(sms) ሙሉውን ኮፒ(copy) በማረግ በ Telegram ያስገቡ\n\n"
            "⚠️ የክፍያ ችግር ካለ @MasterBingoSupport እባኮትን ያግኙ"
        )
    else:  # deposit_cbe
        text = (
            "🎯 የ CBE አካውንት\n"
            "```\n1234567890\n```\n\n"
            "መመሪያ:\n"
            "1. ከላይ ባለው የ CBE አካውንት ገንዘቡን ያስገቡ\n"
            "2. ከፈለጉት መረጃ አጭር SMS ከ CBE ይደርሳችሁ\n"
            "3. እባክዎን ኮፒ አድርጉ እና Telegram ላይ ያስገቡ\n\n"
            "⚠️ ችግር ካለ @MasterBingoSupport እባኮትን ያግኙ"
        )

    await callback_query.message.answer(text, parse_mode="Markdown")
    await callback_query.answer()  # closes loading animation on button
# ---- Balance command ----
@dp.message(Command("balance"))
async def balance_handler(message: types.Message):
    # Example user data — replace with your DB query
    user_name = "NEB"
    phone_number = "251948250798"
    withdrawable_balance = 0.0
    non_withdrawable_balance = 0.0
    total_balance = withdrawable_balance + non_withdrawable_balance

    balance_text = (
        "💰 Your Current Account Balance!\n\n"
        "```\n"
        f"Name:                    {user_name}\n"
        f"Phone Number:            {phone_number}\n"
        f"Withdrawable Balance:    {withdrawable_balance}\n"
        f"Non-Withdrawable Balance:{non_withdrawable_balance}\n"
        f"Total Balance:           {total_balance}\n"
        "```"
    )

    await message.answer(balance_text, parse_mode="Markdown")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
