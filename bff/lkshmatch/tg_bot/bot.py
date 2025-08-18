import datetime
import logging
from enum import Enum
from typing import Optional

from telebot import types
from telebot.async_telebot import AsyncTeleBot

from lkshmatch.adapters.base import (Activity, ActivityAdapter, InsufficientRights, Player, PlayerAdapter,
                                     PlayerAlreadyInTeam, PlayerNotFound, PlayerToRegister, SportAdapter, UnknownError,
                                     PlayerAlreadyRegistered, )
from lkshmatch.config import settings
from lkshmatch.di import app_container
from lkshmatch.domain.repositories.student_repository import LKSHStudentsRepository


class Msg(Enum):
    REGISTRATION_USER_NOT_FOUND = "😔 Извините, но вас нет в списках. Подойдите в 4-ый комповник."
    REGISTRATION_CONFIRM_QUESTION = "🎉 %s, мы нашли вас. Это вы?"
    REGISTRATION_CONFIRMED = "🍾 Вы зарегистрировались в системе.\n\n" + "✅ Для регистрации на активность, введите /register_on_sport."
    REGISTRATION_ALREADY_REGISTERED = "🟢 Не переживайте, вы уже зарегистрированы."
    REGISTRATION_CANCELED = "❌ Регистрация отменена. Если хотите зарегистрироваться, подойдите в 4-ый комповник."

    INSUFFICIENT_RIGHTS = "У вас недостаточно прав для этого действия."
    INTERNAL_ERROR = "Извините, что-то пошло не так. Обратитесь в 4-ый комповник к команде P."

    TECHNICAL_SUPPORT = "Опишите свою проблему в ответном сообщении, мы постараемся оперативно ответить."


class Buttons(Enum):
    REGISTRATION_CONFIRM = ("✅ Подтверждаю", "reg_confirm")
    REGISTRATION_CANCEL = ("❌ Отмена регистрации", "reg_cancel")
    SPORTS_REGISTER_ON = ("Записаться на активность", "sports_register")
    TECHNICAL_SUPPORT = ("Написать в техподдержку.", "")

    def __init__(self, text, callback_data):
        self.text = text
        self.callback_data = callback_data

    def inline(self) -> types.InlineKeyboardButton:
        return types.InlineKeyboardButton(text=self.text, callback_data=self.callback_data)

    def keyboard(self):
        return types.KeyboardButton(self.text)


logging.basicConfig(level=logging.INFO)

activity_adapter = app_container.get(ActivityAdapter)
sport_adapter = app_container.get(SportAdapter)
player_adapter = app_container.get(PlayerAdapter)

students_repository = app_container.get(LKSHStudentsRepository)


# Защита от Шоно
async def shono_fuse(mess: types.Message):
    if mess.from_user.id == 1026324598:
        await bot.send_message(mess.chat.id, "Шоно перестань, займись делом.", message_thread_id=mess.message_thread_id)
        return True
    return False


def log_text(text: str, mess: types.Message) -> str:
    return text + (f" [username: @{mess.from_user.username}, tg_id: {mess.from_user.id},"
                   f" time: {datetime.datetime.fromtimestamp(mess.date)}]")


def log_info(text: str, mess: types.Message) -> None:
    logging.info(log_text(text, mess))


def log_warning(text: str, mess: types.Message) -> None:
    logging.warning(log_text(text, mess))


def log_error(text: str, mess: types.Message) -> None:
    logging.error(log_text(text, mess))


try:
    token = settings.get("TELEGRAM_TOKEN")
    if token is None:
        raise ValueError("TG token required!")
    bot = AsyncTeleBot(token)
    logging.info(f"Telegram bot started, token: {token}")
except Exception as e:
    logging.error(f"Ошибка создания Telegram бота: {e}")
    exit(1)

try:
    support_chat_id = settings.get("SUPPORT_CHAT_ID")
    if support_chat_id is None:
        raise ValueError("SUPPORT_CHAT_ID required!")
    logging.info(f"Support chat ID: {support_chat_id}")
except Exception as e:
    logging.error(f"Error {e}")
    exit(1)

try:
    support_chat_thread_id = settings.get("SUPPORT_CHAT_THREAD_ID")
    if support_chat_thread_id is None:
        raise ValueError("SUPPORT_CHAT_THREAD_ID required!")
    logging.info(f"Support chat thread ID: {support_chat_thread_id}")
