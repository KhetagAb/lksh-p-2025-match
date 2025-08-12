from lkshmatch.adapters.players import RestValidateRegisterPlayer, RestRegisterPlayer, PlayerAddInfo
from lkshmatch.adapters.sport_sections import SportSection, RestGetSportSections, RestGetPlayersBySportSections
from lkshmatch.adapters.core import InsufficientRights, NameTeamReserveError, TeamNotFound, UnknownError, PlayerNotFound, TeamIsFull
import logging
from telegram import Bot, Update
from fastapi import APIRouter, Request, FastAPI
from telebot.async_telebot import AsyncTeleBot, Handler
from telebot import types
from contextlib import asynccontextmanager
import random
from lkshmatch.config import settings


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     webhook_url = settings.get("WEBHOOK_URL")
#     await bot.set_webhook(
#         url=webhook_url,
#         drop_pending_updates=True
#     )
#     yield
#     await bot.delete_webhook()
#
#
# app = FastAPI(lifespan=lifespan)


# @app.post("/webhook")
# async def webhook_start_bot(req: Request) -> None:
#     await bot.process_new_updates([types.Update.de_json(await req.json())])


real_token = settings.get("MATCH_TELEGRAM_TOKEN")

token = ""

if real_token:
    token = real_token
else:
    # TODO: log error and continue work, because we have other frontends
    exit()

bot = AsyncTeleBot(token)

# Не будет использоваться в дальнейшем
def add_matching(tg_id: int, real_id) -> None:
    with open("accord.txt", 'a') as file:
        file.write(str(tg_id) + ';' + str(real_id) + '\n')


async def make_sports_buttons() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for sport in await RestGetSportSections().get_sections():
        buttons.append(types.KeyboardButton(sport.name))
    markup.add(*buttons)
    return markup


async def fuse_not_nf(mess: types.Message) -> bool:
    return False


async def fuse_nf(mess: types.Message) -> bool:
    return False


# В дальнейшем использоваться не будет, временный костыль
def get_role(id: int, sport: str) -> str:
    return ["admin", "user", "captain"][random.randrange(3)]


# список всех команд по названию спорта
def get_list_of_all_teams(sport: SportSection) -> list[str]:
    return [] # TODO: срочно реализовать


def set_name_of_team(old_team: str, new_team: str) -> None:
    return

# Возвращает tg_id-шник капитана команды


def add_person_to_team(team: str, tg_id: int) -> int:
    return 228777


def approve_adding_person_to_team():
    return


# возвращает название команды, которое присвоила система
def register_new_team(sport: SportSection, tg_id: int) -> str:
    return "Team 228"


def standart_message_to_base_exception() -> str:
    return "Извините, что-то пошло не так. Повторите позже или обратитесь в 4-ый комповник."


def standard_message_to_insufficient_rights() -> str:
    return f"У вас недостаточно прав для этого действия."


def make_noregister_markup(mess: types.Message, sport: str) -> types.ReplyKeyboardMarkup:
    role = get_role(mess.from_user.id, sport) # type: ignore
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    data_for_buttons = []
    if role == "user":
        data_for_buttons = ["/create_team", "/teams",
                            "/join_team", "/approve_member_join"]
    elif role == "captain":
        data_for_buttons = ["/teams", "/approve_member_join", "/delete_team"]
    elif role == "admin":
        pass
    buttons = map(types.KeyboardButton, map(
        lambda x: f"{x} {sport}", data_for_buttons))
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=["start"])
async def start(mess: types.Message) -> None:
    chat_id = mess.chat.id
    user_id = mess.from_user.id if mess.from_user is not None else 0
    username = mess.from_user.username if mess.from_user is not None else None
    if await fuse_not_nf(mess):
        return
    try:
        safe_username = username if username is not None else "unknown_user"
        msg = await RestValidateRegisterPlayer().validate_register_user(PlayerAddInfo(safe_username, int(user_id)))
    except PlayerNotFound:
        msg = "Извините, но вас нет в списках. Подойдите в 4-ый комповник."
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Это я, регистрацию подтверждаю.")
        button2 = types.KeyboardButton("Нет, это не я. Отмена регистрации.")
        markup.add(button1, button2)
        await bot.send_message(mess.chat.id,
                               f"{msg},\nмы нашли Вас в базе. Это вы?",
                               reply_markup=markup)
        return
    except UnknownError as ue:
        print(ue)
        msg = standart_message_to_base_exception()
    await bot.send_message(mess.chat.id, msg)


@bot.message_handler(commands=["register_on_sport"])
async def register_on_sport(mess: types.Message) -> None:
    if await fuse_nf(mess):
        return
    markup = await make_sports_buttons()
    await bot.send_message(mess.chat.id, "Выберите секцию", reply_markup=markup)


