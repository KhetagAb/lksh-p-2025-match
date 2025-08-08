import logging

from telegram import Bot, Update
from fastapi import APIRouter, Request, FastAPI
from telebot.async_telebot import AsyncTeleBot, Handler
from telebot import types
from contextlib import asynccontextmanager
import asyncio
import os
import random
from bff.lkshmatch.adapters import rest


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_url = settings.get("WEBHOOK_URL")
    await bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True
    )
    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)


@app.post('/webhook')
async def webhook_start_bot(req: Request) -> None:
    await bot.process_new_updates([types.Update.de_json(await req.json())])

real_token = settings.get('MATCH_TELEGRAM_TOKEN')

if real_token:
    bot = AsyncTeleBot(real_token)
else:
    # TODO: log error and continue work, because we have other frontends
    exit()


def sign_up_to_sport(sport: str) -> str:
    pass


# Не будет использоваться в дальнейшем
def add_accord(tg_id, real_id) -> None:
    with open("accord.txt", 'a') as file:
        file.write(str(tg_id) + ';' + str(real_id) + '\n')


# Не будет использоваться в дальнейшем
def get_id(tg_id) -> str:
    tg_id = str(tg_id)
    print(tg_id)
    with open("accord.txt", 'r') as file:
        for line in file.readlines():
            print(line)
            if tg_id == line.split(';')[0]:
                return line.split(';')[1]
        return 'nf'


async def make_sports_buttons() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for sport in await rest.RestGetSportSections().get_sections():
        buttons.append(types.KeyboardButton(sport.name))
    markup.add(*buttons)
    return markup


async def fuse_not_nf(mess: types.Message) -> bool:
    if get_id(mess.from_user.id) != 'nf':
        await bot.send_message(mess.chat.id, "Вы регистрировались в системе ранее.")
        return True
    return False


async def fuse_nf(mess: types.Message) -> bool:
    if get_id(mess.from_user.id) == 'nf':
        await bot.send_message(mess.chat.id, "Вы не зарегистрированы в системе. Для регистрации введите /start")
        return True
    return False


def get_role(id: int, sport: str) -> str:
    return ['admin', 'user', 'captain'][random.randrange(3)]


# список всех команд по названию спорта
def get_list_of_all_commands(sport: rest.SportSection) -> list[str]:
    return


def set_name_of_team(old_team: str, new_team: str) -> None:
    return


# возвращает название команды, которое присвоила система
def register_new_team(sport: rest.SportSection, tg_id: int) -> str:
    return "Team 228"


def get_standart_message_to_exception() -> str:
    return "Извините, что-то пошло не так. Повторите позже или обратитесь в 4ый комповник."


def make_noregister_markup(mess: types.Message, sport: str) -> types.ReplyKeyboardMarkup:
    role = get_role(int(get_id(mess.from_user.id)), sport)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    data_for_buttons = []
    if role == "user":
        data_for_buttons = ["/create_team", "/teams", "/join_team", "/approve_member_join"]
    elif role == "captain":
        data_for_buttons = ["/teams", "/approve_member_join", "/delete_team"]
    elif role == "admin":
        pass
    buttons = map(types.KeyboardButton, map(lambda x: x + f" {sport}", data_for_buttons))
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['start'])
async def start(mess: types.Message) -> None:
    chat_id = mess.chat.id
    user_id = mess.from_user.id
    username = mess.from_user.username
    msg = ''
    if await fuse_not_nf(mess):
        return
    try:
        msg = await rest.RestValidateRegisterUser().validate_register_user(rest.PlayerAddInfo(username, int(user_id)))
    except rest.PlayerNotFound:
        msg = "Извините, но вас нет в списках. Подойдите в 4ый комповник."
    except BaseException:
        msg = get_standart_message_to_exception()
    if "Извините, " not in msg:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Это я, регистрацию подтверждаю.")
        button2 = types.KeyboardButton("Нет, это не я. Отмена регистрации.")
        markup.add(button1, button2)
        await bot.send_message(mess.chat.id,
                               f"{msg},\nмы нашли Вас в базе. Это вы?",
                               reply_markup=markup)
    else:
        await bot.send_message(mess.chat.id, msg)


