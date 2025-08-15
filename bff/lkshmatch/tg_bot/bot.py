import asyncio
import datetime
import logging
from enum import Enum
from typing import Optional

from telebot import types
from telebot.async_telebot import AsyncTeleBot

from lkshmatch.adapters.base import (
    Activity,
    ActivityAdapter,
    InsufficientRights,
    Player,
    PlayerAdapter,
    PlayerNotFound,
    PlayerToRegister,
    SportAdapter,
    SportSection,
    UnknownError, PlayerAlreadyRegistered,
)
from lkshmatch.config import settings
from lkshmatch.di import app_container
from lkshmatch.domain.repositories.student_repository import LKSHStudentsRepository


# TODO разобраться как работает
class Msg(Enum):
    REGISTRATION_USER_NOT_FOUND = "😔 Извините, но вас нет в списках. Подойдите в 4-ый комповник."
    REGISTRATION_CONFIRM_QUESTION = "🎉 %s, мы нашли вас. Это вы?"
    REGISTRATION_CONFIRMED = "🍾 Вы зарегистрировались в системе.\n\n" + \
                             "✅ Для регистрации на активность, введите /register_on_sport."
    REGISTRATION_ALREADY_REGISTERED = "🟢 Не переживайте, вы уже зарегистрированы."
    REGISTRATION_CANCELED = "❌ Регистрация отменена. Если хотите зарегистрироваться, подойдите в 4-ый комповник."

    INSUFFICIENT_RIGHTS = "У вас недостаточно прав для этого действия."
    INTERNAL_ERROR = "Извините, что-то пошло не так. Обратитесь в 4-ый комповник к команде P."


class Buttons(Enum):
    REGISTRATION_CONFIRM = "✅ Подтверждаю."
    REGISTRATION_CANCEL = "❌ Отмена регистрации."

    SPORT_REGISTER_ON = "Записаться на активность"

    def tg(self):
        return types.KeyboardButton(self.value)


logging.basicConfig(level=logging.INFO)

activity_adapter = app_container.get(ActivityAdapter)
sport_adapter = app_container.get(SportAdapter)
player_adapter = app_container.get(PlayerAdapter)

students_repository = app_container.get(LKSHStudentsRepository)

try:
    token = settings.get("TELEGRAM_TOKEN")
    if token is None:
        raise ValueError("TG token required!")
    bot = AsyncTeleBot(token)
    logging.info(f"Telegram bot started, token: {token}")
except Exception as e:
    logging.error(f"Ошибка создания Telegram бота: {e}")
    exit(1)


async def make_sports_buttons() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for sport in await sport_adapter.get_sport_list():
        buttons.append(types.KeyboardButton(sport.ru_name))
    markup.add(*buttons)
    return markup


async def make_activity_buttons(sport: SportSection) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for activity in await activity_adapter.get_activities_by_sport_section(sport.id):
        buttons.append(types.KeyboardButton(activity.title))
    markup.add(*buttons)
    return markup


async def make_choose_registration_buttons() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(Buttons.REGISTRATION_CONFIRM.value)
    button2 = types.KeyboardButton(Buttons.REGISTRATION_CANCEL.value)
    markup.add(button1, button2)
    return markup


# def make_noregister_markup(mess: types.Message, sport: str) -> types.ReplyKeyboardMarkup:
#     role = get_role(mess.from_user.id, sport)
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     data_for_buttons = []
#     if role == "user":
#         data_for_buttons = ["/create_team", "/teams", "/join_team", "/approve_member_join"]
#     elif role == "captain":
#         data_for_buttons = ["/teams", "/approve_member_join", "/delete_team"]
#     elif role == "admin":
#         pass
#     buttons = map(types.KeyboardButton, map(lambda x: f"{x} {sport}", data_for_buttons))
#     markup.add(*buttons)
#     return markup

async def message_without_buttons(mess: types.Message, text: str = None) -> types.Message:
    return await bot.send_message(chat_id=mess.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())


async def message_with_buttons(mess: types.Message, buttons: types.ReplyKeyboardMarkup, text: str) -> types.Message:
    return await bot.send_message(chat_id=mess.chat.id, text=text, reply_markup=buttons)


async def validate_user(mess: types.Message) -> tuple[Optional[int], Optional[str]]:
    if mess.from_user.id is None or mess.from_user.username is None:
        await message_without_buttons(mess, Msg.INTERNAL_ERROR.value)
        logging.warning(log_info("User hasn't got username or tg_id", mess))
        return None, None
    return mess.from_user.id, mess.from_user.username


def log_text(text: str, mess: types.Message) -> str:
    return text + (f" [username: @{mess.from_user.username}, tg_id: {mess.from_user.id},"
                   f" time: {datetime.datetime.fromtimestamp(mess.date)}]")


def log_info(text: str, mess: types.Message) -> None:
    logging.info(log_text(text, mess))


def log_warning(text: str, mess: types.Message) -> None:
    logging.warning(log_text(text, mess))


def log_error(text: str, mess: types.Message) -> None:
    logging.error(log_text(text, mess))


