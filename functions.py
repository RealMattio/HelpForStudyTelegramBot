from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from typing import Set
import os
import json
import random
import emoji

def scegli_materia(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Cybersecurity", callback_data='CS')],
        [InlineKeyboardButton("Innovazione e trasformazione digitale", callback_data='ITD')],
        [InlineKeyboardButton("Fondamenti di Intelligenza Artificiale", callback_data='FIA')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text="Scegli una materia da studiare", reply_markup=reply_markup)
