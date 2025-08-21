import datetime
import logging
import traceback
from enum import Enum

from telebot import types
from telebot.async_telebot import AsyncTeleBot

from lkshmatch.adapters.base import (
    Activity,
    ActivityAdapter,
    InsufficientRights,
    PlayerAdapter,
    PlayerAlreadyInTeam,
    PlayerNotFound,
    PlayerToRegister,
    SportAdapter,
    UnknownError,
    PlayerAlreadyRegistered,
)
from lkshmatch.config import settings
from lkshmatch.di import app_container
from lkshmatch.domain.repositories.student_repository import LKSHStudentsRepository


class Msg(Enum):
    REGISTRATION_USER_NOT_FOUND = (
        "😔 Извините, но вас нет в списках. Подойдите в 4-ый комповник."
    )
    REGISTRATION_CONFIRM_QUESTION = "🎉 %s, мы нашли вас. Это вы?"
    REGISTRATION_CONFIRMED = (
        "🍾 Вы зарегистрировались в системе.\n\n"
        + "✅ Для регистрации на активность, введите /register_on_sport."
    )
    REGISTRATION_ALREADY_REGISTERED = "🟢 Не переживайте, вы уже зарегистрированы."
    REGISTRATION_CANCELED = "❌ Регистрация отменена. Если хотите зарегистрироваться, подойдите в 4-ый комповник."

    INSUFFICIENT_RIGHTS = "У вас недостаточно прав для этого действия."
    INTERNAL_ERROR = (
        "Извините, что-то пошло не так. Обратитесь в 4-ый комповник к команде P."
    )

    TECHNICAL_SUPPORT = "Опишите свою проблему в ОТВЕТНОМ сообщении, мы постараемся оперативно ответить."


class Buttons(Enum):
    REGISTRATION_CONFIRM = ("✅ Подтверждаю", "reg_confirm")
    REGISTRATION_CANCEL = ("❌ Отмена регистрации", "reg_cancel")
    SPORTS_REGISTER_ON = ("Записаться на активность", "sports_register")
    TECHNICAL_SUPPORT = ("Написать в техподдержку.", "tech_sup")
    BACK_TO_SPORTS = ("⬅️ К выбору спорта", "back_to_sports")
    BACK_TO_ACTIVITIES = ("⬅️ К выбору активности", "back_to_activities")

    def __init__(self, text: str, callback_data: str):
        self.text = text
        self.callback_data = callback_data

    def inline(self) -> types.InlineKeyboardButton:
        return types.InlineKeyboardButton(
            text=self.text, callback_data=self.callback_data
        )

    def keyboard(self) -> types.KeyboardButton:
        return types.KeyboardButton(self.text)


activity_adapter = app_container.get(ActivityAdapter)
sport_adapter = app_container.get(SportAdapter)
player_adapter = app_container.get(PlayerAdapter)
students_repository = app_container.get(LKSHStudentsRepository)

logging.basicConfig(level=logging.INFO)

def get_required_param(param: str) -> str:
    try:
        answer = settings.get(param)
        if answer is None:
            raise ValueError(f"{param} required!")
        logging.info(f"{param}: {answer}")
    except Exception as e:
        logging.error(f"Error in gettin {param}: {e}")
        exit(1)
    return answer


token = get_required_param("TELEGRAM_TOKEN")
support_chat_id = int(get_required_param("SUPPORT_CHAT_ID"))
support_chat_thread_id = int(get_required_param("SUPPORT_CHAT_THREAD_ID"))

bot = AsyncTeleBot(token)


async def make_sports_buttons(with_back: bool = False) -> types.InlineKeyboardMarkup:
    buttons: list[types.InlineKeyboardButton] = []
    for sport in await sport_adapter.get_sport_list():
        button = types.InlineKeyboardButton(
            text=sport.ru_name.capitalize(), callback_data=f"sport_{sport.id}"
        )
        buttons.append(button)
    markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup() # type: ignore
    markup.add(*buttons, row_width=3)

    if with_back:
        markup.add(Buttons.SPORTS_REGISTER_ON.inline())

    return markup


async def make_sports_buttons_except_one(
    sport_id: int, new_text: str
) -> types.InlineKeyboardMarkup:
    buttons: list[types.InlineKeyboardButton] = []
    for sport in await sport_adapter.get_sport_list():
        button = types.InlineKeyboardButton(
            text=sport.ru_name.capitalize() if sport_id != sport.id else new_text,
            callback_data=f"sport_{sport.id}",
        )
        buttons.append(button)
    markup = types.InlineKeyboardMarkup() # type: ignore
    return markup.add(*buttons, row_width=3)


