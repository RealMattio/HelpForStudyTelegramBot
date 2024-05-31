#brodcast inviare messaggio a tutti gli utenti che hanno interagito con il bot
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from typing import Set
import os
import json
import random

USERS_FILE = 'users.json'
NICKNAMES_FILE = 'nicknames.json'
#read bot token from file
with open('token_file.txt', 'r') as f:
    BOT_TOKEN = f.readlines()

# Read the question file
with open('data/domande_cybersecurity_it.txt', 'r', encoding='utf-8') as f:
    questions = f.read().splitlines()

# Load the set of users who have ever interacted with the bot
def load_users() -> Set[int]:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return set(json.load(f))
    return set()

# Load the set of the nicknames who have ever interacted with the bot
def load_nicknames() -> list:
    if os.path.exists(NICKNAMES_FILE):
        with open(NICKNAMES_FILE, 'r') as f:
            return json.load(f)
    return list()

# Save the set of users who have ever interacted with the bot
def save_users(users: Set[int]) -> None:
    with open(USERS_FILE, 'w') as f:
        json.dump(list(users), f)

# Save the set of nicknames who have ever interacted with the bot
def save_nicknames(nicknames: list) -> None:
    with open(NICKNAMES_FILE, 'w') as f:
        json.dump(nicknames, f)


users = load_users()
nicknames = load_nicknames()


def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    users.add(chat_id)
    if update.message.from_user.username not in [people['nickname'] for people in nicknames]:
        nicknames.append({'chat_id':chat_id, 'nickname':update.message.from_user.username})
        save_nicknames(nicknames)
    save_users(users)
    update.message.reply_text(f'Ciao {update.message.from_user.username}! Sono il bot che ti aiuterà a preparare l\'esame di Cybersecurity.\nUsa il comando /iniziaStudio per iniziare a studiare.')


def echo(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    users.add(chat_id)
    save_users(users)
    update.message.reply_text("Mi dispiace, non ho capito cosa vuoi dire. Usa il comando /iniziaStudio per iniziare a studiare.")


def scegli(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Domande", callback_data='question')],
        [InlineKeyboardButton("Flashcards", callback_data='flashcard')]
        #[InlineKeyboardButton("Option 3", callback_data='opzione 3')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text('Scegli cosa vuoi:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'question':
        get_question(update, query)
    elif query.data == 'flashcard':
        get_flashcard(update, query)
    elif query.data == 'scegli':
        scegli(update, context)
    else:    
        query.edit_message_text(text=f"Selected option: {query.data}")

def get_question(update: Update, query) -> None:
    question = random.choice(questions)
    keyboard_question = [
        [InlineKeyboardButton("Nuova domanda", callback_data='question')],
        [InlineKeyboardButton("Indietro", callback_data='scegli')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard_question)
    query.edit_message_text(text=question, reply_markup= reply_markup)

def get_flashcard(update: Update, query) -> None:
    # send a message to the user
    query.edit_message_text(text="Flashcard mode is not implemented yet. Sorry :( ")


def main():
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your bot's token
    
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    # Add command handler for the /start command
    dp.add_handler(CommandHandler("start", start))

    # Add message handler for echo functionality
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dp.add_handler(CommandHandler("iniziaStudio", scegli))

    dp.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()