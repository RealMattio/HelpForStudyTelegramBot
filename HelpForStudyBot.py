from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from typing import Set
import os
import json
import random
import emoji

USERS_FILE = 'users.json'
NICKNAMES_FILE = 'nicknames.json'
#read bot token from file
with open('token_file.txt', 'r') as f:
    BOT_TOKEN = f.readlines()[0]

QUESTIONS = []
# Read the question file

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
    update.message.reply_text(f'Ciao {update.message.from_user.username}! Sono il bot che ti aiuterà a preparare gli esami.\n'
                                '\nUsa il comando /iniziaStudio per scegliere una materia e iniziare a studiare.\n'
                                '\nEcco cosa posso fare per te:\n'
                                '   - Posso farti delle domande delle materie di cui ho conoscienza. Non devi rispondermi ma devi rispondere ripetendo a voce alta cercando di migliorarti\n'
                                '   - Posso fornirti delle flashcards con un argomento e delle parole chiave per aiutarti a ripetere\n'
                                'Usa il comando /cosapuoifare se vuoi che ti ridica cosa posso fare per te\n'
                                'Usa il comando /info per maggiori informazioni.\n'
                                f'\nBuono studio {emoji.emojize(':smiling_face_with_sunglasses:')}')

def echo(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    users.add(chat_id)
    save_users(users)
    update.message.reply_text("Mi dispiace, non ho capito cosa vuoi dire. Usa il comando /iniziaStudio per iniziare a studiare.")


def choose_subject(update: Update, context: CallbackContext) -> None:
    global QUESTIONS
    # add a button to this keyboard if you want to add a subject to study
    keyboard = [
        [InlineKeyboardButton("Cybersecurity", callback_data='CS')],
        [InlineKeyboardButton("Innovazione e trasformazione digitale", callback_data='ITD')],
        [InlineKeyboardButton("Fondamenti di Intelligenza Artificiale", callback_data='FIA')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        update.callback_query.edit_message_text(text="Scegli una materia da studiare", reply_markup=reply_markup)
    else:
        update.message.reply_text(text="Scegli una materia da studiare", reply_markup=reply_markup)

def set_subject(update: Update, sub:str) -> None:
    global QUESTIONS
    # add subject code to this if statement specifing the path where the .txt with questions is if you want to add a subject to this bot
    if sub == 'CS':
        #change the path where the questions are stored   
        with open('data/domande_cybersecurity_it.txt', 'r', encoding='utf-8') as f:
            QUESTIONS = f.read().splitlines()
            choose_mode(update)
    elif sub == 'ITD':    
        with open('data/domande_itd_it.txt', 'r', encoding='utf-8') as f:
            QUESTIONS = f.read().splitlines()
            choose_mode(update)
    elif sub == 'FIA':    
        with open('data/domande_fia_it.txt', 'r', encoding='utf-8') as f:
            QUESTIONS = f.read().splitlines()
            choose_mode(update)

def choose_mode(update: Update) -> None:
    keyboard = [
        [InlineKeyboardButton("Domande", callback_data='question')],
        [InlineKeyboardButton("Flashcards", callback_data='flashcard')],
        [InlineKeyboardButton("Cambia materia", callback_data='change_sub')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    #if the function is called by a callback query, edit the message else reply with a new message
    if update.callback_query:
        update.callback_query.edit_message_text(text="Scegli una modalità di studio", reply_markup=reply_markup)
    else:
        update.message.reply_text(text="Scegli una modalità di studio", reply_markup=reply_markup)
    

def button(update: Update, context: CallbackContext) -> None:
    global QUESTIONS
    query = update.callback_query
    query.answer()
    if QUESTIONS == [] and query.data != 'CS' and query.data != 'ITD' and query.data != 'FIA':    
        choose_subject(update, context)
    #add subject in this elif when you wnat to add a subject to your bot
    elif query.data == 'CS' or query.data == 'ITD' or query.data == 'FIA':
        set_subject(update, query.data)
    elif query.data == 'question':
        get_question(update, query)
    elif query.data == 'flashcard':
        get_flashcard(update, query)
    elif query.data == 'choose_mode':
        choose_mode(update)
    elif query.data == 'change_sub':
        choose_subject(update, context)
    else:    
        query.edit_message_text(text=f"Selected option: {query.data}")
        

def get_question(update: Update, query) -> None:
    question = random.choice(QUESTIONS)
    keyboard_question = [
        [InlineKeyboardButton("Nuova domanda", callback_data='question')],
        [InlineKeyboardButton("Indietro", callback_data='choose_mode')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard_question)
    query.edit_message_text(text=question, reply_markup= reply_markup)

def get_flashcard(update: Update, query) -> None:
    # send a message to the user
    keyboard_question = [
        [InlineKeyboardButton("Indietro", callback_data='choose_mode')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard_question)
    query.edit_message_text(text=f"Mi dispiace le flashcard ancora non sono state implementate! {emoji.emojize(':slightly_frowning_face:')}", reply_markup= reply_markup)

def whatcanudo(update: Update, context: CallbackContext):
    update.message.reply_text('Usa il comando /iniziaStudio per scegliere una materia e iniziare a studiare.\n'
                                '\nEcco cosa posso fare per te:\n'
                                '   - Posso farti delle domande delle materie di cui ho conoscienza. Non devi rispondermi ma devi rispondere ripetendo a voce alta cercando di migliorarti\n'
                                '   - Posso fornirti delle flashcards con un argomento e delle parole chiave per aiutarti a ripetere\n'
                                'Usa il comando /cosapuoifare se vuoi che ti ridica cosa posso fare per te\n'
                                'Usa il comando /info per maggiori informazioni.\n'
                                f'\nBuono studio {emoji.emojize(':smiling_face_with_sunglasses:')}')

def info(update: Update, context: CallbackContext):
    update.message.reply_text('Bot realizzato da @RealMattio\nSe ci sono errori nelle domande o vuoi contribuire aggiungendone tu alcune contattalo quì su Telegram.')

def main():
    # Replace 'BOT_TOKEN' with your bot's token
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handler for the /start command
    dp.add_handler(CommandHandler("start", start))

    # Add message handler for each possible command
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(CommandHandler("iniziaStudio", choose_subject))
    dp.add_handler(CommandHandler("cosapuoifare", whatcanudo))
    dp.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()