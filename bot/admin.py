import os

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from db import product_admin1, product2, delete_admin, uindexall, addproduct_admin
from info import TOKEN, ADMIN
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()
bot = Bot(token=TOKEN)
router.message.filter(F.from_user.id == ADMIN)


@router.message(CommandStart())
async def start(message: Message):
    inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить товар", callback_data="addproduct")
            ],
            [
                InlineKeyboardButton(text="Удалить товар", callback_data="clearproduct")
            ]
        ]
    )
    a = await message.answer(
        text="Привет, админ! Как я могу тебе помочь?",
        reply_markup=inline
    )
    await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 1)


@router.callback_query(F.data == "backer")
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    try:
        await state.clear()
    except:
        pass
    inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить товар", callback_data="addproduct")
            ],
            [
                InlineKeyboardButton(text="Удалить товар", callback_data="clearproduct")
            ]
        ]
    )
    try:
        await callback.message.answer(
            text="Привет, админ! Как я могу тебе помочь?",
            reply_markup=inline
        )
    except:
        a = await callback.message.answer(
            text="Привет, админ! Как я могу тебе помочь?",
            reply_markup=inline
        )
        await bot.delete_message(chat_id=callback.from_user.id, message_id=a.message_id - 1)



class AddPr(StatesGroup):
    name = State()
    desc = State()
    photo = State()


@router.callback_query(F.data == "addproduct")
async def addproduct(callback: CallbackQuery, state: FSMContext):
    inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отменить❌", callback_data="backer")]])
    await callback.message.edit_text(
        text="Отправьте фотографию розыгрыша",
        reply_markup=inline
    )
    await state.set_state(AddPr.photo)


@router.message(AddPr.photo)
async def AddPr_photo(message: Message, state: FSMContext):
    inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отменить❌", callback_data="backer")]])
    if message.photo is not None:
        await state.update_data(photo=message.photo[-1].file_id)
        a = await message.answer(
            text="Введите название товара:\n\n<blockquote>Если вам необходимо форматирование текста используйте HTML:</blockquote>",
            reply_markup=inline,
            parse_mode="HTML"
        )
        await message.answer(
            text="HTML:\n\n"
                 "Цитата - <blockquote>...</blockquote>\n"
                 "Зачеркнутый - <s>...</s>\n"
                 "Подчеркнутый - <u>...</u>\n"
                 "Курсив - <i>...</i>\n"
                 "Моноширинный - <code>...</code>\n"
                 "Скрытый - <tg-spoiler>....</tg-spoiler>\n"
                 "Жирный - <b>...</b>\n"
                 "Ссылка - <a href=''>...</a>\n\n"
                 "Вы можете использовать тег в теге, то есть <blockquote><code>...</code></blockquote>"
        )

        await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 1)
        await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 2)
        await state.set_state(AddPr.name)
    else:
        a = await message.answer(
            text="Отправьте фотографию розыгрыша",
            reply_markup=inline
        )
        await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 1)
        await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 2)
        await state.set_state(AddPr.photo)


@router.message(AddPr.name)
async def addpr_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отменить❌", callback_data="backer")]])
    a = await message.answer(
        text="Введите описание товара\n\n<blockquote>Если вам необходимо форматирование текста используйте HTML:</blockquote>",
        parse_mode="HTML",
        reply_markup=inline
    )
    await message.answer(
        text="HTML:\n\n"
             "Цитата - <blockquote>...</blockquote>\n"
             "Зачеркнутый - <s>...</s>\n"
             "Подчеркнутый - <u>...</u>\n"
             "Курсив - <i>...</i>\n"
             "Моноширинный - <code>...</code>\n"
             "Скрытый - <tg-spoiler>....</tg-spoiler>\n"
             "Жирный - <b>...</b>\n"
             "Ссылка - <a href=''>...</a>\n\n"
             "Вы можете использовать тег в теге, то есть <blockquote><code>...</code></blockquote>"
    )
    await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 3)
    await state.set_state(AddPr.desc)


@router.message(AddPr.desc)
async def AddPr_desc(message: Message, state: FSMContext):
    desc = message.text
    await state.update_data(desc=desc)

    user_data = await state.get_data()
    photo = user_data["photo"]
    name = user_data["name"]
    desc = user_data["desc"]

    text = f"<b>{name}</b>\n\n{desc}"

    inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить✅", callback_data="confirmadd")
            ],
            [
                InlineKeyboardButton(text="Отменить❌", callback_data="backer")
            ]
        ]
    )
    a = await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=inline,
        parse_mode="HTML"
    )
    await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 2)
    await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id - 3)


