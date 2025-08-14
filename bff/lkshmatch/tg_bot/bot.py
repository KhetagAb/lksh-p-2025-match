import logging
import os
import random
import asyncio

from telebot import types
from telebot.async_telebot import AsyncTeleBot

from lkshmatch.adapters.base import (
    InsufficientRights,
    NameTeamReserveError,
    Player,
    PlayerNotFound,
    PlayerToRegister,
    SportSection,
    TeamNotFound,
    UnknownError,
    Activity, ActivityAdapter, SportAdapter, PlayerAdapter
)
from lkshmatch.di import app_container
from lkshmatch.domain.repositories.student_repository import LKSHStudentsRepository

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


token = os.getenv("TELEGRAM_TOKEN")
logging.info(f"TELEGRAM_TOKEN: {token}")

if token is None:
    raise ValueError("TG token required!")

try:
    bot = AsyncTeleBot(token)
except Exception as e:
    logging.error(f"Ошибка создания Telegram бота: {e}")
    exit(1)


def add_matching(tg_id: int, real_id) -> None:
    # Не будет использоваться в дальнейшем
    with open("accord.txt", "a") as file:
        file.write(str(tg_id) + ";" + str(real_id) + "\n")


async def make_sports_buttons() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for sport in await app_container.get(SportAdapter).get_sport_list():
        buttons.append(types.KeyboardButton(sport.ru_name))
    markup.add(*buttons)
    return markup


async def make_activity_buttons(sport: SportSection) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for activity in await app_container.get(ActivityAdapter).get_activities_by_sport_section(sport.id):
        buttons.append(types.KeyboardButton(activity.title))
    markup.add(*buttons)
    return markup


# предохранитель, чтобы юзер не мог регистрироваться по несколько раз
async def fuse_not_nf(mess: types.Message) -> bool:
    return False


# предохранитель, чтобы юзер не мог ничего делать, если он не зареган
async def fuse_nf(mess: types.Message) -> bool:
    return False


def standart_message_to_base_exception() -> str:
    return "Извините, что-то пошло не так. Повторите позже или обратитесь в 4-ый комповник."


def standard_message_to_insufficient_rights() -> str:
    return "У вас недостаточно прав для этого действия."


def make_noregister_markup(mess: types.Message, sport: str) -> types.ReplyKeyboardMarkup:
    role = get_role(mess.from_user.id, sport)  # type: ignore
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    data_for_buttons = []
    if role == "user":
        data_for_buttons = ["/create_team", "/teams", "/join_team", "/approve_member_join"]
    elif role == "captain":
        data_for_buttons = ["/teams", "/approve_member_join", "/delete_team"]
    elif role == "admin":
        pass
    buttons = map(types.KeyboardButton, map(lambda x: f"{x} {sport}", data_for_buttons))
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
        repo = app_container.get(LKSHStudentsRepository)
        msg = await repo.validate_register_user(Player(safe_username, int(user_id)))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Это я, регистрацию подтверждаю.")
        button2 = types.KeyboardButton("Нет, это не я. Отмена регистрации.")
        markup.add(button1, button2)
        await bot.send_message(mess.chat.id, f"{msg},\nмы нашли Вас в базе. Это вы?", reply_markup=markup)
        return
    except PlayerNotFound:
        msg = "Извините, но вас нет в списках. Подойдите в 4-ый комповник."
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
        response = await app_container.get(PlayerAdapter).register_user(
            PlayerToRegister(username, user_id, "TESTNAME_FIX")
        )
        if mess.from_user is not None:
            add_matching(mess.from_user.id, response)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/register_on_sport"))
        to_pin = (
            await bot.send_message(
                mess.chat.id,
                "Вы зарегистрировались в системе.\n"
                "Для регистрации в какую-либо секцию, введите /register_on_sport\n"
                "В случае возникновения проблем, обращайтесь в 4-ый комповник.",
                reply_markup=markup,
            )
        ).message_id
        await bot.pin_chat_message(mess.chat.id, to_pin)
        return True
    if mess.text == "Нет, это не я. Отмена регистрации.":
        if await fuse_not_nf(mess):
            await bot.send_message(mess.chat.id, "Вы не начинали регистрацию.")
            return True
        await bot.send_message(
            mess.chat.id, "Регистрация отменена. Если хотите зарегистрироваться, подойдите в 4-ый комповник."
        )
        return True
    return False


