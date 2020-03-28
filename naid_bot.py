import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler,  CallbackQueryHandler)
from telegram import ParseMode

# internal imports
from text_templates import *
from bot_credentials_private import API_TOKEN, GROUP_CHAT_ID
from database_model import *
from markup import *

# ========================= DEV AREA == REMOVE ================================
# for develepment only
from pprint import pprint
import numpy as np

def show_all(update, context):
    """For develepment only."""
    pprint(update.to_dict())


# test call to post a test task quickly for demo and debug
demo_title = [
    "Einkaufen am Giesberg",
    "Dringende Besorgungen",
    "Toilettenpapier besorgen - eine Aufgabe auf Leben und Tod"
]
demo_descriprion = [
    "Persoenliche Informationen werden hier stehen",
    "Fam. Hertel braucht ganz dringend Esssen, kann aber nicht raus gehen.",
    "Das ist nur ein Test. Nichts wichtiges."
]
demo_location = [
    '<a href="https://www.google.de/maps/place/Unter+den+Linden+10+Berlin">Unter den Linden 10, Berlin</a>',
    '<a href="https://www.google.de/maps/place/Schultereck">Schultereck, Hamburg</a>',
    '<a href="https://www.google.de/maps/place/Marinenplatz+1+Muenchen">Marinenplatz 1, Muenchen</a>'
]
def command_test(update, context):

    with session_handler() as session:
        user = update.message.from_user
        client = session.query(User).filter(User.id == user.id).one_or_none()
        if client is None:

            # never seen this user before
            if update.message.chat.id == GROUP_CHAT_ID:
                # user is using group chat, add this user as client
                client = User(id = user.id, first_name = user.first_name, username = user.username)
                session.add(client)
                session.commit()
            else:
                # user is not using group chat, explain problem to user
                update.message.reply_text(
                    template_start_not_authorized,
                    parse_mode = ParseMode.HTML
                )
                return

        task = Task(
            title = demo_title[np.random.randint(3)],
            description = demo_descriprion[np.random.randint(3)],
            location = demo_location[np.random.randint(3)],
            client = client
        )
        session.add(task)
        session.flush()

        msg = context.bot.send_message(
            chat_id = GROUP_CHAT_ID,
            text = template_task_group_open.format(
                title = task.title,
                client_user_id = task.client.id,
                client_first_name = task.client.first_name
            ),
            reply_markup = markup_inline_keyboard_assign_task(task.id),
            parse_mode = ParseMode.HTML
        )
        task.message_id_post = msg.message_id
        task.status = "posted"
        session.commit()
# =============================================================================


# -----------------------------------------------------------------------------
# logging errors etc.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

    if context.error == "Forbidden: bot can't initiate conversation with a user":
        update.message.reply_text(
            template_cant_init_conversation.format(first_name = update.message.from_user.first_name),
            parse_mode = ParseMode.HTML
        )
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# simple reply commands
def command_help_start(update, context):
    """Send a message when the command /help or /start is issued."""
    context.bot.send_message(
        update.message.from_user.id,
        text = template_help_message,
        parse_mode = ParseMode.HTML
    )


def command_uebergabe(update, context):

    context.bot.send_message(
        update.message.from_user.id,
        text = template_help_uebergabe,
        parse_mode = ParseMode.HTML
    )


def command_bezahlung(update, context):

    context.bot.send_message(
        update.message.from_user.id,
        text = template_help_bezahlung,
        parse_mode = ParseMode.HTML
    )


def command_handschuhe(update, context):

    context.bot.send_message(
        update.message.from_user.id,
        text = template_help_handschuhe,
        parse_mode = ParseMode.HTML
    )


def command_maske(update, context):

    context.bot.send_message(
        update.message.from_user.id,
        text = template_help_maske,
        parse_mode = ParseMode.HTML
    )
# -----------------------------------------------------------------------------


# =============================================================================
# states for task recording conversation
RECORD_TITLE, RECORD_DESC, RECORD_LOCATION, SHOW_OVERVIEW = map(chr, range(4))

def command_aufgabe(update, context):
    """/aufgabe: Entry point for task recording."""

    user = update.message.from_user

    with session_handler() as session:

        client = session.query(User).filter(User.id == user.id).one_or_none()
        if client is None:

            # never seen this user before
            if update.message.chat.id == GROUP_CHAT_ID:
                # user is using group chat, add this user as client
                client = User(id = user.id, first_name = user.first_name, username = user.username)
                session.add(client)
                session.commit()
            else:
                # user is not using group chat, explain problem to user
                context.bot.send_message(
                    chat_id = user.id,
                    text = template_start_not_authorized,
                    parse_mode = ParseMode.HTML
                )
                return

    context.bot.send_message(
        chat_id = user.id,
        text = template_record_title,
        parse_mode = ParseMode.HTML,
        reply_markup = markup_inline_keyboard_cancel()
    )

    return RECORD_TITLE

