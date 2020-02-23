#!/usr/bin/env python
import logging
import random
import os
import subprocess
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    update.message.reply_text('Hi!')
    update.message.reply_text('see /help for available commands')


def saytext(update, context, msg):
    with open("cmd.sh", "w") as f:
        if msg[:5] == "/say ": msg = msg[5:]
        f.write('echo %s &> to_say.txt' % msg) # warning: this is vulnerable

    os.system('su bot -c "unshare --user -n timeout 3 bash cmd.sh"') 
    speak(update)

def help(update, context):
    update.message.reply_text('/pun - tell me a really, really funny joke\
            \n/say <text> - let me speak to you\
            \n/source - show me naked (nsfw)')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def pun(update, context):
    f = open("puns.txt", "r")
    lines = f.read().split('===')[:-1]
    update.message.reply_text(lines[random.randrange(len(lines))])

def speak(update):
    pitch = random.randrange(100)
    gender = random.choice(['f','m'])
    voice = random.choice(['1','2','3','4','5'])
    os.system("espeak -v {}{} -g 20 -p {} -f to_say.txt -w audio.wav".format(gender,voice,pitch))
    os.system("oggenc -q 8 audio.wav -o audio.ogg")
    with  open("./audio.ogg", "r") as f:
        update.message.reply_voice(voice=f)


def source(update):
    update.message.reply_text("Give me a moment please!")
    os.system("su bot -c 'cat telegram_bot.py > to_say.txt'")
    speak(update)


def say(update, context):
    update.message.reply_text("Here it comes!")
    saytext(update, context, str(update.message.text))


def commands(update, context):
    if update.message.text == "/pun": pun(update, context)
    if update.message.text.startswith("/say"): say(update, context)
    if update.message.text.startswith("/source"): source(update)


def main():
    updater = Updater("[apikey_redacted]", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.command, commands))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    main()