async def make_activity_buttons(
    activities: list[Activity],
        sport_id: int | None = None,
) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup() # type: ignore
    for activity in activities:
        button = types.InlineKeyboardButton(
            text=activity.title, callback_data=f"activity_{activity.id}"
        )
        markup.add(button)

    if sport_id is not None:
        back_button = Buttons.BACK_TO_SPORTS.inline()
        markup.add(back_button)
    
    return markup


async def make_choose_registration_buttons() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup() # type: ignore
    confirm_btn = Buttons.REGISTRATION_CONFIRM.inline()
    cancel_btn = Buttons.REGISTRATION_CANCEL.inline()
    markup.add(confirm_btn, cancel_btn)
    return markup


async def make_activity_detail_buttons(
        activity: Activity,
        list_of_all_teams: list,
        chat_id: int,
        sport_id: int | None = None
) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()  # type: ignore

    if any(team.captain.tg_id == chat_id for team in list_of_all_teams):
        leave_button = types.InlineKeyboardButton(
            "❌ Отписаться", callback_data=f"leave_{activity.id}"
        )
        markup.add(leave_button)
    else:
        create_button = types.InlineKeyboardButton(
            "✅ Записаться", callback_data=f"create_{activity.id}"
        )
        markup.add(create_button)

    if sport_id is not None:
        activities = await activity_adapter.get_activities_by_sport_section(sport_id)
        if len(activities) > 1:
            back_button = types.InlineKeyboardButton(
                "⬅️ К выбору активности",
                callback_data=f"back_to_activities_{sport_id}"
            )
        else:
            back_button = Buttons.BACK_TO_SPORTS.inline()
        markup.add(back_button)

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


async def msg_with_ibuttons(
    mess: types.Message, text: str, buttons: types.InlineKeyboardMarkup
) -> types.Message:
    return await bot.send_message(chat_id=mess.chat.id, text=text, reply_markup=buttons)


async def msg_with_buttons(
    mess: types.Message, text: str, buttons: types.ReplyKeyboardMarkup
) -> types.Message:
    return await bot.send_message(chat_id=mess.chat.id, text=text, reply_markup=buttons)


async def msg_without_buttons(mess: types.Message, text: str) -> types.Message:
    return await bot.send_message(
        chat_id=mess.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove()
    )


async def edit_with_ibuttons(
    call: types.CallbackQuery, text: str, buttons: types.InlineKeyboardMarkup
) -> types.Message:
    return await bot.edit_message_text( # type: ignore
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=buttons,
    )


async def edit_without_buttons(call: types.CallbackQuery, text: str) -> None:
    await bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id, text=text
    )


async def validate_user(mess: types.Message) -> tuple[int | None, str | None]:
    if mess.from_user is None:
        await msg_without_buttons(mess, Msg.INTERNAL_ERROR.value)
        log_warning("Fail to acquire from_user (is None)", mess)
        return None, None
    if mess.from_user.id is None or mess.from_user.username is None:
        await msg_without_buttons(mess, Msg.INTERNAL_ERROR.value)
        log_info("User hasn't got username or tg_id", mess)
        return None, None
    return mess.from_user.id, mess.from_user.username


def log_text(text: str, mess: types.Message | types.InaccessibleMessage) -> str:
    match mess:
        case types.Message(from_user=user, date=date) if user is not None:
            username = f"@{user.username}" if user.username else "<no username>"
            return (
                text + f" [username: {username}, tg_id: {user.id},"
                f" time: {datetime.datetime.fromtimestamp(date)}]"
            )
        case types.InaccessibleMessage(date=date):
            return (
                text
                + f" [inaccessible message, time: {datetime.datetime.fromtimestamp(date)}]"
            )
        case _:
            return text + " [unknown message type]"


def log_info(text: str, mess: types.Message | types.InaccessibleMessage) -> None:
    logging.info(log_text(text, mess))


def log_warning(
    text: str, mess: types.Message | types.InaccessibleMessage
) -> None:
    logging.warning(log_text(text, mess))


def log_error(text: str, mess: types.Message | types.InaccessibleMessage) -> None:
    logging.error(log_text(text, mess))

