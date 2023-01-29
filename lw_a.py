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
db = pymysql.connect(host="localhost", user="root", passwd = '1234', charset="utf8")
cursor = db.cursor()
cursor.execute('USE chatbot;')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# QUESTION 1 : 1 / QUESTION 2 : 3 / QUESTION 3 : 5 / QUESTION 4 : 7 / QUESTION 5 : 9
INTRO, INTRO2, START, QUESTION_1, QUESTION_1_ADDED, QUESTION_2, QUESTION_2_ADDED, QUESTION_3, QUESTION_3_ADDED, QUESTION_4, QUESTION_4_ADDED, QUESTION_5, QUESTION_5_ADDED, \
QUESTION_6, QUESTION_6_ADDED, QUESTION_7, QUESTION_7_ADDED, QUESTION_8, QUESTION_8_ADDED, QUESTION_9, QUESTION_9_ADDED, QUESTION_10, QUESTION_10_ADDED, \
QUESTION_11, QUESTION_11_ADDED, QUESTION_12, QUESTION_12_ADDED, QUESTION_13, QUESTION_13_ADDED, QUESTION_14, QUESTION_14_ADDED, QUESTION_15, QUESTION_15_ADDED, \
QUESTION_16, QUESTION_16_ADDED, QUESTION_17, QUESTION_17_ADDED, QUESTION_18, QUESTION_18_ADDED, QUESTION_19, QUESTION_19_ADDED, QUESTION_20, QUESTION_20_ADDED, \
QUESTION_21, QUESTION_21_ADDED, QUESTION_22, QUESTION_22_ADDED, QUESTION_23, QUESTION_23_ADDED, QUESTION_24, QUESTION_24_ADDED, QUESTION_25, QUESTION_25_ADDED, \
QUESTION_26, QUESTION_26_ADDED, QUESTION_27, QUESTION_27_ADDED, QUESTION_28, QUESTION_28_ADDED, QUESTION_29, QUESTION_29_ADDED, QUESTION_30, QUESTION_30_ADDED, \
QUESTION_31, QUESTION_31_ADDED, QUESTION_32, QUESTION_32_ADDED, QUESTION_33, QUESTION_33_ADDED, QUESTION_34, QUESTION_34_ADDED, QUESTION_35, QUESTION_35_ADDED  = range(73)



async def intro (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    good_button = [[InlineKeyboardButton('알겠어', callback_data='알겠어')]]
    reply_markup = InlineKeyboardMarkup(good_button)

    text = "오늘 넌 나한테 도형의 넓이와 둘레를 구하는 문제를 설명할거야."
    await context.bot.send_message(
        chat_id=chat_id, text=text,
        reply_markup=reply_markup
    )

    return INTRO

async def intro2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id, text="20분동안 내가 문제를 풀어볼 건데, 내 답이 맞을 수도 있고 틀릴 수도 있어."
    )

    await context.bot.send_message(
        chat_id=chat_id, text="내 답이 틀렸다면 왜 틀렸는지 설명하고"
    )


    gotcha_button = [[InlineKeyboardButton('이해했어', callback_data='이해했어')]]
    reply_markup = InlineKeyboardMarkup(gotcha_button)

    await context.bot.send_message(
        chat_id=chat_id, text="내 답이 맞았다면 왜 맞았다고 생각했는지도 알려줘.",
        reply_markup=reply_markup
    )

    return INTRO2

async def start (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    start_button = [[InlineKeyboardButton('준비됐어', callback_data='준비됐어')]]
    reply_markup = InlineKeyboardMarkup(start_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text='준비가 됐다면 아래 보이는 <준비됐어> 버튼을 클릭해.',
        reply_markup=reply_markup
    )

    return START



async def question_1 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='1번 문제부터 풀어볼게.',
    )

    await context.bot.send_photo(
        chat_id, open('a1.png', 'rb')
    )


    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식은 16×14÷2야.\n\n정답이지?",
        reply_markup= reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 1

    return QUESTION_1

async def question_2 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음은 2번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a2.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="(90×60)÷2야.\n\n맞아?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 2

    return QUESTION_2

async def question_3 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='이제 3번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a3.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="(200+60)×140÷2라고 생각해.\n\n내 식이 맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 3

    return QUESTION_3

async def question_4 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='흠 다음은 4번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a4.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="15×8이 맞지 않아?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 4

    return QUESTION_4