@bot.message_handler(commands=["start"])
async def start(mess: types.Message) -> None:
    log_info("Called /start.", mess)
    user_id, username = await validate_user(mess)
    if user_id is None:
        return
    try:
        user_name = await students_repository.validate_register_user(Player(username, int(user_id)))
        await message_with_buttons(
            mess=mess,
            text=Msg.REGISTRATION_CONFIRM_QUESTION.value % user_name,
            buttons=await make_choose_registration_buttons(),
        )
    except PlayerNotFound:
        log_warning("User not found in lksh database. Validate failed.", mess)
        await message_without_buttons(mess, Msg.REGISTRATION_USER_NOT_FOUND.value)
    except UnknownError as ue:
        log_error(f"Internal error: {ue}. Validate failed.", mess)
        await message_without_buttons(mess, Msg.INTERNAL_ERROR.value)
    log_info("Finished /start successfully.", mess)


@bot.message_handler(commands=["register_on_sport"])
async def register_on_sport(mess: types.Message) -> None:
    log_info(f"Called /register_on_sport.", mess)
    await message_with_buttons(
        mess,
        text="Выберите спортивную секцию.",
        buttons=await make_sports_buttons(),
    )
    log_info("Finished /register_on_sport successfully.", mess)


# TODO перехватывать нажатия на пноки
async def processing_of_registration(mess: types.Message) -> bool:
    if mess.text == Buttons.REGISTRATION_CONFIRM.value:
        log_info("Registration accepted.", mess)
        user_id, username = await validate_user(mess)
        if user_id is None:
            return True

        try:
            user_name = await students_repository.validate_register_user(Player(username, int(user_id)))
            await player_adapter.register_user(PlayerToRegister(username, user_id, user_name))
            to_pin = (
                await message_with_buttons(
                    mess=mess,
                    text=Msg.REGISTRATION_CONFIRMED.value,
                    buttons=types.ReplyKeyboardMarkup(resize_keyboard=True).
                    add(Buttons.SPORT_REGISTER_ON.tg()),
                )
            ).message_id
            await bot.pin_chat_message(mess.chat.id, to_pin)
        except PlayerNotFound:
            log_warning("User not found in lksh database. Validate failed.", mess)
            await message_without_buttons(mess, Msg.REGISTRATION_USER_NOT_FOUND.value)
        except PlayerAlreadyRegistered:
            log_warning("User already registered.", mess)
            await message_without_buttons(mess, Msg.REGISTRATION_ALREADY_REGISTERED.value)
        except UnknownError as ue:
            log_error(f"Internal error: {ue}. Validate failed.", mess)
            await message_without_buttons(mess, Msg.INTERNAL_ERROR.value)
        await register_on_sport(mess)
        return True
    if mess.text == Buttons.REGISTRATION_CANCEL.value:
        await message_without_buttons(
            mess=mess,
            text=Msg.REGISTRATION_CANCELED.value
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
            await bot.send_message(mess.chat.id, Msg.INTERNAL_ERROR.value)
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


# async def setname_team(mess: types.Message, activity: Activity) -> bool:
#     setname_string = f"set_name_{activity.title}_"
#     if mess.text is not None and setname_string == mess.text[: len(setname_string)]:
#         try:
#             team = mess.text[len(f"set_name_{activity.title}_"): mess.text.find(": ")]
#         except Exception as ue:
#             print(ue)
#             await bot.send_message(mess.chat.id, "Вы не ввели текущее название команды.")
#             return True
#         try:
#             new_team = ": ".join(mess.text.split(": ")[1:])
#         except Exception as ue:
#             print(ue)
#             await bot.send_message(mess.chat.id, "Вы не ввели новое название команды.")
#             return True
#         msg = f"Название команды изменено на <{new_team}>."
#         try:
#             set_name_of_team(team, new_team)
#         except TeamNotFound:
#             msg = f"Команда {team} не найдена в секции {activity.title}."
#         except NameTeamReserveError:
#             msg = f"Название {new_team} уже занято. Если хотите сменить название, повторите операцию, но с другим новым названием."
#         except InsufficientRights:
#             msg = Msg.INSUFFICIENT_RIGHTS.value
#         except UnknownError as ue:
#             print(ue)
#             msg = Msg.INTERNAL_ERROR.value
#         await bot.send_message(mess.chat.id, msg)
#         return True
#     return False


async def enroll_player_in_activity(mess: types.Message, activity: Activity) -> bool:
    if f"create {activity.title}" == mess.text:
        team = ""
        try:
            team = await app_container.get(ActivityAdapter).enroll_player_in_activity(activity.id,
                                                                                      mess.from_user.id)  # type: ignore
        except InsufficientRights:
            await bot.send_message(mess.chat.id, Msg.INSUFFICIENT_RIGHTS.value)
        except UnknownError as ue:
            print(ue)
            await bot.send_message(mess.chat.id, Msg.INTERNAL_ERROR.value)
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
            "Для выбора события, нажмите кнопку.",
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


# todo сделать более умную обработку кнопок
@bot.message_handler(content_types=["text"])
async def answer_to_buttons(mess: types.Message) -> None:
    if await (
            processing_of_registration(mess)):
        return
    for sport in await app_container.get(SportAdapter).get_sport_list():
        if await signup_to_sport(mess, sport):
            return
        for activity in await activity_adapter.get_activities_by_sport_section(sport.id):
            if await processing_select_activity(mess, activity):
                return
            if await signup_to_activity(mess, activity):
                return
            if await enroll_player_in_activity(mess, activity):
                return
            # if await setname_team(mess, activity):
            #     return
    await bot.send_message(mess.chat.id, "Я вас не понимаю.")


asyncio.run(bot.polling(non_stop=True, none_stop=True))