@bot.message_handler(commands=["start"]) # type: ignore
async def start(mess: types.Message) -> None:
    log_info("Called /start.", mess)
    user_id, username = await validate_user(mess)
    if user_id is None:
        return
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.add(types.KeyboardButton(Buttons.TECHNICAL_SUPPORT.text))
        await msg_with_buttons(mess, "Здравствуйте!", markup)
        user_name = await students_repository.get_name_by_username(username)
        await msg_with_ibuttons(
            mess=mess,
            text=Msg.REGISTRATION_CONFIRM_QUESTION.value % user_name,
            buttons=await make_choose_registration_buttons(),
        )
    except PlayerNotFound:
        log_warning("User not found in lksh database. Validate failed.", mess)
        await msg_without_buttons(mess, Msg.REGISTRATION_USER_NOT_FOUND.value)
    except UnknownError as ue:
        log_error(f"Internal error: {ue}. Validate failed.", mess)
        logging.error(f"Full stack trace for UnknownError:\n{traceback.format_exc()}")
        await msg_without_buttons(mess, Msg.INTERNAL_ERROR.value)
    log_info("Finished /start successfully.", mess)


@bot.callback_query_handler(
    func=lambda call: call.data
    in [
        Buttons.REGISTRATION_CONFIRM.callback_data,
        Buttons.REGISTRATION_CANCEL.callback_data,
    ]
) # type: ignore
async def processing_of_registration(call: types.CallbackQuery) -> None:
    await bot.answer_callback_query(call.id)
    if call.data == Buttons.REGISTRATION_CONFIRM.callback_data:
        log_info("Registration accepted.", call.message)
        user_id, username = call.from_user.id, call.from_user.username
        if user_id is None or username is None:
            await edit_without_buttons(call, Msg.INTERNAL_ERROR.value)
            return

        sport_markup = types.InlineKeyboardMarkup() # type: ignore
        sport_btn = Buttons.SPORTS_REGISTER_ON.inline()
        sport_markup.add(sport_btn)

        try:
            user_name = await students_repository.get_name_by_username(username)
            await player_adapter.register_user(
                PlayerToRegister(
                    tg_id=user_id,
                    tg_username=username,
                    name=user_name
                )
            )

            to_pin = (await edit_with_ibuttons(call, Msg.REGISTRATION_CONFIRMED.value, sport_markup)).message_id
            await bot.pin_chat_message(call.message.chat.id, to_pin)
        except PlayerNotFound:
            log_warning(
                "User not found in lksh database. Validate failed.", call.message
            )
            await edit_without_buttons(call, Msg.REGISTRATION_USER_NOT_FOUND.value)
        except PlayerAlreadyRegistered:
            log_warning("User already registered.", call.message)
            await edit_with_ibuttons(
                call, Msg.REGISTRATION_ALREADY_REGISTERED.value, sport_markup
            )
        except UnknownError as ue:
            log_error(f"Internal error: {ue}. Validate failed.", call.message)
            logging.error(f"Full stack trace for UnknownError:\n{traceback.format_exc()}")
            await edit_without_buttons(call, Msg.INTERNAL_ERROR.value)
    elif call.data == Buttons.REGISTRATION_CANCEL.callback_data:
        await edit_without_buttons(call, Msg.REGISTRATION_CANCELED.value)


@bot.message_handler(commands=["register_on_sport"])  # type: ignore
async def register_on_sport(mess: types.Message) -> None:
    log_info("Called /register_on_sport.", mess)
    await msg_with_ibuttons(
        mess=mess,
        text="Выберите спортивную секцию.",
        buttons=await make_sports_buttons()
    )
    # await bot.pin_chat_message(mess.chat.id, to_pin)
    log_info("Finished /register_on_sport successfully.", mess)


@bot.callback_query_handler(
    func=lambda call: call.data == Buttons.SPORTS_REGISTER_ON.callback_data
)  # type: ignore
async def handle_sport_register_callback(call: types.CallbackQuery) -> None:
    log_info("Called handle_sport_register_callback.", call.message)
    await bot.answer_callback_query(call.id)
    markup = await make_sports_buttons()
    await edit_with_ibuttons(call, "Выберите спортивную секцию:", markup)  # type: ignore
    log_info("Finished handle_sport_register_callback successfully.", call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith("sport_")) # type: ignore