async def processing_of_registration(mess: types.Message) -> bool:
    if mess.text == "Это я, регистрацию подтверждаю.":
        if await fuse_not_nf(mess):
            await bot.send_message(mess.chat.id, "Вы не начинали регистрацию.")
            return True
        if mess.from_user is not None:
            username = mess.from_user.username if mess.from_user.username is not None else "unknown_user"
            user_id = mess.from_user.id
        else:
            username = "unknown_user"
            user_id = 0  # or handle appropriately
        response = await RestRegisterPlayer().register_user(
            PlayerAddInfo(username, user_id))
        if mess.from_user is not None:
            add_matching(mess.from_user.id, response)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/register_on_sport"))
        to_pin = (await bot.send_message(mess.chat.id,
                                         "Вы зарегистрировались в системе.\n"
                                         "Для регистрации в какую-либо секцию, введите /register_on_sport\n"
                                         "В случае возникновения проблем, обращайтесь в 4-ый комповник.",
                                         reply_markup=markup)).message_id
        await bot.pin_chat_message(mess.chat.id, to_pin)
        return True
    if mess.text == "Нет, это не я. Отмена регистрации.":
        if await fuse_not_nf(mess):
            await bot.send_message(mess.chat.id, "Вы не начинали регистрацию.")
            return True
        await bot.send_message(mess.chat.id,
                               "Регистрация отменена. Если хотите зарегистрироваться, подойдите в 4-ый комповник.")
        return True
    return False


async def processing_select_sport(mess: types.Message, sport: SportSection) -> bool:
    if sport.name == mess.text:
        try:
            list_of_all_participants = await RestGetPlayersBySportSections().get_players_by_sport_sections(sport)
            msg = [participant.name for participant in list_of_all_participants]
            await bot.send_message(mess.chat.id, f"Список участников секции {sport.name}:\n" + '\n'.join(msg))
        except UnknownError as ue:
            print(ue)
            await bot.send_message(mess.chat.id, standart_message_to_base_exception())
            return True
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        create = types.KeyboardButton(f"create_{sport.en_name}")
        signup = types.KeyboardButton(f"signup_{sport.en_name}")
        markup.add(create, signup)
        await bot.send_message(mess.chat.id,
                               f"Вы можете создать свою команду с помощью кнопки create_{sport.en_name},"
                               f" или записаться в уже существующую, нажав на кнопку signup_{sport.en_name}",
                               reply_markup=markup)
        return True
    return False


async def setname_team(mess: types.Message, sport: SportSection) -> bool:
    setname_string = f"set_name_{sport.en_name}_"
    if mess.text is not None and setname_string == mess.text[:len(setname_string)]:
        try:
            team = mess.text[len(
                f"set_name_{sport.en_name}_"):mess.text.find(": ")]
        except Exception as ue:
            print(ue)
            await bot.send_message(mess.chat.id, "Вы не ввели текущее название команды.")
            return True
        try:
            new_team = ": ".join(mess.text.split(": ")[1:])
        except Exception as ue:
            print(ue)
            await bot.send_message(mess.chat.id, "Вы не ввели новое название команды.")
            return True
        msg = f"Название команды изменено на <{new_team}>."
        try:
            set_name_of_team(team, new_team)
        except TeamNotFound:
            msg = f"Команда {team} не найдена в секции {sport.name}."
        except NameTeamReserveError:
            msg = f"Название {new_team} уже занято. Если хотите сменить название, повторите операцию, но с другим новым названием."
        except InsufficientRights:
            msg = standard_message_to_insufficient_rights()
        except UnknownError as ue:
            print(ue)
            msg = standart_message_to_base_exception()
        await bot.send_message(mess.chat.id, msg)
        return True
    return False


async def create_team(mess: types.Message, sport: SportSection) -> bool:
    if f"create_{sport.en_name}" == mess.text:
        team = ""
        try:
            team = register_new_team(sport, mess.from_user.id) # type: ignore
        except InsufficientRights:
            await bot.send_message(mess.chat.id, standard_message_to_insufficient_rights())
        except UnknownError as ue:
            print(ue)
            await bot.send_message(mess.chat.id, standart_message_to_base_exception())
            return True
        await bot.send_message(mess.chat.id,
                               f"Вы зарегистрировали новую команду. Название: {team}. Если захотите изменить название команды на новое_название, введите <set_name_{sport.en_name}_{team}: новое_название>.")
        return True
    return False


async def signup_to_sport(mess: types.Message, sport: SportSection) -> bool:
    if f"signup_{sport.en_name}" == mess.text:
        buttons = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for team in get_list_of_all_teams(sport):
            buttons.append(types.KeyboardButton(f"{sport.en_name}: {team}"))
        markup.add(*buttons)
        await bot.send_message(mess.chat.id,
                               f"Для выбора команды с названием название_команды нажмите кнопку <{sport.en_name}: название команды>",
                               reply_markup=markup)
        return True
    return False


async def make_request_to_add_in_team(mess: types.Message, sport: SportSection) -> bool:
    if f"{sport.en_name}: " in mess.text: # type: ignore
        team = mess.text[len(f"{sport.en_name}: "):] # type: ignore
        try:
            add_person_to_team(team, mess.from_user.id) # type: ignore
        except TeamIsFull:
            pass
        return True
    return False


async def approve_adding_person_in_team():
    pass


@bot.message_handler(content_types=["text"])
async def answer_to_buttons(mess: types.Message) -> None:
    if await processing_of_registration(mess):
        return
    if await fuse_nf(mess):
        return
    for sport in await RestGetSportSections().get_sections():
        if await processing_select_sport(mess, sport):
            return
        if signup_to_sport(mess, sport):
            return
        if make_request_to_add_in_team(mess, sport):
            return
        if await setname_team(mess, sport):
            return
        if await setname_team(mess, sport):
            return
    await bot.send_message(mess.chat.id, "Я вас не понимаю.")
