# coding=utf-8
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
from messages import Message
from datetime import date
from datetime import datetime
from datetime import timedelta
import logging
import feedparser
import re
import os
import dotenv

dotenv.load_dotenv()

updater = Updater(
    token=os.environ['TELEGRAM_BOT_KEY'],
    use_context=True
)

feed_url = os.environ['DPS_DO_CAFE_FEED_URL'] 

dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Este é o bot do Depois do Café, com ele você pode ouvir os nossos episódios exclusivos."
    )


def welcome_message(update, context):
    username = update.effective_user.username
    today = str(date.today())

    if not username:
        return
     
    message = Message(os.path.dirname(os.path.realpath('__file__')) + '/goodmorning_user.json')

    json = message.read_file()

    if True == message.verify_exists(username, today):
        return

    message.add_message(username, today)

    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Opa, tudo certo @{}? Como tá o seu dia?".format(username)
    )

def episodes(update, context):
    prevent_spam()
    episodes = ''
    count = 0
    feed = feedparser.parse(feed_url)

    for entry in feed['entries']:

        count += 1
        episodes += "#{} - {}\n".format(count, entry.title)

    episodes += "\n\n----------------------"
    episodes += "\nPara ouvir algum episódio use o comando como o exemplo: /ouvir_episodio #1"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=episodes
    )


def listen_episode(update, context):
    prevent_spam()
    text = ' '.join(context.args)

    if not re.search('#\d+', text):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Opa, mas você precisa passar o numero do episodio pra gente. /ouvir_episodio #1 por exemplo'
        )
        return

    episode_number = int(re.findall('#(\d+)', text)[0]) - 1
    episodes = []
    feed = feedparser.parse(feed_url)

    for entry in feed['entries']:

        episodes.append({
            'link': entry.link,
        })

    try: 
        context.bot.send_audio(
            chat_id=update.effective_chat.id,
            audio=episodes[episode_number]['link']
        )
    except IndexError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Nao temos o episodio {}, para saber quais episodios temos aqui use o comando /episodios'.format(text)
        )
        return


def feed(update, context):
    prevent_spam()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=feed_url
    )

def prevent_spam():
    message = Message(os.path.dirname(os.path.realpath('__file__')) + '/prevent_spam.json')
    json = message.read_file()

    try:
        last_command = datetime.strptime(json['command'][0], "%Y-%m-%d %H:%M:%S.%f") + timedelta(minutes=5)

        if last_command > datetime.now():
            raise RuntimeError("MUITA MENSAGEM")   
        
        message.re_write('command', str(datetime.now()))

    except KeyError:
        message.re_write('command', str(datetime.now()))

def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Desculpa mas não estamos sintonizados neste comando."
    )

welcome_message_handler = MessageHandler(Filters.text & (~Filters.command), welcome_message)
start_handler = CommandHandler('start', start)
episodes_handler = CommandHandler('episodios', episodes)
listen_episode_handler = CommandHandler('ouvir_episodio', listen_episode)
feed_url_handler = CommandHandler('feed', feed)
unknown_handler = MessageHandler(Filters.command, unknown)


dispatcher.add_handler(welcome_message_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(episodes_handler)
dispatcher.add_handler(listen_episode_handler)
dispatcher.add_handler(feed_url_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
