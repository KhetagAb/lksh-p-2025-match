from telegram import Bot, Update
from fastapi import APIRouter, Request
from telebot.async_telebot import AsyncTeleBot, Handler
from telebot import types
import asyncio

router = APIRouter()

# real_token = config.settings.telegram_token
token = '8177210409:AAGinnUyakfNtpNsCnafzFEiXGKNaPXA_-U'
bot = AsyncTeleBot(token)


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


def get_list_of_all_sports() -> list[str]:
    return ['Volleyball', 'Basketball', 'Football']


def sign_up_to_sport(sport: str) -> str:
    pass


def registration_person(username: str) -> None:
    pass


def get_list_of_people_on_sport(sport: str) -> list[str]:
    pass


def make_sports_buttons(pref: str):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for sport in get_list_of_all_sports():
        buttons.append(types.KeyboardButton(pref + sport))
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['start'])
async def start(mess):
    chat_id = mess.chat.id
    user_id = mess.from_user.id
    username = mess.from_user.username
    registration_person(username)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("/signup")
    button2 = types.KeyboardButton("/list")
    markup.add(button1, button2)
    for_pin = (await bot.send_message(mess.chat.id,
                           "Hello. For signing up to sports click /signup, for getting list of all users click /list",
                           reply_markup=markup)).message_id
    await bot.pin_chat_message(chat_id=mess.chat.id, message_id=for_pin)



@bot.message_handler(commands=['signup'])
async def signup(mess):
    await bot.send_message(mess.chat.id, "You can sign up for these sports", reply_markup=make_sports_buttons('reg_'))


@bot.message_handler(commands=['list'])
async def list_(mess):
    await bot.send_message(mess.chat.id, "To view the lists, select sports", reply_markup=make_sports_buttons('list_'))


@bot.message_handler(content_types=['text'])
async def answer_to_buttons(mess):
    for sport in get_list_of_all_sports():
        if 'reg_' + sport == mess.text:
            ans = sign_up_to_sport(sport)
            msg = ''
            if ans:
                msg = f"You are sign up to {sport}."
            else:
                msg = f"Sorry, something went wrong. Please repeat later."
            await bot.send_message(mess.chat.id, msg)
            return
        if 'list_' + sport == mess.text:
            await bot.send_message(mess.chat.id, '\n'.join(get_list_of_people_on_sport(sport)))
    await bot.send_message(mess.chat.id, "I don't understand you.")




if __name__ == "__main__":
    asyncio.run(bot.polling())