except Exception as e:
    logging.error(f"Error {e}")
    exit(1)


async def make_sports_buttons() -> types.InlineKeyboardMarkup:
    buttons: list[types.InlineKeyboardButton] = []
    for sport in await sport_adapter.get_sport_list():
        button = types.InlineKeyboardButton(text=sport.ru_name.capitalize(), callback_data=f"sport_{sport.id}")
        buttons.append(button)
    markup = types.InlineKeyboardMarkup()
    return markup.add(*buttons, row_width=3)


async def make_sports_buttons_except_one(sport_id: int, new_text: str) -> types.InlineKeyboardMarkup:
    buttons: list[types.InlineKeyboardButton] = []
    for sport in await sport_adapter.get_sport_list():
        button = types.InlineKeyboardButton(text=sport.ru_name.capitalize() if sport_id != sport.id else new_text,
            callback_data=f"sport_{sport.id}")
        buttons.append(button)
    markup = types.InlineKeyboardMarkup()
    return markup.add(*buttons, row_width=3)


async def make_activity_buttons(activities: list[Activity]) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for activity in activities:
        button = types.InlineKeyboardButton(text=activity.title, callback_data=f"activity_{activity.id}")
        markup.add(button)
    return markup


async def make_choose_registration_buttons() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    confirm_btn = Buttons.REGISTRATION_CONFIRM.inline()
    cancel_btn = Buttons.REGISTRATION_CANCEL.inline()
    markup.add(confirm_btn, cancel_btn)
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

async def msg_with_ibuttons(mess: types.Message, text: str, buttons: types.InlineKeyboardMarkup) -> types.Message:
    return await bot.send_message(chat_id=mess.chat.id, text=text, reply_markup=buttons,
                                  message_thread_id=mess.message_thread_id)


async def msg_with_buttons(mess: types.Message, text: str, buttons: types.ReplyKeyboardMarkup) -> types.Message:
    return await bot.send_message(chat_id=mess.chat.id, text=text, reply_markup=buttons,
                                  message_thread_id=mess.message_thread_id)


async def msg_without_buttons(mess: types.Message, text: str) -> types.Message:
    return await bot.send_message(chat_id=mess.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove(),
                                  message_thread_id=mess.message_thread_id)


async def edit_with_ibuttons(call: types.CallbackQuery, text: str, buttons: types.InlineKeyboardMarkup) -> None:
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
        reply_markup=buttons)


async def edit_without_buttons(call: types.CallbackQuery, text: str) -> None:
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)


async def validate_user(mess: types.Message) -> tuple[Optional[int], Optional[str]]:
    if mess.from_user.id is None or mess.from_user.username is None:
        await msg_without_buttons(mess, Msg.INTERNAL_ERROR.value)
        logging.warning(log_info("User hasn't got username or tg_id", mess))
        return None, None
    return mess.from_user.id, mess.from_user.username


@bot.message_handler(commands=["start"])
async def start(mess: types.Message) -> None:
    if await shono_fuse(mess):
        return
    log_info("Called /start.", mess)
    user_id, username = await validate_user(mess)
    if user_id is None:
        return
    try:
        user_name = await students_repository.validate_register_user(Player(username, int(user_id)))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.add(types.KeyboardButton(Buttons.TECHNICAL_SUPPORT.value[0]))
        await msg_with_buttons(mess, "Здравствуйте!", markup)
        await msg_with_ibuttons(mess=mess, text=Msg.REGISTRATION_CONFIRM_QUESTION.value % user_name,
            buttons=await make_choose_registration_buttons(), )
    except PlayerNotFound:
        log_warning("User not found in lksh database. Validate failed.", mess)
        await msg_without_buttons(mess, Msg.REGISTRATION_USER_NOT_FOUND.value)
    except UnknownError as ue:
        log_error(f"Internal error: {ue}. Validate failed.", mess)
        await msg_without_buttons(mess, Msg.INTERNAL_ERROR.value)
    log_info("Finished /start successfully.", mess)


@bot.callback_query_handler(func=lambda call: call.data in [Buttons.REGISTRATION_CONFIRM.callback_data,
                                                            Buttons.REGISTRATION_CANCEL.callback_data])
