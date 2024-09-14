from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from info import TOKEN, ADMIN
from text import hello

router = Router()
bot = Bot(token=TOKEN)
router.message.filter(F.from_user.id != ADMIN)


@router.message(Command("start"))
async def start(message: Message):
    inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Товары в наличии", web_app=WebAppInfo(""))
            ]
        ]
    )
    a = await message.answer(
        text=f"{hello(message.from_user.first_name)}",
        reply_markup=inline
    )
    await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 1)