async def question_5 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음은 5번 문제.',
    )

    await context.bot.send_photo(
        chat_id, open('a5.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="400×630?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 5

    return QUESTION_5

async def question_6 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음은 6번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a6.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 4×8라고 생각함.\n\n내 식이 맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 6

    return QUESTION_6

async def question_7 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='그런가 다음은 7번 문제를 풀거야.',
    )

    await context.bot.send_photo(
        chat_id, open('a7.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="35×35라고 식을 세웠어.\n\n맞아?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 7

    return QUESTION_7

async def question_8 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='음 다음은 8번 문제야. ',
    )

    await context.bot.send_photo(
        chat_id, open('a8.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 18×18÷2라고 풀었어.\n\n맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 8

    return QUESTION_8

async def question_9 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음은 9번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a9.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식은 40×50÷2야.\n\n정답이지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 9

    return QUESTION_9

async def question_10 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='이제 10번 문제 풀거야.',
    )

    await context.bot.send_photo(
        chat_id, open('a10.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="7×9÷2라고 생각함.\n\n내가 맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 10

    return QUESTION_10

async def question_11 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음은 11번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a11.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="105×68이 맞아?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 11

    return QUESTION_11

async def question_12 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='이번엔 12번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a12.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="(12+8)×2?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 12

    return QUESTION_12

async def question_13 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='...13번 문제 풀게. ',
    )

    await context.bot.send_photo(
        chat_id, open('a13.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="난 (15+9)×7÷2라고 생각해.\n\n맞음?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 13

    return QUESTION_13

async def question_14 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='흠 다음은 14번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a14.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="7×12÷2가 나왔음.\n\n맞아?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 14

    return QUESTION_14

async def question_15 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음 문제는 15번 문제.',
    )

    await context.bot.send_photo(
        chat_id, open('a15.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="30×80÷2가 맞다고 생각?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 15

    return QUESTION_15

async def question_16 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='이제 16번 문제 풀거야.',
    )

    await context.bot.send_photo(
        chat_id, open('a16.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 식은 (5+15)×6÷2.\n\n내 식이 맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 16

    return QUESTION_16

async def question_17 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='디음은 17번 문제.',
    )

    await context.bot.send_photo(
        chat_id, open('a17.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="4×6이 맞지 않아?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 17

    return QUESTION_17

async def question_18 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='이제 18번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a18.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="(20+9)×2라고 생각함.\n\n맞아?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 18

    return QUESTION_18

async def question_19 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='19번 문제 풀거야.',
    )

    await context.bot.send_photo(
        chat_id, open('a19.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="(24+4)×15÷2야.\n\n맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 19

    return QUESTION_19

async def question_20 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='흠 다음 20번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a20.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="난 3×4라고 세울거야.\n\n내가 맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 20

    return QUESTION_20

async def question_21 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음은 21번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a21.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="(7+4)×2네.\n\n맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 21

    return QUESTION_12

async def question_22 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='...이제 22번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a22.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="30×18÷2 맞음?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 22

    return QUESTION_22

async def question_23 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='23번 문제를 풀거야.',
    )

    await context.bot.send_photo(
        chat_id, open('a23.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="4×20÷2?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 23

    return QUESTION_23

async def question_24 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='음 24번 문제 풀게.',
    )

    await context.bot.send_photo(
        chat_id, open('a24.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="9×8이네.\n\n내가 맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 24

    return QUESTION_24

async def question_25 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='25번이야.',
    )

    await context.bot.send_photo(
        chat_id, open('a25.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="(9+14)×12÷2라고 생각함.\n\n내가 맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 25

    return QUESTION_25

async def question_26 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='이제 26번 문제임.',
    )

    await context.bot.send_photo(
        chat_id, open('a26.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="25x16?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 26

    return QUESTION_26

async def question_27 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음 문제는 27번.',
    )

    await context.bot.send_photo(
        chat_id, open('a27.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 식은 24x10÷2야.\n\n내가 맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 27

    return QUESTION_27

async def question_28 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='흠 28번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a28.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="180×90÷2가 나왔네.\n\n맞지 않아?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 28

    return QUESTION_28

async def question_29 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음은 29번이야.',
    )

    await context.bot.send_photo(
        chat_id, open('a29.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="18×10÷2?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 29

    return QUESTION_29

async def question_30 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='음 이제 30번 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a30.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="난 6×3이라고 생각.\n\n맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 30

    return QUESTION_30

async def question_31 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음 문제는 31번이야.',
    )

    await context.bot.send_photo(
        chat_id, open('a31.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식은 11×11.\n\n맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 31

    return QUESTION_31

async def question_32 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='흠 32번 문제 풀게.',
    )

    await context.bot.send_photo(
        chat_id, open('a32.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="5×12?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 32

    return QUESTION_32

async def question_33 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음은 33번 문제.',
    )

    await context.bot.send_photo(
        chat_id, open('a33.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="20×15÷2가 맞는 식이지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 33

    return QUESTION_33

async def question_34 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='이제 34번 문제 풀거야.',
    )

    await context.bot.send_photo(
        chat_id, open('a34.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 식은 18×10÷2.\n\n맞지?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 34

    return QUESTION_34

async def question_35 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='마지막 문제야.',
    )

    await context.bot.send_photo(
        chat_id, open('a35.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="(6+10)×5÷2가 맞지 않아?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 35

    return QUESTION_35


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, "lw_a", question_id, user.first_name)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    answer_o_text = ["내가 맞게 풀었다는 거지?\n식을 구하는 과정을 설명해봐.",
                   "내가 식을 맞게 구했네.\n식을 구하는 과정은 어떻게 되는거지?"]

    answer_x_text = ["내 식이 틀렸다는 거지?\n그럼 식을 구하는 과정을 설명해봐.",
                   "내가 틀리게 풀었다고?;;\n식을 구하는 법이 어떻게 되는건데?"]

    submit_button = {
        1 : [
            [InlineKeyboardButton('밑변의 길이 16, 높이는 14라서 식은 16×14÷2야', callback_data='1')],
            [InlineKeyboardButton('밑변의 길이 16, 높이는 16라서 식은 16×16÷2야', callback_data='2')],
            [InlineKeyboardButton('밑변의 길이 16, 높이는 14라서 식은 16×14야', callback_data='3')],
            [InlineKeyboardButton('밑변의 길이 14, 높이는 16이라서 식은 14×16÷2가 돼', callback_data='4')]
        ],
        2 : [
            [InlineKeyboardButton('한 대각선의 길이 90, 다른 대각선 길이 60이니까 식은 90×60이야', callback_data='1')],
            [InlineKeyboardButton('한 대각선의 길이 90, 다른 대각선 길이 60이므로 식은 90×60÷2야', callback_data='2')],
            [InlineKeyboardButton('한 대각선의 길이 90, 다른 대각선 길이 30이기 때문에 90×30÷2야', callback_data='3')],
            [InlineKeyboardButton('한 대각선의 길이 45, 다른 대각선 길이 60이므로 45×60÷2야', callback_data='4')]
        ],
        3 : [
            [InlineKeyboardButton('윗변의 길이는 140, 아랫변의 길이는 200, 높이는 60니까 (140+200)×60÷2야', callback_data='1')],
            [InlineKeyboardButton('윗변의 길이는 200, 아랫변의 길이는 60, 높이는 140이니까 (200+60)×14÷2야', callback_data='2')],
            [InlineKeyboardButton('윗변의 길이는 60, 아랫변의 길이는 140, 높이는 200이니까 (60+140)×200÷2야', callback_data='3')],
            [InlineKeyboardButton('윗변의 길이는 60, 아랫변의 길이는 140, 높이는 200이니까 (60+140)×200이야', callback_data='4')]
        ],
        4 : [
            [InlineKeyboardButton('세로는 8cm니까 식은 8×8이야', callback_data='1')],
            [InlineKeyboardButton('가로는 15cm니까 식은 15×15야', callback_data='2')],
            [InlineKeyboardButton('가로는 15cm, 세로는 8cm이니까 식을 세워보면 (15+8)×2야', callback_data='3')],
            [InlineKeyboardButton('가로는 15cm이고 세로는 8cm이니까 식을 구해보면 15×8이야', callback_data='4')]
        ],
        5 : [
            [InlineKeyboardButton('밑변은 400cm이고 높이는 630cm이기 때문에 식을 세워보면 400×630이야', callback_data='1')],
            [InlineKeyboardButton('밑변은 400cm이고 높이는 630cm이기 때문에 식을 세워보면 400×630÷2야', callback_data='2')],
            [InlineKeyboardButton('밑변은 200cm이고 높이는 630cm이기 때문에 식을 구해보면 200×630이야', callback_data='3')],
            [InlineKeyboardButton('밑변은 630cm이고 높이는 400cm라서 식을 만들어보면 640×400이야', callback_data='4')]
        ],
        6 : [
            [InlineKeyboardButton('한 변의 길이가 4cm니까 식을 세워보면 4×4야', callback_data='1')],
            [InlineKeyboardButton('한 변의 길이가 4cm니까 식은 4×6이 맞아', callback_data='2')],
            [InlineKeyboardButton('한 변의 길이는 4cm이기 때문에 식은 4×8이 돼', callback_data='3')],
            [InlineKeyboardButton('한 변의 길이가 6cm라서 식은 6×4야', callback_data='4')]
        ],
        7 : [
            [InlineKeyboardButton('한 변의 길이는 35cm이기 때문에 식을 구해보면 35×4가 돼', callback_data='1')],
            [InlineKeyboardButton('한 변의 길이는 30cm이기 때문에 식을 구해보면 30×30이 돼', callback_data='2')],
            [InlineKeyboardButton('한 변의 길이는 35cm이고, 정사각형의 넓이는 35×35를 하면 돼', callback_data='3')],
            [InlineKeyboardButton('한 변의 길이는 35cm이기 때문에 식을 구해보면 35×35÷2가 돼', callback_data='4')]
        ],
        8 : [
            [InlineKeyboardButton('밑변의 길이는 18cm고 높이는 18cm니까 18×18÷2가 맞아', callback_data='1')],
            [InlineKeyboardButton('밑변의 길이는 25cm고 높이는 18cm라서 식은 25×18이야', callback_data='2')],
            [InlineKeyboardButton('밑변의 길이는 18cm고 높이는 25cm이기 때문에 식은 18×25÷2야', callback_data='3')],
            [InlineKeyboardButton('밑변의 길이는 18cm고 높이는 18cm니까 18×18이 맞는 식이야', callback_data='4')]
        ],
        9 : [
            [InlineKeyboardButton('한 대각선의 길이는 40이고 다른 대각선의 길이는 50이므로 식은 40×50이야', callback_data='1')],
            [InlineKeyboardButton('한 대각선의 길이는 40이고 다른 대각선의 길이는 50이니까 식이 40×50÷2야', callback_data='2')],
            [InlineKeyboardButton('한 대각선의 길이는 25이고 다른 대각선의 길이는 50이니까 식은 25×50÷2야', callback_data='3')],
            [InlineKeyboardButton('한 대각선의 길이는 40이고 다른 대각선의 길이는 50이니까 식이 20×50÷2야', callback_data='4')]
        ],
        10 : [
            [InlineKeyboardButton('밑변의 길이는 7cm이고 높이는 9cm니까 식은 7×9÷2야', callback_data='1')],
            [InlineKeyboardButton('밑변의 길이는 7cm이고 높이는 9cm니까 식은 7×9가 맞아', callback_data='2')],
            [InlineKeyboardButton('밑변의 길이는 9cm이고 높이는 7cm니까 식은 9×7÷2라고 세우면 돼', callback_data='3')],
            [InlineKeyboardButton('밑변의 길이는 9cm이고 높이는 7cm이기 때문에 식을 구해보면 9×7이 나와', callback_data='4')]
        ],
        11 : [
            [InlineKeyboardButton('가로는 105cm이고 세로는 68cm니까 식은 105+68이야', callback_data='1')],
            [InlineKeyboardButton('가로는 105cm이고 세로는 68cm이기 때문에 식을 구하면 105×68이 나와', callback_data='2')],
            [InlineKeyboardButton('가로는 105cm이고 세로는 68cm라서 식은 (105+68)÷2가 맞아', callback_data='3')],
            [InlineKeyboardButton('가로는 105cm이고 세로는 60cm니까 식은 105×60라고 세우면 돼', callback_data='4')]
        ],
        12 : [
            [InlineKeyboardButton('한 변의 길이는 12cm이고 다른 변의 길이는 10cm니까 식은 12+10이야', callback_data='1')],
            [InlineKeyboardButton('한 변의 길이는 12cm이고 다른 변의 길이는 10cm니까 식은 (12+10)×2야', callback_data='2')],
            [InlineKeyboardButton('한 변의 길이는 12cm이고 다른 변의 길이는 8cm니까 (12+8)×2가 맞는 식이야', callback_data='3')],
            [InlineKeyboardButton('한 변의 길이는 12cm이고 다른 변의 길이는 8cm라서 12×8로 구하면 돼', callback_data='4')]
        ],
        13 : [
            [InlineKeyboardButton('윗변의 길이는 15고 아랫변의 길이는 9, 높이는 7이니까 식은 (15+9)×7÷2야', callback_data='1')],
            [InlineKeyboardButton('윗변의 길이는 15고 높이는 7이니까 식을 구하면 15×72가 나와', callback_data='2')],
            [InlineKeyboardButton('윗변의 길이는 15고 아랫변의 길이는 9, 높이는 9니까 식은 (15+9)×9÷2야', callback_data='3')],
            [InlineKeyboardButton('윗변의 길이는 15고 아랫변의 길이는 9, 높이는 7이니까 식은 (15+9)×7이야', callback_data='4')]
        ],
        14 : [
            [InlineKeyboardButton('밑변의 길이는 12cm이고 높이는 7cm니까 식은 12×7÷2야', callback_data='1')],
            [InlineKeyboardButton('밑변의 길이는 7cm이고 높이는 12cm니까 식을 구해보면 7×12가 나와', callback_data='2')],
            [InlineKeyboardButton('밑변의 길이는 7cm이고 높이는 12cm니까 식은 7×12÷2야', callback_data='3')],
            [InlineKeyboardButton('밑변의 길이는 12cm이고 높이는 7cm니까 식은 12×7이야', callback_data='4')]
        ],
        15 : [
            [InlineKeyboardButton('밑변의 길이는 30cm이고 높이는 80cm니까 30×80이 맞아', callback_data='1')],
            [InlineKeyboardButton('밑변의 길이는 30cm이고 높이는 80cm이기 때문에 식은 30×80÷2가 맞아', callback_data='2')],
            [InlineKeyboardButton('밑변의 길이는 80cm이고 높이는 30cm니까 식은 80×30라고 세우면 돼', callback_data='3')],
            [InlineKeyboardButton('밑변의 길이는 80cm이고 높이는 30cm라서 식은 80×30÷2야', callback_data='4')]
        ],
        16 : [
            [InlineKeyboardButton('윗변의 길이는 5, 아랫변의 길이는 15, 높이는 6이니까 식은 (5+15)×6이야', callback_data='1')],
            [InlineKeyboardButton('윗변의 길이는 5, 아랫변의 길이는 15, 높이는 6이니까 (5+15)×6÷2가 맞아', callback_data='2')],
            [InlineKeyboardButton('아랫변의 길이는 15고 높이는 6이기 때문에 식을 세우면 15×6÷2가 돼', callback_data='3')],
            [InlineKeyboardButton('윗변의 길이는 5, 아랫변의 길이는 15, 높이는 8이니까 (5+15)×8이 맞아', callback_data='4')]
        ],
        17 : [
            [InlineKeyboardButton('한 대각선의 길이는 4cm이고 다른 대각선의 길이는 6cm니까 4×6이 맞아', callback_data='1')],
            [InlineKeyboardButton('한 대각선의 길이는 6cm, 다른 대각선의 길이는 4cm이기 때문에 식은 (4+6)×2야', callback_data='2')],
            [InlineKeyboardButton('한 대각선의 길이는 6cm, 다른 대각선의 길이는 6cm니까 4×6÷2가 맞는 식이야', callback_data='3')],
            [InlineKeyboardButton('한 대각선의 길이는 4cm, 다른 대각선의 길이는 6cm니까 4×6÷2라고 세울 수 있어', callback_data='4')]
        ],
        18 : [
            [InlineKeyboardButton('가로는 20cm이고, 세로는 9cm이니까 20+9+9가 돼', callback_data='1')],
            [InlineKeyboardButton('가로는 20cm니까 식을 구해보면 20+20이 돼', callback_data='2')],
            [InlineKeyboardButton('세로가 9cm니까 식을 세워보면 9×4가 돼', callback_data='3')],
            [InlineKeyboardButton('가로는 20cm이고, 세로는 9cm이니까 (20+9)×2가 돼', callback_data='4')]
        ],
        19 : [
            [InlineKeyboardButton('윗변의 길이 24, 아랫변의 길이 4, 높이 15니까 (24+4)×15÷2가 돼', callback_data='1')],
            [InlineKeyboardButton('윗변의 길이 24, 아랫변의 길이 15, 높이 4이니까 식은 (24+15)×4÷2가 맞아', callback_data='2')],
            [InlineKeyboardButton('윗변의 길이 24, 아랫변의 길이 4, 높이 15니까 식은 (24+4)×15가 돼', callback_data='3')],
            [InlineKeyboardButton('높이 15, 아랫변의 길이 4니까 식을 세워 보면 15×4÷2가 돼', callback_data='4')]
        ],
        20: [
            [InlineKeyboardButton('밑변은 3이고 높이는 4이기 때문에 식은 3×4야', callback_data='1')],
            [InlineKeyboardButton('밑변은 3이고 높이는 4이기 때문에 식은 3×4÷2야', callback_data='2')],
            [InlineKeyboardButton('밑변은 4이고 높이는 3이기 때문에 식은 (4+3)×2야', callback_data='3')],
            [InlineKeyboardButton('밑변은 3이고 높이는 5이기 때문에 식은 3×5야', callback_data='4')]
        ],
        21 : [
            [InlineKeyboardButton('세로는 4cm니까 식은 4×4야', callback_data='1')],
            [InlineKeyboardButton('가로는 7cm, 세로는 4cm니까 식을 세워보면 (7+4)×2야', callback_data='2')],
            [InlineKeyboardButton('가로는 7cm이고 세로는 4cm니까 식을 구해보면 7×4야', callback_data='3')],
            [InlineKeyboardButton('가로는 7cm니까 식은 7×7이야.', callback_data='4')]
        ],
        22 : [
            [InlineKeyboardButton('한 대각선의 길이는 30, 다른 대각선의 길이는 18이기 때문에 식은 30×18이 돼', callback_data='1')],
            [InlineKeyboardButton('한 대각선의 길이는 15, 다른 대각선의 길이는 18이기 때문에 15×18이야', callback_data='2')],
            [InlineKeyboardButton('한 대각선의 길이는 30, 다른 대각선의 길이는 18이기 때문에 식은 30×18÷2야', callback_data='3')],
            [InlineKeyboardButton('한 대각선의 길이는 30, 다른 대각선의 길이는 9이기 때문에 30×9÷2가 돼', callback_data='4')]
        ],
        23 : [
            [InlineKeyboardButton('밑변의 길이는 4cm이고, 높이는 20cm이기 때문에 식을 세워보면 4×20이 돼', callback_data='1')],
            [InlineKeyboardButton('밑변의 길이는 4cm이고, 높이는 20cm이기 때문에 식은 4×20÷2가 돼', callback_data='2')],
            [InlineKeyboardButton('밑변의 길이는 20cm이고, 높이는 4cm이기 때문에 식을 구해보면 20×4가 돼', callback_data='3')],
            [InlineKeyboardButton('밑변의 길이는 16cm이고, 높이는 20cm이기 때문에 식을 세워보면 16×20÷2가 돼', callback_data='4')]
        ],
        24 : [
            [InlineKeyboardButton('한 변의 길이는 9cm니까 식을 구해보면 9×7가 돼', callback_data='1')],
            [InlineKeyboardButton('한 변의 길이는 9cm니까 식으로 표현하면 9×6이 돼', callback_data='2')],
            [InlineKeyboardButton('한 변의 길이는 18cm니까 식으로 표현하면 18×7이야', callback_data='3')],
            [InlineKeyboardButton('한 변의 길이는 9cm니까 식을 세워보면 9×8이야', callback_data='4')]
        ],
        25 : [
            [InlineKeyboardButton('윗변의 길이는 9, 아랫변의 길이는 14, 높이는 12니까 (9+14)×12÷2가 돼', callback_data='1')],
            [InlineKeyboardButton('윗변의 길이는 12, 아랫변의 길이는 14, 높이는 9니까 식은 (12+14)×9÷2야', callback_data='2')],
            [InlineKeyboardButton('윗변의 길이는 9, 높이는 12니까 식을 세워 보면 9×12÷2가 돼', callback_data='3')],
            [InlineKeyboardButton('높이는 12, 아랫변의 길이는 14니까 식을 세워 보면 12×14÷2가 돼', callback_data='4')]
        ],
        26 : [
            [InlineKeyboardButton('종이의 밑변은 25, 높이는 16이기 때문에 식을 구해보면 25×16이 돼', callback_data='1')],
            [InlineKeyboardButton('종이의 밑변은 25, 높이는 16이기 때문에 식을 구해보면 25×16÷2가 돼', callback_data='2')],
            [InlineKeyboardButton('종이의 밑변은 16, 높이는 25이기 때문에 식은 16×25÷2가 되는 것 같아', callback_data='3')],
            [InlineKeyboardButton('종이의 밑변은 50, 높이는 16이기 때문에 식은 50×16이야', callback_data='4')]
        ],
        27 : [
            [InlineKeyboardButton('한 대각선의 길이는 10, 다른 대각선의 길이는 24이기 때문에 식은 10×24가 돼', callback_data='1')],
            [InlineKeyboardButton('한 대각선의 길이는 10, 다른 대각선의 길이는 13이기 때문에 10×13이 돼', callback_data='2')],
            [InlineKeyboardButton('한 대각선의 길이는 10, 다른 대각선의 길이는 13이기 때문에 10×13÷2가 돼', callback_data='3')],
            [InlineKeyboardButton('한 대각선의 길이는 10, 다른 대각선의 길이는 24이기 때문에 10×24÷2가 돼', callback_data='4')]
        ],
        28 : [
            [InlineKeyboardButton('밑변의 길이는 150cm, 높이는 90cm이기 때문에 식을 세우면, 150×90÷2가 돼', callback_data='1')],
            [InlineKeyboardButton('밑변의 길이는 150cm, 높이는 90cm이기 때문에 식을 세우면, 150×90가 돼', callback_data='2')],
            [InlineKeyboardButton('밑변의 길이는 180cm, 높이는 150cm이기 때문에 식을 세우면, 180×150÷2가 돼', callback_data='3')],
            [InlineKeyboardButton('밑변의 길이는 180cm, 높이는 90cm이기 때문에 식을 세우면, 180×90÷2가 돼', callback_data='4')]
        ],
        29 : [
            [InlineKeyboardButton('가로는 6cm니까 식은 6×6이야', callback_data='1')],
            [InlineKeyboardButton('세로는 12cm니까 식은 12×12야', callback_data='2')],
            [InlineKeyboardButton('가로는 6cm, 세로는 12cm이니까 식을 세워보면 (6+12)×2야', callback_data='3')],
            [InlineKeyboardButton('가로는 6cm이고 세로는 12cm이니까 식을 구해보면 6×12야', callback_data='4')]
        ],
        30 : [
            [InlineKeyboardButton('한 변의 길이는 6cm니까 6×2가 돼', callback_data='1')],
            [InlineKeyboardButton('한 변은 6cm니까 테두리의 길이는 6×3이 돼', callback_data='2')],
            [InlineKeyboardButton('한 변의 길이가 6cm니까 테두리는 6×3÷2가 돼', callback_data='3')],
            [InlineKeyboardButton('한 변의 길이가 3cm니까 테두리는 3×3이 돼', callback_data='4')]
        ],
        31 : [
            [InlineKeyboardButton('한 변의 길이는 11m이기 때문에 식을 구해보면 11×11이 돼', callback_data='1')],
            [InlineKeyboardButton('한 변의 길이는 22m이기 때문에 식을 세워보면 22×22가 돼', callback_data='2')],
            [InlineKeyboardButton('한 변의 길이는 11m이고, 정사각형의 넓이는 11×4를 하면 돼', callback_data='3')],
            [InlineKeyboardButton('한 변의 길이는 11m이기 때문에 식을 구해보면 11×11÷2가 돼', callback_data='4')]
        ],
        32 : [
            [InlineKeyboardButton('밑변은 15cm이고 높이는 12cm이기 때문에 식을 세우면 15×12÷2야', callback_data='1')],
            [InlineKeyboardButton('밑변은 15cm이고 높이는 5cm이기 때문에 식을 세워보면 15×5야', callback_data='2')],
            [InlineKeyboardButton('밑변은 5cm이고 높이는 12cm이기 때문에 식을 구해보면 5×12야', callback_data='3')],
            [InlineKeyboardButton('밑변은 5cm이고 높이는 15cm라서 식을 만들어보면 5×15야', callback_data='4')]
        ],
        33 : [
            [InlineKeyboardButton('밑변의 길이는 20cm, 높이는 15cm이기 때문에 식을 세워보면, 20×15÷2가 돼', callback_data='1')],
            [InlineKeyboardButton('밑변의 길이는 25cm, 높이는 15cm라서 식을 세워보면, 25×15÷2가 돼', callback_data='2')],
            [InlineKeyboardButton('밑변의 길이는 20cm, 높이는 15cm이기 때문에 식을 세워보면, 20×15가 되네', callback_data='3')],
            [InlineKeyboardButton('밑변의 길이는 15cm, 높이는 25cm이기 때문에 식을 만들어보면 15×25÷2가 나와', callback_data='4')]
        ],
        34 : [
            [InlineKeyboardButton('한 대각선의 길이는 18, 다른 대각선의 길이는 10이기 때문에 식은 18×10이 돼', callback_data='1')],
            [InlineKeyboardButton('한 대각선의 길이는 18, 다른 대각선의 길이는 5이기 때문에 18×5÷2가 돼', callback_data='2')],
            [InlineKeyboardButton('한 대각선의 길이는 9, 다른 대각선의 길이는 10이기 때문에 9×10÷2가 돼', callback_data='3')],
            [InlineKeyboardButton('한 대각선의 길이는 18, 다른 대각선의 길이는 10이기 때문에 18×10÷2가 돼', callback_data='4')]
        ],
        35: [
            [InlineKeyboardButton('윗변의 길이는 6, 아랫변의 길이는 10, 높이는 5니까 (6+10)×5÷2가 돼', callback_data='1')],
            [InlineKeyboardButton('윗변의 길이는 5, 아랫변의 길이는 10, 높이는 6이니까 식은 (5+10)×6÷2가 맞아', callback_data='2')],
            [InlineKeyboardButton('윗변의 길이는 5, 아랫변의 길이는 10, 높이는 6이니까 식은 (5+10)×6이야', callback_data='3')],
            [InlineKeyboardButton('윗변의 길이는 6, 아랫변의 길이는 10, 높이는 5니까 (6+10)×5가 돼', callback_data='4')]
        ],

    }
    reply_markup = InlineKeyboardMarkup(submit_button[question_id])


    await context.bot.send_message(
        chat_id=chat_id,
        text= answer_o_text[question_id % 2] if update.callback_query.data == "맞아" else answer_x_text[question_id % 2], # % 뒤의 숫자는 answer_text의 개수만큼으로 한다
        reply_markup=reply_markup
    )


    return 2 * question_id + 2


async def end (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, 'lw_a', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id, text="오늘 준비한 수학 문제는 여기까지. 잘가."
    )

    return ConversationHandler.END

async def warning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    if not context.user_data:
        context.user_data["question_id"] = 1

    callback_number = 2 * context.user_data["question_id"] + 1

    await context.bot.send_message(
        chat_id=chat_id, text="버튼을 눌러서 알려줘."
    )

    return callback_number


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    return ConversationHandler.END
"""
def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    # Remove job with given name. Returns whether job was removed.
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def callback_second(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=context.job.chat_id, photo=context.job.data)
"""

if __name__ == '__main__':
    # load_dotenv()
    application = Application.builder().token('5915485149:AAEM_K2CM8hs9gAhBIjutlR3AnPux4WGQb4').build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", intro)],
        states={

            INTRO: [
                CallbackQueryHandler(intro2, pattern="^\s*알겠어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],

            INTRO2: [
                CallbackQueryHandler(start, pattern="^\s*이해했어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],

            START: [
                CallbackQueryHandler(question_1, pattern="^\s*준비됐어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
                # MessageHandler(filters.Regex("^\s*준비됐어\s*"), question_1),
                #MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_1: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_1_ADDED: [
                CallbackQueryHandler(question_2, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_2: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_2_ADDED: [
                CallbackQueryHandler(question_3, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_3: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_3_ADDED: [
                CallbackQueryHandler(question_4, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_4: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_4_ADDED: [
                CallbackQueryHandler(question_5, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_5: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_5_ADDED: [
                CallbackQueryHandler(question_6, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_6: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_6_ADDED: [
                CallbackQueryHandler(question_7, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_7: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_7_ADDED: [
                CallbackQueryHandler(question_8, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_8: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_8_ADDED: [
                CallbackQueryHandler(question_9, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_9: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_9_ADDED: [
                CallbackQueryHandler(question_10, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_10: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_10_ADDED: [
                CallbackQueryHandler(question_11, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_11: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_11_ADDED: [
                CallbackQueryHandler(question_12, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_12: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_12_ADDED: [
                CallbackQueryHandler(question_13, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_13: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_13_ADDED: [
                CallbackQueryHandler(question_14, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_14: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_14_ADDED: [
                CallbackQueryHandler(question_15, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_15: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_15_ADDED: [
                CallbackQueryHandler(question_16, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_16: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_16_ADDED: [
                CallbackQueryHandler(question_17, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_17: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_17_ADDED: [
                CallbackQueryHandler(question_18, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_18: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_18_ADDED: [
                CallbackQueryHandler(question_19, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_19: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_19_ADDED: [
                CallbackQueryHandler(question_20, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_20: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_20_ADDED: [
                CallbackQueryHandler(question_21, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_21: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_21_ADDED: [
                CallbackQueryHandler(question_22, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_22: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_22_ADDED: [
                CallbackQueryHandler(question_23, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_23: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_23_ADDED: [
                CallbackQueryHandler(question_24, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_24: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_24_ADDED: [
                CallbackQueryHandler(question_25, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_25: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_25_ADDED: [
                CallbackQueryHandler(question_26, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_26: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_26_ADDED: [
                CallbackQueryHandler(question_27, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_27: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_27_ADDED: [
                CallbackQueryHandler(question_28, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_28: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_28_ADDED: [
                CallbackQueryHandler(question_29, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_29: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_29_ADDED: [
                CallbackQueryHandler(question_30, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_30: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_30_ADDED: [
                CallbackQueryHandler(question_31, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_31: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_31_ADDED: [
                CallbackQueryHandler(question_32, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_32: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_32_ADDED: [
                CallbackQueryHandler(question_33, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_33: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_33_ADDED: [
                CallbackQueryHandler(question_34, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_34: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_34_ADDED: [
                CallbackQueryHandler(question_35, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_35: [
                CallbackQueryHandler(answer, pattern="^(맞|틀)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_35_ADDED: [
                CallbackQueryHandler(end, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