async def processing_of_registration(call: types.CallbackQuery) -> None:
    await bot.answer_callback_query(call.id)
    if await shono_fuse(call.message):
        return
    if call.data == Buttons.REGISTRATION_CONFIRM.callback_data:
        log_info("Registration accepted.", call.message)
        user_id, username = call.from_user.id, call.from_user.username
        if user_id is None or username is None:
            await edit_without_buttons(call, Msg.INTERNAL_ERROR.value)
            return

        sport_markup = types.InlineKeyboardMarkup()
        sport_btn = Buttons.SPORTS_REGISTER_ON.inline()
        sport_markup.add(sport_btn)

        try:
            user_name = await students_repository.validate_register_user(Player(username, int(user_id)))
            await player_adapter.register_user(PlayerToRegister(username, user_id, user_name))

            await edit_with_ibuttons(call, Msg.REGISTRATION_CONFIRMED.value,
                                     sport_markup)  # await bot.pin_chat_message(call.message.chat.id, call.message.message_id)
        except PlayerNotFound:
            log_warning("User not found in lksh database. Validate failed.", call.message)
            await edit_without_buttons(call, Msg.REGISTRATION_USER_NOT_FOUND.value)
        except PlayerAlreadyRegistered:
            log_warning("User already registered.", call.message)
            await edit_with_ibuttons(call, Msg.REGISTRATION_ALREADY_REGISTERED.value, sport_markup)
        except UnknownError as ue:
            log_error(f"Internal error: {ue}. Validate failed.", call.message)
            await edit_without_buttons(call, Msg.INTERNAL_ERROR.value)
    elif call.data == Buttons.REGISTRATION_CANCEL.callback_data:
        await edit_without_buttons(call, Msg.REGISTRATION_CANCELED.value)


@bot.message_handler(commands=["register_on_sport"])
async def register_on_sport(mess: types.Message) -> None:
    if await shono_fuse(mess):
        return
    log_info(f"Called /register_on_sport.", mess)
    to_pin = (await msg_with_ibuttons(mess=mess, text="Выберите спортивную секцию.",
        buttons=await make_sports_buttons(), )).message_id
    log_warning(str(to_pin), mess)
    await bot.pin_chat_message(mess.chat.id, to_pin)
    log_info("Finished /register_on_sport successfully.", mess)


@bot.callback_query_handler(func=lambda call: call.data == Buttons.SPORTS_REGISTER_ON.callback_data)
async def handle_sport_register_callback(call: types.CallbackQuery) -> None:
    await bot.answer_callback_query(call.id)
    if await shono_fuse(call.message):
        return
    markup = await make_sports_buttons()
    await msg_with_ibuttons(call.message, "Выберите спортивную секцию:", markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("sport_"))