@bot.message_handler(commands=['register_on_sport'])
async def register_on_sport(mess: types.Message) -> None:
    if await fuse_nf(mess):
        return
    markup = await make_sports_buttons()
    await bot.send_message(mess.chat.id, "Выберите секцию", reply_markup=markup)


@bot.message_handler(content_types=['text'])
async def answer_to_buttons(mess: types.Message) -> None:
    if mess.text == "Это я, регистрацию подтверждаю.":
        if await fuse_not_nf(mess):
            return
        response = await rest.RestRegisterUser().register_user(
            rest.PlayerAddInfo(mess.from_user.username, mess.from_user.id))
        add_accord(mess.from_user.id, response)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("/register_on_sport")
        markup.add(button)
        to_pin = (await bot.send_message(mess.chat.id,
                                         "Вы зарегистрировались в системе.\n"
                                         "Для регистраци в какую-либо секцию, введите /register_on_sport\n"
                                         "В случае возникновения проблем, обращайтесь в 4ый комповник.",
                                         reply_markup=markup)).message_id
        await bot.pin_chat_message(mess.chat.id, to_pin)
        return
    if mess.text == "Нет, это не я. Отмена регистрации.":
        if await fuse_not_nf(mess):
            return
        await bot.send_message(mess.chat.id,
                               "Регистрация отменена. Если хотите зарегистрироваться, подойдите в 4ый комповник.")
        return
    if await fuse_nf(mess):
        return
    for sport in await rest.RestGetSportSections().get_sections():
        if sport == mess.text:
            try:
                await bot.send_message(mess.chat.id, f"Список участников секции {sport.name}:\n" + '\n'.join(
                    await rest.RestGetPlayersBySportSections().players_by_sport_sections(sport)))
            except BaseException:
                await bot.send_message(mess.chat.id, get_standart_message_to_exception())
                return
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton(f"create_{sport.en_name}")
            button2 = types.KeyboardButton(f"signup_{sport.en_name}")
            markup.add(button1, button2)
            await bot.send_message(mess.chat.id,
                                   f"Вы можете создать свою команду с помощью кнопки create_{sport.en_name},"
                                   f" или записаться в уже существующую, нажав на кнопку signup_{sport.en_name}",
                                   reply_markup=markup)
            return
        if f"signup_{sport.en_name}" == mess.text:
            buttons = []
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for team in get_list_of_all_commands(sport):
                buttons.append(types.KeyboardButton(f"{sport.en_name}: {team}"))
            markup.add(*buttons)
            await bot.send_message(mess.chat.id,
                                   f"Для выбора команды с названием название_команды нажмите кнопку <{sport.en_name}: название команды>",
                                   reply_markup=markup)
            return
        if f"create_{sport.en_name}" == mess.text:
            try:
                team = register_new_team(sport, mess.from_user.id)
            except BaseException:
                await bot.send_message(mess.chat.id, get_standart_message_to_exception())
                return
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton())
            await bot.send_message(mess.chat.id,
                                   f"Вы зарегистрировали новую команду. Название: {team}. Если захотите изменить название команды на новое_название, введите <set_name_{sport.en_name}_{team} новое_название>",
                                   reply_markup=markup)
            return
        if f"set_name_{sport.en_name}_" == mess.text[:len(f"set_name_{sport.en_name}_")]:
            team = mess.text.split('_')[3]
            try:
                new_team = mess.text.split(" ")[1]
            except BaseException:
                await bot.send_message(mess.chat.id, "Вы не ввели новое название команды")
                return
            msg = f"Название команды изменено на <{new_team}>"
            try:
                set_name_of_team(team, new_team)
            except TeamNotFound:
                pass

    await bot.send_message(mess.chat.id, "Я вас не понимаю.")