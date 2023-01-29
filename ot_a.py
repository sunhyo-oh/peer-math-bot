import logging
import pymysql
#from dotenv import load_dotenv
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
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

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
# QUESTION_1_ADDED : 2 / QUESTION_2_ADDED : 4 / QUESTION_3_ADDED : 6 / QUESTION_4_ADDED : 8 / QUESTION_5_ADDED : 10
START, START2, QUESTION_1, QUESTION_1_ADDED, QUESTION_2, QUESTION_2_ADDED, QUESTION_3, QUESTION_3_ADDED, QUESTION_4, QUESTION_4_ADDED, QUESTION_5, QUESTION_5_ADDED = range(12)


async def explanation (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    chat_id = update.message.chat.id

    args = (chat_id, "ot_a", context.user_data["question_id"], user.first_name, update.message.text)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, cond, question_id, user_id, explanation) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    return 2 * context.user_data["question_id"] + 1

async def start (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id, text="안녕하세요. 저는 연습용 챗봇입니다.\n제가 푼 5개의 문제에 대해 제 답이 맞았는지 틀렸는지 조언을 해주세요."
    )

    start_button = [[InlineKeyboardButton('준비됐습니다', callback_data='준비됐습니다')]]

    reply_markup = InlineKeyboardMarkup(start_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text='준비가 되었다면 아래 보이는 <준비됐습니다> 버튼을 눌러주세요.',
        reply_markup=reply_markup
    )
    return START


async def start2 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id
    await context.bot.send_message(
        chat_id=chat_id, text="이번엔 <준비됐습니다>를 채팅창에 한번 입력해보시겠습니까?"
    )

    return START2

