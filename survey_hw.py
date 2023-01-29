import logging
import pymysql
# from dotenv import load_dotenv
import os

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

import time

# Connect database with chatbot and move on to chatbot database
# db = pymysql.connect(host="localhost", user="root", charset="utf8")
# cursor = db.cursor()
# cursor.execute('USE chatbot;')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def intro (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(
        chat_id=update.message.chat.id, text="안녕! 난 방금 너와 함께 문제를 푼 하랑이야👋🏻 지금까지 나한테 설명해주느라 고생 많았어!"
    )

    await context.bot.send_message(
        chat_id=update.message.chat.id, text="지금부터 나 하랑이와 함께 문제를 풀어 본 경험에 대해 설문을 진행해보려고 해🤪"
    )

    await context.bot.send_message(
        chat_id=update.message.chat.id, text="문제 푸느라 피곤하겠지만~ 문항들을 꼼꼼하게 읽고 너가 느낀 그!대!로! 답해주면 좋겠어ㅎㅎ"
    )

    return INTRO


if __name__ == '__main__':
    # load_dotenv()
    application = Application.builder().token('5838635966:AAFi6chZeiqY0Ks359PR_RccmbZIo0T61fQ').build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", intro)],
        states={

            INTRO:[
                MessageHandler(filters.Regex("."), intro2)
            ],

        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()