# coding: utf-8

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import json
import os
# import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - \
                        %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

# Global Variables
PREFIX = '#'  # constants are all caps
EPP = 5  # elements per page
CURSOR = 0  # points at the first element
SECTION = ''  # current section of user

# JSON files containing questions
with open('data/faq.json') as f:
    faq_data = json.load(f)
with open('data/links.json') as links:
    social_media = json.load(links)
with open('data/welcome.txt', 'r') as welcome_file:
    welcome_message = welcome_file.read()
# All hashtags:


def generate_hashtags():
    hashtag_list = []
    section_keys = list(faq_data.keys())

    for key in section_keys:
        hashtag_list += list(faq_data[key]["content"].items())

    hashtag_list += list(social_media.items())

    return hashtag_list


hashtag_list = generate_hashtags()

# --
# Functions used in FAQ
# --


def faq_index(x):
    foo = list(faq_data.keys())
    return foo[x: x+EPP]


def show_sections(bot, update, query, bool):

    keyboard = create_sections_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    if bool:
        bot.edit_message_text(
            'Please choose:',
            message_id=query.message.message_id,
            chat_id=query.message.chat_id,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    else:
        update.message.reply_text(
            "Please choose:", reply_markup=reply_markup, parse_mode="html")


def create_sections_keyboard():
    section_keys = list(faq_data.keys())
    keyboard = list(
        map(
            lambda x: [InlineKeyboardButton(
                faq_data[x]["label"], callback_data=x)],
            section_keys
        )
    )
    return keyboard


def show_questions(bot, query):
    global CURSOR
    questions = faq_data[SECTION]['content']
    question_keys = list(questions.keys())[CURSOR: CURSOR+EPP]

    keyboard = create_questions_keyboard(questions, question_keys)

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        'Please choose:',
        message_id=query.message.message_id,
        chat_id=query.message.chat_id,
        reply_markup=reply_markup,
        parse_mode='html')


def create_questions_keyboard(questions, question_keys):
    global faq_data, CURSOR, EPP

    keyboard = list(
        map(
            lambda x: [InlineKeyboardButton(
                questions[x]["label"], callback_data=x)],
            question_keys
        )
    )

    keyboard = [[
        InlineKeyboardButton("[ Back to Sections ]", callback_data="top")]] + keyboard

    if len(question_keys) + CURSOR == len(questions) and CURSOR == 0:
        pass

    elif CURSOR >= EPP and len(question_keys) + CURSOR == len(questions):
        keyboard += [[
            InlineKeyboardButton("< Previous", callback_data="prev")
        ]]

    elif CURSOR == 0 and len(question_keys) < len(questions):
        keyboard += [[InlineKeyboardButton("Next >", callback_data="next")]]
    else:
        keyboard += [[
            InlineKeyboardButton("< Previous", callback_data="prev"),
            InlineKeyboardButton("Next >", callback_data="next")
        ]]
    return keyboard


def show_answer(bot, query):
    question = faq_data[SECTION]['content'][query.data]['label']
    answer = faq_data[SECTION]['content'][query.data]['response']

    bot.edit_message_text(
        text="<b>" + question + "</b> \n" +
        answer +
        "\n[ <i>Reference this answer with</i> <code>#" + query.data
        + "</code> ]",
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        parse_mode='html')

# ---
# FAQ
# ---


def faq(bot, update):
    global CURSOR, EPP, SECTION
    query = update.callback_query

    # First call to function
    if not query:
        show_sections(bot, update, query, False)

    elif query.data.split("_")[0] == "section":
        SECTION = query.data
        show_questions(bot, query)

    elif query.data == "next":
        CURSOR += EPP
        show_questions(bot, query)

    elif query.data == "prev":
        CURSOR -= EPP
        show_questions(bot, query)

    elif query.data == "top":
        CURSOR = 0
        show_sections(bot, update, query, True)

    else:
        CURSOR = 0
        show_answer(bot, query)


# --
# Hashtag functionality
# --

def hashtag(bot, update):
    global PREFIX
    global hashtag_list

    input = update.message.text.lower()

    if input[0] != PREFIX:
        return
    else:
        answer = list(
            filter(
                lambda x: x[0] == input[1:], hashtag_list
            )
        )
        if len(answer) == 0:
            update.message.reply_text("Unrecognized # command.")
        else:
            if answer[0][0] in list(social_media.keys()):
                text = "<b>" + answer[0][1]['label'] + \
                    "</b> \n" + answer[0][1]['response']
            else:
                text = "<b>" + answer[0][1]['label'] + "</b> \n" + answer[0][1]['response'] + \
                    "\n[ <i>Reference this answer with</i> <code>#" + \
                    answer[0][1]['id'] + "</code> ]"
            update.message.reply_text(text=text, parse_mode="html")


# --
# Telegram app basic commands // recommended for most bots
# --
# Welcomes new users joining
def welcome(bot, update):
    first_name = update.message.new_chat_members[0].first_name

    # welcome_message.replace("__NAME__", input)
    formatted_welcome_message = welcome_message.format(name=first_name)

    update.message.reply_text(
        text=formatted_welcome_message, parse_mode="html")


def help(bot, update):
    # Basic commands
    help_text = "<b>Basic Commands:</b>\n"
    help_text += "<code>/help</code>: Lists all of the available commands.\n"
    # help_text += "<code>/start</code>: Greeting message.\n"
    help_text += "<code>/faq</code>: Brings up the frequently asked questions menu.\n"
    # social media links
    help_text += "<b>Links:</b>\n"
    for i in list(social_media.keys()):
        help_text += "<code>#" + i + "</code>\n"

    update.message.reply_text(help_text, parse_mode='html')


# --
# Error Catching
# --
def error(bot, update, error):
    logger.warning('Update "%s" cased error "%s"', update, error)


# --
# Starting the bot
# --
def main():
    api_key = os.environ['CODERBOT_API_KEY']

    updater = Updater(api_key)

    dp = updater.dispatcher

    # dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(
        MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(CommandHandler("faq", faq))
    dp.add_handler(CallbackQueryHandler(faq))
    dp.add_handler(MessageHandler(Filters.text, hashtag))
    # dp.add_handler(CallbackQueryHandler(button))

    # This goes last
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