async def processing_select_activity(mess: types.Message, activity: Activity) -> bool:
    if activity.title == mess.text:
        try:
            list_of_all_teams = await app_container.get(ActivityAdapter).get_teams_by_activity_id(activity.id)
            # TODO: id -> name
            msg = [team.name for team in list_of_all_teams]
            await bot.send_message(mess.chat.id, f"Список участников секции {activity.title}:\n" + "\n".join(msg))
        except UnknownError as ue:
            print(ue)
            await bot.send_message(mess.chat.id, standart_message_to_base_exception())
            return True
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        create = types.KeyboardButton(f"create {activity.title}")
        signup = types.KeyboardButton(f"signup {activity.title}")
        markup.add(create, signup)
        await bot.send_message(
            mess.chat.id,
            f"Вы можете создать свою команду с помощью кнопки <create {activity.title}>,"
            f" или записаться в уже существующую, нажав на кнопку <signup {activity.title}>",
            reply_markup=markup,
        )
        return True
    return False


async def setname_team(mess: types.Message, activity: Activity) -> bool:
    setname_string = f"set_name_{activity.title}_"
    if mess.text is not None and setname_string == mess.text[: len(setname_string)]:
        try:
            team = mess.text[len(f"set_name_{activity.title}_"): mess.text.find(": ")]
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
            msg = f"Команда {team} не найдена в секции {activity.title}."
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


async def create_team(mess: types.Message, activity: Activity) -> bool:
    if f"create {activity.title}" == mess.text:
        team = ""
        try:
            team = await app_container.get(ActivityAdapter).enroll_player_in_activity(activity.id, mess.from_user.id)  # type: ignore
        except InsufficientRights:
            await bot.send_message(mess.chat.id, standard_message_to_insufficient_rights())
        except UnknownError as ue:
            print(ue)
            await bot.send_message(mess.chat.id, standart_message_to_base_exception())
            return True
        await bot.send_message(
            mess.chat.id,
            f"Вы зарегистрировали новую команду. Название: {team.name}. Если захотите изменить название команды на новое_название, введите <set_name {activity.title}|{team.name}: новое_название>.",
        )
        return True
    return False


async def signup_to_sport(mess: types.Message, sport: SportSection) -> bool:
    if f"{sport.ru_name}" == mess.text:
        markup = await make_activity_buttons(sport)
        await bot.send_message(
            mess.chat.id,
            f"Для выбора события, нажмите кнопку.",
            reply_markup=markup,
        )
        return True
    return False


async def signup_to_activity(mess: types.Message, activity: Activity) -> bool:
    if mess.text == activity:  # type: ignore
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        signup_button = types.KeyboardButton(f"signup {activity.title}")
        create_button = types.KeyboardButton(f"create {activity.title}")
        markup.add(signup_button, create_button)
        await bot.send_message(
            mess.chat.id,
            f"Для записи в уже существующую команду, нажмите <signup {activity.title}>, для создания новой команды, нажмите <create_{activity.title}>",
            reply_markup=markup,
        )
    return False


async def approve_adding_person_in_team():
    pass


@bot.message_handler(content_types=["text"])
async def answer_to_buttons(mess: types.Message) -> None:
    if await processing_of_registration(mess):
        return
    if await fuse_nf(mess):
        return
    for sport in await app_container.get(SportAdapter).get_sport_list():
        if await signup_to_sport(mess, sport):
            return
        for activity in await app_container.get(ActivityAdapter).get_activities_by_sport_section(sport.id):
            if await processing_select_activity(mess, activity):
                return
            if await signup_to_activity(mess, activity):
                return
            if await  create_team(mess, activity):
                return
            if await setname_team(mess, activity):
                return
    await bot.send_message(mess.chat.id, "Я вас не понимаю.")


asyncio.run(bot.polling(non_stop=True, none_stop=True))