async def select_sport(call: types.CallbackQuery) -> None:
    await bot.answer_callback_query(call.id)
    if await shono_fuse(call.message):
        return
    sport_id = int(call.data.split("_")[1])
    for s in await sport_adapter.get_sport_list():
        if s.id == sport_id:
            activities = await activity_adapter.get_activities_by_sport_section(sport_id)

            if len(activities) == 0:
                markup = await make_sports_buttons_except_one(sport_id, "💤 ПУСТО")
                await edit_with_ibuttons(call, "Выберите спортивную секцию:", markup)
                return
            if len(activities) == 1:
                await select_activity(call, activities[0])
                return

            markup = await make_activity_buttons(activities)
            await edit_with_ibuttons(call, "Для выбора события, нажмите кнопку.", markup)
            return
    await edit_without_buttons(call, "Спортивная секция не найдена.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("activity_"))
async def processing_select_activity(call: types.CallbackQuery) -> None:
    await bot.answer_callback_query(call.id)
    if await shono_fuse(call.message):
        return
    activity_id = int(call.data.split("_")[1])
    activity = await get_activity_by_id(activity_id)
    if not activity:
        await edit_without_buttons(call, "Активность не найдена.")
        return

    await select_activity(call, activity)


async def get_activity_by_id(activity_id):
    # TODO переделать на получение активности по id эффективнее
    activity = None
    for sport in await sport_adapter.get_sport_list():
        activities = await activity_adapter.get_activities_by_sport_section(sport.id)
        for act in activities:
            if act.id == activity_id:
                activity = act
                break
        if activity:
            break
    return activity


async def select_activity(call: types.CallbackQuery, activity: Activity) -> None:
    try:
        list_of_all_teams = await activity_adapter.get_teams_by_activity_id(activity.id)
        description = f"ℹ️ Описание: {activity.description}\n\n" if activity.description else ""
        # TODO: id -> name
        if list_of_all_teams:
            numbered_teams = [f"{i + 1}. {team.name}" for i, team in enumerate(list_of_all_teams)]
            # todo сделать поддерждку команда/участник
            teams_text = f"🏆 {activity.title}\n\n{description}📋 Список участников:\n\n" + "\n".join(numbered_teams)
        else:
            teams_text = f"🏆 {activity.title}\n\n📋 Пока нет участников."

        # TODO вынести
        markup = types.InlineKeyboardMarkup()
        create = types.InlineKeyboardButton("Записаться", callback_data=f"create_{activity.id}")
        # todo сделать поддерждку записи в команду если это командный турнир
        # signup = types.InlineKeyboardButton("Записаться в команду", callback_data=f"signup_{activity.id}")
        markup.add(create)

        await edit_with_ibuttons(call, f"{teams_text}", markup)
    except UnknownError as ue:
        print(ue)
        await edit_without_buttons(call, Msg.INTERNAL_ERROR.value)


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


@bot.callback_query_handler(func=lambda call: call.data.startswith("create_"))
async def enroll_player_in_activity(call: types.CallbackQuery) -> None:
    await bot.answer_callback_query(call.id)
    if await shono_fuse(call.message):
        return
    activity_id = int(call.data.split("_")[1])

    try:
        team = await activity_adapter.enroll_player_in_activity(activity_id, call.from_user.id)
        activity = await get_activity_by_id(activity_id)
        await select_activity(call, activity)

        # todo вариант для создания команды
        await msg_without_buttons(call.message, f"✅ Вы записались как {team.name}\n\n.")
    except PlayerAlreadyInTeam:
        await msg_without_buttons(call.message, "⚠️ Вы уже записаны.")
    except InsufficientRights:
        await edit_without_buttons(call, Msg.INSUFFICIENT_RIGHTS.value)
    except UnknownError:
        await edit_without_buttons(call, Msg.INTERNAL_ERROR.value)


@bot.callback_query_handler(func=lambda call: call.data.startswith("signup_"))
async def signup_to_activity(call: types.CallbackQuery) -> None:
    await bot.answer_callback_query(call.id)
    # TODO:
    await edit_without_buttons(call, "🚧 Функция записи в существующую команду находится в разработке. ")


def parse_message(msg: str) -> int:
    str1 = msg.split(", id: ")[1]
    return int(str1[:str1.find("]")])


async def change_message(mess: types.Message, answer: types.Message) -> None:
    await bot.edit_message_text(f"{mess.text}\n\nОтвечено: [username: {answer.from_user.username}, "
                                f"id: {answer.from_user.id}]", mess.chat.id, mess.id)


@bot.message_handler(content_types=["text"])
async def answer_to_buttons(mess: types.Message) -> None:
    if await shono_fuse(mess):
        return
    if mess.text == Buttons.TECHNICAL_SUPPORT.value[0]:
        await msg_without_buttons(mess, Msg.TECHNICAL_SUPPORT.value)
        log_info("User need help", mess)
        return
    if mess.reply_to_message is not None and mess.reply_to_message.text == Msg.TECHNICAL_SUPPORT.value:
        log_info(f"support_chat_id: {support_chat_id}, message_thread_id: {support_chat_thread_id}", mess)
        await bot.send_message(support_chat_id, f"[username: @{mess.from_user.username}, id: {mess.from_user.id}]"
                                                f"\n\n{mess.text}", message_thread_id=support_chat_thread_id)
        log_info("Message has been sent to support", mess)
        await msg_without_buttons(mess, f"Сообщение отправлено в техподдержку. Через некоторое время с Вами свяжутся.")
        return
    if mess.message_thread_id is not None and mess.message_thread_id == support_chat_thread_id:
        if mess.reply_to_message is not None:
            await bot.send_message(parse_message(mess.reply_to_message.text), mess.text)
            log_info("Message has been sent to user", mess)
            await change_message(mess.reply_to_message, mess)
            return
        return
    await msg_without_buttons(mess, "Я вас не понимаю. Используйте кнопки или команды.")

# asyncio.run(bot.polling(non_stop=True, none_stop=True))