async def select_sport(call: types.CallbackQuery) -> None:
    log_info("Called select_sport.", call.message)
    await bot.answer_callback_query(call.id)
    sport_id = int(call.data.split("_")[1])  # type: ignore
    for s in await sport_adapter.get_sport_list():
        if s.id == sport_id:
            activities = await activity_adapter.get_activities_by_sport_section(sport_id)

            if len(activities) == 0:
                markup = await make_sports_buttons_except_one(sport_id, "💤 ПУСТО")
                await edit_with_ibuttons(call, "Выберите спортивную секцию:", markup)
                log_info("Finished select_sport (no activities).", call.message)
                return
            if len(activities) == 1:
                await select_activity(call, activities[0], sport_id)
                log_info("Finished select_sport (single activity).", call.message)
                return

            markup = await make_activity_buttons(activities, sport_id)
            await edit_with_ibuttons(call, "Для выбора события, нажмите кнопку.", markup)
            log_info("Finished select_sport (multiple activities).", call.message)
            return
    log_warning("Sport section not found.", call.message)
    await edit_without_buttons(call, "Спортивная секция не найдена.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("activity_")) # type: ignore
async def processing_select_activity(call: types.CallbackQuery) -> None:
    log_info("Called processing_select_activity.", call.message)
    await bot.answer_callback_query(call.id)
    activity_id = int(call.data.split("_")[1])  # type: ignore
    activity = await activity_adapter.get_activity_by_id(activity_id)
    if not activity:
        log_warning("Activity not found.", call.message)
        await edit_without_buttons(call, "Активность не найдена.")
        return

    await select_activity(call, activity, activity.sport_section_id)
    log_info("Finished processing_select_activity successfully.", call.message)


async def select_activity(call: types.CallbackQuery, activity: Activity, sport_id: int | None = None) -> None:
    try:
        list_of_all_teams = await activity_adapter.get_teams_by_activity_id(activity.id)
        description = f"ℹ️ Описание: {activity.description}\n\n" if activity.description else ""

        if list_of_all_teams:
            numbered_teams = [f"{i + 1}. {team.name}" for i, team in enumerate(list_of_all_teams)]
            # todo сделать поддержку команда/участник
            teams_text = f"🏆 {activity.title}\n\n{description}📋 Список участников:\n\n" + "\n".join(numbered_teams)
        else:
            teams_text = f"🏆 {activity.title}\n\n{description}📋 Пока нет участников."

        markup = await make_activity_detail_buttons(
            activity=activity,
            list_of_all_teams=list_of_all_teams,
            chat_id=call.message.chat.id,
            sport_id=sport_id
        )

        await edit_with_ibuttons(call, f"{teams_text}", markup)
    except UnknownError as ue:
        log_error(str(ue), call.message)
        logging.error(f"Full stack trace for UnknownError:\n{traceback.format_exc()}")
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


@bot.callback_query_handler(func=lambda call: call.data.startswith("create_")) # type: ignore
async def enroll_player_in_activity(call: types.CallbackQuery) -> None:
    log_info("Called enroll_player_in_activity.", call.message)
    await bot.answer_callback_query(call.id)
    activity_id = int(call.data.split("_")[1])  # type: ignore

    try:
        player = await player_adapter.get_player_by_tg(tg_id=call.from_user.id)
        team = await activity_adapter.enroll_player_in_activity(activity_id, player.core_id)
        activity = await activity_adapter.get_activity_by_id(activity_id)
        if activity is None:
            log_error(
                f"Couldn't find activity by activity id received from ActivityAdapter (activity_id: {activity_id})",
                call.message,
            )
        await select_activity(call, activity, activity.sport_section_id)

        # todo вариант для создания команды
        await msg_without_buttons(
            # TODO: fix types
            call.message, # type: ignore
            f"✅ Вы записались как {team.name}.",
        )
        log_info("Finished enroll_player_in_activity successfully.", call.message)
    except PlayerAlreadyInTeam:
        log_warning("Player already in team.", call.message)
        await msg_without_buttons(call.message, "⚠️ Вы уже записаны.")  # type: ignore
    except InsufficientRights:
        log_warning("Insufficient rights for enrollment.", call.message)
        await edit_without_buttons(call, Msg.INSUFFICIENT_RIGHTS.value)
    except UnknownError as ue:
        log_error(f"UnknownError in enroll_player_in_activity: {ue}", call.message)
        logging.error(f"Full stack trace for UnknownError:\n{traceback.format_exc()}")
        await edit_without_buttons(call, Msg.INTERNAL_ERROR.value)


@bot.callback_query_handler(func=lambda call: call.data.startswith("leave_"))  # type: ignore
async def leave_player_from_activity(call: types.CallbackQuery) -> None:
    log_info("Called leave_player_from_activity.", call.message)
    await bot.answer_callback_query(call.id)
    activity_id = int(call.data.split("_")[1])  # type: ignore

    try:
        player = await player_adapter.get_player_by_tg(tg_id=call.from_user.id)
        await activity_adapter.leave_player_by_activity(activity_id, player.core_id)
        activity = await activity_adapter.get_activity_by_id(activity_id)
        if activity is None:
            log_error(
                f"Couldn't find activity by activity id received from ActivityAdapter (activity_id: {activity_id})",
                call.message,
            )
        await select_activity(call, activity, activity.sport_section_id)

        await msg_without_buttons(
            call.message,  # type: ignore
            "✅ Вы успешно отписались от активности.",
        )
        log_info("Finished leave_player_from_activity successfully.", call.message)
    except InsufficientRights:
        log_warning("Insufficient rights for leaving activity.", call.message)
        await edit_without_buttons(call, Msg.INSUFFICIENT_RIGHTS.value)
    except UnknownError as ue:
        log_error(f"UnknownError in leave_player_from_activity: {ue}", call.message)
        logging.error(f"Full stack trace for UnknownError:\n{traceback.format_exc()}")
        await edit_without_buttons(call, Msg.INTERNAL_ERROR.value)


@bot.callback_query_handler(func=lambda call: call.data.startswith("signup_")) # type: ignore
async def signup_to_activity(call: types.CallbackQuery) -> None:
    log_info("Called signup_to_activity.", call.message)
    await bot.answer_callback_query(call.id)
    await edit_without_buttons(call, "🚧 Функция записи в существующую команду находится в разработке. ")
    log_info("Finished signup_to_activity (feature in development).", call.message)


@bot.callback_query_handler(func=lambda call: call.data == Buttons.BACK_TO_SPORTS.callback_data)  # type: ignore
async def back_to_sports(call: types.CallbackQuery) -> None:
    log_info("Called back_to_sports.", call.message)
    await bot.answer_callback_query(call.id)
    markup = await make_sports_buttons()
    await edit_with_ibuttons(call, "Выберите спортивную секцию:", markup)
    log_info("Finished back_to_sports successfully.", call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith("back_to_activities_"))  # type: ignore
async def back_to_activities(call: types.CallbackQuery) -> None:
    log_info("Called back_to_activities.", call.message)
    await bot.answer_callback_query(call.id)
    sport_id = int(call.data.split("_")[3])  # back_to_activities_{sport_id}
    activities = await activity_adapter.get_activities_by_sport_section(sport_id)
    markup = await make_activity_buttons(activities, sport_id)
    await edit_with_ibuttons(call, "Для выбора события, нажмите кнопку.", markup)
    log_info("Finished back_to_activities successfully.", call.message)


def get_id_from_support_message(msg: str) -> int:
    str1 = msg.split(", id: ")[1]
    return int(str1[:str1.find("]")])


async def change_support_message(mess: types.Message, answer: types.Message) -> None:
    await bot.edit_message_text(f"{mess.text}\n\nОтвечено: [username: {answer.from_user.username}, " # type: ignore
                                f"id: {answer.from_user.id}]", mess.chat.id, mess.id) # type: ignore


async def notify_person(tg_id: int, text: str) -> None:
    await bot.send_message(tg_id, text)


@bot.message_handler(content_types=["text"]) # type: ignore
async def answer_to_buttons(mess: types.Message) -> None:
    if mess.text == Buttons.TECHNICAL_SUPPORT.text:
        await msg_without_buttons(mess, Msg.TECHNICAL_SUPPORT.value)
        log_info("User need help", mess)
        return
    if mess.reply_to_message is not None and mess.reply_to_message.text == Msg.TECHNICAL_SUPPORT.value:
        log_info(f"support_chat_id: {support_chat_id}, message_thread_id: {support_chat_thread_id}", mess)
        await bot.send_message(support_chat_id, f"[username: @{mess.from_user.username}, id: {mess.from_user.id}]" # type: ignore
                                                f"\n\n{mess.text}", message_thread_id=support_chat_thread_id)
        log_info("Message has been sent to support", mess)
        await msg_without_buttons(mess, "Сообщение отправлено в техподдержку. Через некоторое время с Вами свяжутся.")
        return
    if mess.message_thread_id is not None and mess.message_thread_id == support_chat_thread_id:
        if mess.reply_to_message is not None:
            await bot.send_message(get_id_from_support_message(mess.reply_to_message.text), mess.text) # type: ignore
            log_info("Message has been sent to user", mess)
            await change_support_message(mess.reply_to_message, mess)
            return
    await msg_without_buttons(mess, "Я вас не понимаю. Используйте кнопки или команды.")