def record_description(update, context):
    context.user_data["title"] = update.message.text
    update.message.reply_text(
        template_record_description,
        parse_mode = ParseMode.HTML,
        reply_markup = markup_inline_keyboard_cancel()
    )

    return RECORD_DESC

def record_location(update, context):
    context.user_data["description"] = update.message.text
    update.message.reply_text(
        template_record_location,
        parse_mode = ParseMode.HTML,
        reply_markup = markup_inline_keyboard_cancel()
    )

    return RECORD_LOCATION

def show_overview(update, context):

    location = update.message.text
    context.user_data["location"]  = '<a href="https://www.google.de/maps/place/{}">{}</a>'.format(
        "+".join(location.replace("\n", "").split()),
        location
    )

    update.message.reply_text(
        template_task_client_overview.format(**context.user_data),
        parse_mode = ParseMode.HTML,
        reply_markup = markup_inline_keyboard_confirm_overview()
    )

    return SHOW_OVERVIEW

def post_task(update, context):

    # store TASK to database
    task = Task(status = "posted", **context.user_data)
    user = update.callback_query.from_user
    with session_handler() as session:
        client = session.query(User).filter(User.id == user.id).one_or_none()
        task.client = client
        session.add(task)
        session.commit()

        # post task in group
        context.bot.send_message(
            chat_id = GROUP_CHAT_ID,
            text = template_task_group_open.format(
                title = task.title,
                client_user_id = task.client.id,
                client_first_name = task.client.first_name
            ),
            reply_markup = markup_inline_keyboard_assign_task(task.id),
            parse_mode = ParseMode.HTML
        )

    # reply to user
    update.callback_query.edit_message_text(
        template_task_client_overview.format(**context.user_data) + "<em>Verschickt</em>",
        parse_mode = ParseMode.HTML
    )
    context.user_data.clear()
    return ConversationHandler.END

def discard_task(update, context):

    # reply to user
    update.callback_query.edit_message_text(
        template_task_client_overview.format(**context.user_data) + "<em>Verworfen</em>",
        parse_mode = ParseMode.HTML,
    )

    context.user_data.clear()
    return ConversationHandler.END

def cancel_recording(update, context):

    update.callback_query.edit_message_text(
        "<em>Ok, vielleicht spaeter.</em>",
        parse_mode = ParseMode.HTML
    )

    return ConversationHandler.END
# =============================================================================


# =============================================================================
# ASSIGN TASK
def assign_task(update, context):

    task_id = int(update.callback_query.data.split("_")[1])
    user_id = update.callback_query.from_user.id

    with session_handler() as session:

        task = session.query(Task).filter(Task.id == task_id).one_or_none()
        if task is None:
            logger.error("in assign_task: Task with id {} not found in database.".format(task_id))
            return

        volunteer = session.query(User).filter(User.id == user_id).one_or_none()
        if volunteer is None:

            volunteer = User(
                id = user_id,
                first_name = update.callback_query.from_user.first_name,
                username = update.callback_query.from_user.username
            )
            session.add(volunteer)
            session.flush()

        task.volunteer = volunteer
        task.status = "assigned"
        session.commit()

        # update post
        update.callback_query.edit_message_text(
            template_task_group_processing.format(
                title = task.title,
                client_user_id = task.client.id,
                client_first_name = task.client.first_name,
                volunteer_first_name = volunteer.first_name
            ),
            parse_mode = ParseMode.HTML,
        )

        # message to volunteer
        msg = context.bot.send_message(
            chat_id = volunteer.id,
            text = template_task_client_confirm.format(
                title = task.title,
                volunteer_user_id = task.volunteer.id,
                volunteer_first_name = task.volunteer.first_name
            ),
            reply_markup = markup_inline_keyboard_confirm_task(),
            parse_mode = ParseMode.HTML
        )
        task.message_id_volunteer = msg.message_id
        session.commit()


