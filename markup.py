from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

# -----------------------------------------------------------------------------
# unspecific markups
def markup_inline_keyboard_yes_no():
    buttons = [[
        InlineKeyboardButton(text="Ja", callback_data=role + "yes"),
        InlineKeyboardButton(text="Nein", callback_data=role + "no")
    ]]
    return InlineKeyboardMarkup(buttons, one_time_keyboard=True)


def markup_inline_keyboard_cancel():
    buttons = [[
        InlineKeyboardButton(text="Abbrechen", callback_data="cancel")
    ]]
    return InlineKeyboardMarkup(buttons, one_time_keyboard=True)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# specific markups for task recording
def markup_inline_keyboard_confirm_overview():
    buttons = [[
        InlineKeyboardButton(text="Abschicken", callback_data="post"),
        InlineKeyboardButton(text="Verwerfen", callback_data="discard")
    ]]
    return InlineKeyboardMarkup(buttons, one_time_keyboard=True)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# specific markups for task assignment
def markup_inline_keyboard_assign_task(task_id):
    buttons = [[
        InlineKeyboardButton(text="Helfen", callback_data="assigntask_{}".format(task_id))
    ]]
    return InlineKeyboardMarkup(buttons, one_time_keyboard=True)


def markup_inline_keyboard_confirm_task():
    buttons = [[
        InlineKeyboardButton(text="Ja, ich bin mir sicher.", callback_data="confirmtask_1"),
        InlineKeyboardButton(text="Nein, doch nicht.", callback_data="confirmtask_0")
    ]]
    return InlineKeyboardMarkup(buttons, one_time_keyboard=True)


def markup_inline_keyboard_confirm_task_done():
    buttons = [[
        InlineKeyboardButton(text="Erledigt", callback_data="taskdone_1"),
        InlineKeyboardButton(text="Nochmal in der Gruppe anbieten.", callback_data="taskdone_0")
    ]]
    return InlineKeyboardMarkup(buttons, one_time_keyboard=True)
# -----------------------------------------------------------------------------