async def question_1 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    # update.callback_query.edit_message_reply_markup(None)
    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='1번 문제부터 시작하겠습니다.',
    )

    await context.bot.send_photo(
        chat_id, open('ot1.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞습니다', callback_data='맞습니다')], [InlineKeyboardButton('틀렸습니다', callback_data='틀렸습니다')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="제가 구한 답은 18900÷21입니다.\n\n제가 구한 답이 맞습니까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 1

    return QUESTION_1

async def question_2 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, "ot_a", question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='네, 다음은 2번 문제입니다.',
    )

    await context.bot.send_photo(
       chat_id, open('ot2.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞습니다', callback_data='맞습니다')], [InlineKeyboardButton('틀렸습니다', callback_data='틀렸습니다')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="답을 구해보니 (15+20+10+15)÷4가 나왔습니다.\n\n제가 구한 게 정답입니까?",
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

    args = (chat_id, update.callback_query.data, "ot_a", question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇군요. 다음은 3번 문제입니다.',
    )

    await context.bot.send_photo(
        chat_id, open('ot3.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞습니다', callback_data='맞습니다')], [InlineKeyboardButton('틀렸습니다', callback_data='틀렸습니다')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="제 답은 (43+45+35+40+33+51+40)÷6입니다.\n\n제가 구한 답이 맞습니까?",
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

    args = (chat_id, update.callback_query.data, "ot_a", question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='알겠습니다. 다음은 4번 문제입니다.',
    )

    await context.bot.send_photo(
        chat_id, open('ot4.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞습니다', callback_data='맞습니다')], [InlineKeyboardButton('틀렸습니다', callback_data='틀렸습니다')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="저는 답이 (5+4+2+1)÷4라고 생각합니다.\n\n제 답이 맞습니까?",
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

    args = (chat_id, update.callback_query.data, "ot_a", question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id,
        text='네, 다음은 5번 문제입니다.',
    )

    await context.bot.send_photo(
        chat_id, open('ot5.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞습니다', callback_data='맞습니다')], [InlineKeyboardButton('틀렸습니다', callback_data='틀렸습니다')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="제가 생각한 답은 480+6입니다.\n\n제가 구한 게 맞습니까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 5

    return QUESTION_5

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, "ot_a", question_id, user.first_name)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    answer_o_text = [
        "제 식이 맞다고 생각하셨군요. \n식을 구하는 과정을 알려주세요."
    ]

    answer_x_text = [
        "제 식이 틀리다고 생각하십니까? \n그럼 식을 구하는 방법을 알려주세요."
    ]

    submit_button = {
        1 : [
            [InlineKeyboardButton('3주일은 20일이니까 18900÷20을 하면 돼', callback_data='1')],
            [InlineKeyboardButton('1주일이 7일이고 3주일은 21일이니까 18900÷21을 하면 돼', callback_data='2')],
            [InlineKeyboardButton('1주일이 6일이고 3주일은 18일이니까 18900÷18을 하면 돼', callback_data='3')],
            [InlineKeyboardButton('3주일은 14일이니까 18900÷20을 하면 돼', callback_data='4')],
        ],
        2 : [
            [InlineKeyboardButton('전체 딱지 수가 15+20+10이고, 학생은 4명이니까 (15+20+10)×4야', callback_data='1')],
            [InlineKeyboardButton('전체 딱지는 15+20+10+15개이고, 학생은 4명이니까 (15+20+10+15)÷4야', callback_data='2')],
            [InlineKeyboardButton('전체 딱지는 15+20+10+15개이고, 학생은 3명이니까 (15+20+10+15)÷3이야', callback_data='3')],
            [InlineKeyboardButton('전체 딱지 수가 15+20+10이고, 학생은 3명이니까 (15+20+10)×3이야', callback_data='4')],
        ],
        3 : [
            [InlineKeyboardButton('일주일은 7일이니까 43+45+35+40+33+51+40 개의 달걀을 7로 나누면 돼', callback_data='1')],
            [InlineKeyboardButton('일주일은 6일이니까 43+45+35+40+33+51+40 개의 달걀을 6으로 나누면 돼', callback_data='2')],
            [InlineKeyboardButton('일주일은 6일이니까 43+45+35+40+33+51 개의 달걀을 6으로 나누면 돼', callback_data='3')],
            [InlineKeyboardButton('일주일은 7일이니까 43+45+35+40+33+51 개의 달걀을 7으로 나누면 돼', callback_data='4')],
        ],
        4 : [
            [InlineKeyboardButton('1,2,3,4일에 읽은 책의 총합인 5+4+2+1을 3로 나누어주면 돼', callback_data='1')],
            [InlineKeyboardButton('1,2,3,4일에 읽은 책의 총합인 5+2+1을 4로 나누어주면 돼', callback_data='2')],
            [InlineKeyboardButton('1,2,3,4일에 읽은 책의 총합인 5+4+2+1을 4로 나누어주면 돼', callback_data='3')],
            [InlineKeyboardButton('1,2,3,4일에 읽은 책의 총합인 5+4+1을 4로 나누어주면 돼', callback_data='4')],
        ],
        5 : [
            [InlineKeyboardButton('왕복 전체 거리인 960km를 전체 걸린 시간인 6시간으로 나누어주면 돼', callback_data='1')],
            [InlineKeyboardButton('전체 거리인 480km를 왕복 걸린 시간인 12시간으로 나누어주면 돼', callback_data='2')],
            [InlineKeyboardButton('왕복 전체 거리인 960km를 왕복 걸린 시간인 12시간으로 나누어주면 돼', callback_data='3')],
            [InlineKeyboardButton('전체 거리인 480km를 전체 걸린 시간인 6시간으로 나누어주면 돼', callback_data='4')],
        ]
    }

    reply_markup = InlineKeyboardMarkup(submit_button[question_id])

    await context.bot.send_message(
        chat_id=chat_id,
        text= answer_o_text[0] if update.callback_query.data == "맞습니다" else answer_x_text[0], # % 뒤의 숫자는 answer_text의 개수만큼으로 한다
        reply_markup=reply_markup
    )

    return 2 * question_id + 1


async def end (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, "ot_a", question_id, user.first_name)
    cursor.execute('INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    await context.bot.send_message(
        chat_id=chat_id, text="준비한 연습용 수학 문제는 여기까지입니다. 선생님의 지시가 있을 때까지 기다려주세요."
    )

    return ConversationHandler.END

async def warning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    if not context.user_data:
        context.user_data["question_id"] = 1

    callback_number = 2 * context.user_data["question_id"] - 1

    await context.bot.send_message(
        chat_id=chat_id, text="버튼을 눌러서 알려주세요"
    )

    return callback_number

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user

    logger.info("User %s canceled the conversation.", user.first_name)

    return ConversationHandler.END

"""
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await context.bot.send_photo(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
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
    #load_dotenv()
    application = Application.builder().token('5965962344:AAHg8cL-id-WcVHy178YsqHBqTfQHVHcNUg').build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={

            START: [
                CallbackQueryHandler(start2, pattern="^\s*준비됐습니다\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],

            START2: [
                MessageHandler(filters.Regex("."), question_1)
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
                CallbackQueryHandler(end, pattern="^(1|2|3|4)"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()