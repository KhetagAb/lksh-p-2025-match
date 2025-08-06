from telegram import Bot, Update
from fastapi import APIRouter, Request
# from app.config import settings
from telebot.async_telebot import AsyncTeleBot, Handler
from telebot import types
import asyncio
import os

router = APIRouter()

real_token = os.getenv("TELEGRAM_TOKEN")
bot = AsyncTeleBot(real_token)


# dispatcher = Dispatcher(bot, update_queue=None, workers=0, use_context=True)

# Register handlers
# TODO
#
# @router.post(f"/webhook/{config.settings.telegram_token}")
# async def webhook(request: Request):
#     data = await request.json()
#     update = Update.de_json(data, bot)
#     dispatcher.process_update(update)
#     return {"ok": True}


def get_all_sport_section() -> list[str]:
    return ['Volleyball', 'Basketball', 'Football']


def sign_up_to_sport(sport: str) -> str:
    pass


def add_accord(tg_id, real_id) -> None:
    with open("accord.txt", 'a') as file:
        file.write(str(tg_id) + ';' + str(real_id) + '\n')


def get_id(tg_id) -> str:
    tg_id = str(tg_id)
    print(tg_id)
    with open("accord.txt", 'r') as file:
        for line in file.readlines():
            print(line)
            if tg_id == line.split(';')[0]:
                return line.split(';')[1]
        return 'nf'


def validate_register_user(tg_id: int, username: str) -> str:
    return "Vasya Pupkin"


def register_user(tg_id: int, username: str) -> int:
    return 228356789


def get_players_by_sport_section(sport: str) -> list[str]:
    return ['Vasya', 'Petya']


def register_player_sport_section(real_id, sport) -> None:
    return


def make_sports_buttons() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for sport in get_all_sport_section():
        buttons.append(types.KeyboardButton(sport))
    markup.add(*buttons)
    return markup


async def fuse_not_nf(mess: types.Message) -> bool:
    if get_id(mess.from_user.id) != 'nf':
        await bot.send_message(mess.chat.id, "You was register in system later.")
        return True
    return False


async def fuse_nf(mess: types.Message) -> bool:
    if get_id(mess.from_user.id) == 'nf':
        await bot.send_message(mess.chat.id, "You weren't registered in the system. To register, enter /start")
        return True
    return False


@bot.message_handler(commands=['start'])
async def start(mess):
    chat_id = mess.chat.id
    user_id = mess.from_user.id
    username = mess.from_user.username
    msg = ''
    if await fuse_not_nf(mess):
        return
    try:
        msg = validate_register_user(int(user_id), username)
    except UserNotFound:
        msg = "Sorry, you are not in lists. Go to 4th kompovnik."
    except BaseException:
        msg = "Sorry, something went wrong. Repeat later, or go to 4th kompovnik."
    if "Sorry, " not in msg:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Yes, register confirm.")
        button2 = types.KeyboardButton("No, register cancel.")
        markup.add(button1, button2)
        await bot.send_message(mess.chat.id,
                               f"{msg},\nwe are find you in base. It is you? If not, got to 4th kompovnik",
                               reply_markup=markup)
    else:
        await bot.send_message(mess.chat.id, msg)


@bot.message_handler(commands=['register_on_sport'])
async def register_on_sport(mess):
    if await fuse_nf(mess):
        return
    markup = make_sports_buttons()
    await bot.send_message(mess.chat.id, "Choose a sport", reply_markup=markup)


@bot.message_handler(content_types=['text'])
async def answer_to_buttons(mess):
    if mess.text == "Yes, register confirm.":
        if await fuse_not_nf(mess):
            return
        response = register_user(mess.from_user.id, mess.from_user.username)
        add_accord(mess.from_user.id, response)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("/register_on_sport")
        markup.add(button)
        to_pin = (await bot.send_message(mess.chat.id,
                                         "You was register in system.\n"
                                         "To register for something sport, click /register_on_sport",
                                         reply_markup=markup)).message_id
        await bot.pin_chat_message(mess.chat.id, to_pin)
        return
    if mess.text == "No, register cancel.":
        if await fuse_not_nf(mess):
            return
        await bot.send_message(mess.chat.id, "OK, register canceled. If you want to register another, enter /start")
        return
    if await fuse_nf(mess):
        return
    for sport in get_all_sport_section():
        if sport == mess.text:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton(f"list_{sport}")
            button2 = types.KeyboardButton(f"signup_{sport}")
            markup.add(button1, button2)
            await bot.send_message(mess.chat.id,
                                   f"You can view list of participants with button list_{sport} or sign up to sport with button signup_{sport}",
                                   reply_markup=markup)
            return
        if f"list_{sport}" == mess.text:
            await bot.send_message(mess.chat.id, '\n'.join(get_players_by_sport_section(sport)))
            return
        if f"signup_{sport}" == mess.text:
            msg = f"Yo're have registered on {sport}"
            try:
                register_player_sport_section(get_id(mess.from_user.id), sport)
            except RegistrationOver:
                msg = f"Sorry, registration on {sport} section is over"
            except AlreadyRegistered:
                msg = f"You already registered on {sport}"
            except BaseException:
                msg = "Sorry, something went wrong. Repeat later, or go to 4th kompovnik."
            await bot.send_message(mess.chat.id, msg)
            return

    await bot.send_message(mess.chat.id, "I don't understand you.")


if __name__ == "__main__":
    asyncio.run(bot.polling())