def confirm_task(update, context):

    message_id = update.callback_query.message.message_id

    with session_handler() as session:

        task = session.query(Task).filter(Task.message_id_volunteer == message_id).one_or_none()
        if task is None:
            logger.error("in confirm_task: Task not found in database.")
            return

        # update volunteer message
        update.callback_query.edit_message_text(
            text = template_task_volunteer_confirmed_both.format(
                title = task.title,
                description = task.description,
                location = task.location,
                client_user_id = task.client.id,
                client_first_name = task.client.first_name
            ),
            reply_markup = markup_inline_keyboard_confirm_task_done(),
            parse_mode = ParseMode.HTML
        )
        task.status = "confirmed"
        session.commit()


def confirm_task_done(update, context):

    message_id = update.callback_query.message.message_id

    with session_handler() as session:

        task = session.query(Task).filter(Task.message_id_volunteer == message_id).one_or_none()
        if task is None:
            logger.error("Task not found in database. callback_query_confirm_overview()")
            return

        # update volunteer message
        update.callback_query.edit_message_text(
            text = template_task_volunteer_done.format(
                volunteer_first_name = task.volunteer.first_name
            ),
            parse_mode = ParseMode.HTML
        )
        task.status = "done"
        session.commit()

        # edit post message in group chat
        context.bot.edit_message_text(
            chat_id = GROUP_CHAT_ID,
            message_id = task.message_id_post,
            text = template_task_group_done.format(
                title = task.title,
                client_user_id = task.client.id,
                client_first_name = task.client.first_name,
                volunteer_first_name = task.volunteer.first_name
            ),
            parse_mode = ParseMode.HTML
        )


def reset_task(update, context):

    task_id = context.user_data["task_id"]
    message_id = context.user_data["message_id"]

    print(task_id, message_id)
    return ConversationHandler.END
# =============================================================================


# -----------------------------------------------------------------------------
# functions to keep track of group members
def group_chat(update, context):

    # check if user already in database
    user = update.message.from_user
    with session_handler() as session:

        db_user = session.query(User).filter(User.id == user.id).one_or_none()
        if db_user is None:
            db_user = User(id = user.id, first_name = user.first_name, username = user.username)
            session.add(db_user)
            session.commit()
            logger.info("{} added to databse.".format(db_user))


def status_update_new_members(update, context):

    with session_handler() as session:
        for user in update.message.new_chat_members:

            db_user = session.query(User).filter(User.id == user.id).one_or_none()
            if db_user is None:
                db_user = User(id = user.id, first_name = user.first_name, username = user.username)
                session.add(db_user)
                session.commit()
                logger.info("{} added to databse.".format(db_user))


def status_update_left_member(update, context):

    user = update.message.left_chat_member
    with session_handler() as session:

        db_user = session.query(User).filter(User.id == user.id).one_or_none()
        if db_user:
            session.delete(db_user)
            session.commit()
            logger.info("{} removed from databse.".format(db_user))
# -----------------------------------------------------------------------------


# =============================================================================
def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", command_help_start))
    dp.add_handler(CommandHandler("help", command_help_start))

    dp.add_handler(CommandHandler("uebergabe", command_uebergabe))
    dp.add_handler(CommandHandler("bezahlung", command_bezahlung))
    dp.add_handler(CommandHandler("handschuhe", command_handschuhe))
    dp.add_handler(CommandHandler("maske", command_maske))

    # for development
    dp.add_handler(CommandHandler("show", show_all))
    dp.add_handler(CommandHandler("test", command_test))

    # Conversation to record and post task
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('aufgabe', command_aufgabe)],
        states = {
            RECORD_TITLE:[
                MessageHandler(Filters.text, record_description)
            ],
            RECORD_DESC:[
                MessageHandler(Filters.text, record_location)
            ],
            RECORD_LOCATION:[
                MessageHandler(Filters.text, show_overview)
            ],
            SHOW_OVERVIEW:[
                CallbackQueryHandler(post_task, pattern='^post$'),
                CallbackQueryHandler(discard_task, pattern='^discard$')
            ]
        },
        fallbacks = [CallbackQueryHandler(cancel_recording, pattern='^cancel$')]
    )
    dp.add_handler(conv_handler)

    # assign tasks
    dp.add_handler(CallbackQueryHandler(assign_task, pattern='^assigntask'))
    dp.add_handler(CallbackQueryHandler(confirm_task, pattern='^confirmtask'))
    dp.add_handler(CallbackQueryHandler(confirm_task_done, pattern='^taskdone'))

    # keep track of users in group chat
    dp.add_handler(MessageHandler(Filters.group, group_chat))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, status_update_new_members))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, status_update_left_member))

    dp.add_handler(MessageHandler(Filters.all, show_all))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