@router.callback_query(F.data == "confirmadd")
async def confirmadd(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    photo = user_data["photo"]
    name = user_data["name"]
    desc = user_data["desc"]

    uindex_lst = uindexall()
    uin = int.from_bytes(bytes=os.urandom(4), byteorder="big")
    while True:
        if uin not in uindex_lst:
            break
        uin = int.from_bytes(bytes=os.urandom(4), byteorder="big")

    addproduct_admin(uin, photo, name, desc)

    text = f"<b>{name}</b>\n\n{desc}\n\nТовар добавлен✅"

    inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️Вернуться в главное меню", callback_data="backer")
            ]
        ]
    )
    a = await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=inline,
        parse_mode="HTML"
    )
    await bot.delete_message(chat_id=callback.from_user.id, message_id=a.message_id - 1)
    await state.clear()


@router.callback_query(F.data == "clearproduct")
async def clearproductcmd(callback: CallbackQuery):
    if len(product2()) != 0:
        inline = InlineKeyboardMarkup(
            inline_keyboard=product_admin1()
        )
        await callback.message.edit_text(
            text="Выберете товар👇",
            reply_markup=inline
        )
    else:
        inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️Вернуться в главное меню", callback_data="backer")]])
        await callback.message.edit_text(
            text="К сожалению, сейчас нет товаров(",
            reply_markup=inline
        )


@router.callback_query(F.data.split("_")[0] == "clear")
async def clearcmdrr(callback: CallbackQuery):
    await callback.message.delete()
    uindex = int(callback.data.split("_")[1])
    print(uindex)
    inld = product2()
    # inld = [1,2,3,4,5,6,7,8,9,0]
    if uindex == 0:
        if uindex == len(inld) - 1:
            inline = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=f"{str(uindex + 1)}/{len(inld)}", callback_data="fdfvfv"),
                    ]
                ]
            )
        else:
            inline = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="     ", callback_data="fdfvfv"),
                        InlineKeyboardButton(text=f"{str(uindex + 1)}/{len(inld)}", callback_data="fdfvfv"),
                        InlineKeyboardButton(text="Вперед➡️", callback_data=f"clear_{str(uindex+1)}")
                    ]
                ]
            )
    elif 1 <= uindex <= len(inld) - 2:
        inline = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="⬅️Назад", callback_data=f"clear_{str(uindex-1)}"),
                    InlineKeyboardButton(text=f"{str(uindex+1)}/{len(inld)}", callback_data="fdfvfv"),
                    InlineKeyboardButton(text="Вперед➡️", callback_data=f"clear_{str(uindex + 1)}")
                ]
            ]
        )

    elif uindex == len(inld) - 1:
        inline = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="⬅️Назад", callback_data=f"clear_{str(uindex-1)}"),
                    InlineKeyboardButton(text=f"{str(uindex + 1)}/{len(inld)}", callback_data="fdfvfv"),
                    InlineKeyboardButton(text="     ", callback_data="fdfvfv")
                ]
            ]
        )
    inline.inline_keyboard.append(
        [
            InlineKeyboardButton(text="Вернуться в главное меню", callback_data="backer")
        ]
    )
    inline.inline_keyboard.append(
        [
            InlineKeyboardButton(text="Удалить товар", callback_data=f"delete_{str(uindex)}")
        ]
    )
    await callback.message.answer_photo(
        photo=inld[uindex][1],
        caption=f"<b>{inld[uindex][2]}</b>\n\n{inld[uindex][3]}\n\nАртикул: {inld[uindex][0]}",
        reply_markup=inline,
        parse_mode="HTML"
    )
    # await callback.message.edit_text(
    #     text=f"Привет",
    #     reply_markup=inline
    # )


@router.callback_query(F.data.startswith("delete_"))
async def deletecmd(callback: CallbackQuery):
    num = int(callback.data.split("_")[1])
    uindex = product2()[num][0]
    inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️Вернуться в главное меню", callback_data="backer")]])
    delete_admin(uindex)
    await callback.message.delete()
    await callback.message.answer(
        text="Товар удален из базы",
        reply_markup=inline
    )
