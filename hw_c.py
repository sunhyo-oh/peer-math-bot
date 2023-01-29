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
INTRO, INTRO2, INTRO3, START, QUESTION_1, QUESTION_1_ADDED, QUESTION_2, QUESTION_2_ADDED, QUESTION_3, QUESTION_3_ADDED, QUESTION_4, QUESTION_4_ADDED, QUESTION_5, QUESTION_5_ADDED, \
QUESTION_6, QUESTION_6_ADDED, QUESTION_7, QUESTION_7_ADDED, QUESTION_8, QUESTION_8_ADDED, QUESTION_9, QUESTION_9_ADDED, QUESTION_10, QUESTION_10_ADDED, \
QUESTION_11, QUESTION_11_ADDED, QUESTION_12, QUESTION_12_ADDED, QUESTION_13, QUESTION_13_ADDED, QUESTION_14, QUESTION_14_ADDED, QUESTION_15, QUESTION_15_ADDED, \
QUESTION_16, QUESTION_16_ADDED, QUESTION_17, QUESTION_17_ADDED, QUESTION_18, QUESTION_18_ADDED, QUESTION_19, QUESTION_19_ADDED, QUESTION_20, QUESTION_20_ADDED, \
QUESTION_21, QUESTION_21_ADDED, QUESTION_22, QUESTION_22_ADDED, QUESTION_23, QUESTION_23_ADDED, QUESTION_24, QUESTION_24_ADDED, QUESTION_25, QUESTION_25_ADDED, \
QUESTION_26, QUESTION_26_ADDED, QUESTION_27, QUESTION_27_ADDED, QUESTION_28, QUESTION_28_ADDED, QUESTION_29, QUESTION_29_ADDED, QUESTION_30, QUESTION_30_ADDED, \
QUESTION_31, QUESTION_31_ADDED, QUESTION_32, QUESTION_32_ADDED, QUESTION_33, QUESTION_33_ADDED, QUESTION_34, QUESTION_34_ADDED, QUESTION_35, QUESTION_35_ADDED  = range(74)

async def explanation (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    chat_id = update.message.chat.id

    args = (chat_id, "hw_c", context.user_data["question_id"], user.first_name, update.message.text)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, cond, question_id, user_id, explanation) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    return 2 * context.user_data["question_id"] + 3

async def intro (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(
        chat_id=update.message.chat.id, text="안녕👋🏻 \n나는 오늘 너랑 같이 문제를 풀러 온 하랑이야~너는 이름이 뭐야?"
    )
    return INTRO

async def intro2 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    chat_id = update.message.chat.id
    question_id = None

    args = (chat_id, update.message.text, 'hw_c', question_id, user.first_name)
    cursor.execute(
        'INSERT INTO messages (chat_id, explanation, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    good_button = [[InlineKeyboardButton('좋아', callback_data='좋아')]]
    reply_markup = InlineKeyboardMarkup(good_button)

    text = "반가워~🥰 날씨가 또 추워졌어ㅠㅠ\n오늘은 도형의 넓이와 둘레를 구하는 문제를 나랑 같이 풀어보려고 하는데 어때??"
    await context.bot.send_message(
        chat_id=chat_id, text=text,
        reply_markup=reply_markup
    )

    return INTRO2

async def intro3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id, text="20분동안 내가 문제를 풀어볼 건데, 내 답이 틀릴 수도 있고 맞을 수도 있어!"
    )

    gotcha_button = [[InlineKeyboardButton('알겠어!', callback_data='알겠어!')]]
    reply_markup = InlineKeyboardMarkup(gotcha_button)

    await context.bot.send_message(
        chat_id=chat_id, text="내 답을 보고 잘 풀었는지 못 풀었는지에 대해 조언을 해주면 내가 더 열심히 해볼게🙌🏻",
        reply_markup=reply_markup
    )

    return INTRO3

async def start (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    start_button = [[InlineKeyboardButton('준비됐어💪🏻', callback_data='준비됐어💪🏻')]]
    reply_markup = InlineKeyboardMarkup(start_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text='난 이제 너의 조언에 귀 기울일 준비가 되어있어!\n너도 준비가 되었다면 아래 보이는 <준비됐어💪🏻> 버튼을 클릭해줘!!',
        reply_markup=reply_markup
    )

    return START


async def question_1 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그럼 1번 문제부터 풀어볼게!',
    )

    await context.bot.send_photo(
        chat_id, open('c1.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 식은 16×14÷2야!\n\n내가 세운 식이 맞니?🤔",
        reply_markup= reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 1

    return QUESTION_1


async def question_2 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='친절하게 설명해줘서 고마워~!😇 다음은 2번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c2.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내 생각엔 (90×60)÷2인 것 같은데,\n\n내가 구한 게 정답일까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 2

    return QUESTION_2

async def question_3 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='아하 그렇구나!! 알려줘서 고마워👍🏻 다음은 3번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c3.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 구해보니 (200+60)×140÷2가 나왔어~\n\n내가 구한 식이 맞았는지 알려줄 수 있어?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 3

    return QUESTION_3

async def question_4 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='너의 설명 잊지 않도록 노력해볼게💪 다음은 4번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c4.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 15×8이라고 생각해!!\n\n어때? 내 식이 맞을까?🧐",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 4

    return QUESTION_4

async def question_5 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='너와 함께 문제를 풀 수 있어서 너무 행복해😘 다음은 5번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c5.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 400×630인데,\n\n내가 맞게 풀었을까??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 5

    return QUESTION_5

async def question_6 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='자세한 설명 고마워👏🏻 이제 6번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c6.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 세운 식은 4×8이야!!\n\n내가 식을 맞게 세운걸까?🙏🏻",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 6

    return QUESTION_6

async def question_7 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 너가 알려준대로 다음 문제들도 열심히 풀어볼게💪🏻 다음은 7번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c7.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 세워봤는데 35×35가 나왔어!!\n\n내가 구한 게 정답이니~?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 7

    return QUESTION_7

async def question_8 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='알려줘서 정말 고마워🤩 다음은 8번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c8.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 18×18÷2이야!\n\n내 식이 맞다고 생각해, 아님 틀리다고 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 8

    return QUESTION_8

async def question_9 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 다음에도 멋진 설명 부탁해😆 다음은 9번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c9.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 40×50÷2라고 생각해ㅎㅎ\n\n내 식이 맞을까??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 9

    return QUESTION_9

async def question_10 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='친절하게 설명해줘서 고마워😙 다음은 10번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c10.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 7×9÷2야!\n\n내 생각이 맞을까?🤔",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 10

    return QUESTION_10

async def question_11 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='아 그렇네! 너의 생각이 맞는 것 같아☺️다음은 11번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c11.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 답은 105×68인데,\n\n어떻게 생각해?🤩",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 11

    return QUESTION_11

async def question_12 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='너가 도와줘서 문제 푸는게 재밌어😙 다음은 12번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c12.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 구해보니, (12+8)×2가 나왔어!!\n\n내가 구한 게 정답일까??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 12

    return QUESTION_12

async def question_13 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='아하 그렇구나! 날 도와줘서 정말 고마워🥺 다음은 13번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c13.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 세워보니 (15+9)×7÷2가 나왔어~\n\n내가 잘 풀은걸까?🧐",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 13

    return QUESTION_13

async def question_14 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='아 그렇지! 다음은 14번 문제야😆',
    )

    await context.bot.send_photo(
        chat_id, open('c14.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 7×12÷2라고 생각해!!\n\n너는 내 식이 맞았다고 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 14

    return QUESTION_14

async def question_15 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='아하! 다음 문제도 잘 부탁해🤗 다음은 15번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c15.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 답은 30×80÷2야.\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 15

    return QUESTION_15

async def question_16 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='나도 그렇게 생각해!🙌🏻 다음은 16번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c16.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 식은 (5+15)×6÷2야!\n\n너는 내 식에 대해 어떻게 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 16

    return QUESTION_16

async def question_17 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='너의 설명을 기억하도록 노력할게💪🏻 다음은 17번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c17.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 구해봤는데, 4×6이 나왔어~\n\n내가 구한 게 정답이니?🙏🏻",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 17

    return QUESTION_17

async def question_18 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='알려줘서 고마워👏🏻 다음은 18번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c18.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 답은 (20+9)×2야!\n\n내가 구한 답을 어떻게 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 18

    return QUESTION_18

async def question_19 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='아 맞네~ 너의 설명이 정말 도움이 되고 있어😇 다음 19번 문제도 잘 부탁해~',
    )

    await context.bot.send_photo(
        chat_id, open('c19.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 열심히 식을 세워봤는데 (24+4)×15÷2가 나왔어!\n\n내가 맞게 푼걸까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 19

    return QUESTION_19

async def question_20 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='너랑 같이 공부하니 너무 재밌어😆 다음은 20번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c20.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 3×4야~!\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 20

    return QUESTION_20

async def question_21 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나😲 알려줘서 고마워~ 다음은 21번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c21.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 식은 (7+4)×2인데,\n\n너가 생각하기엔 어때~??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 21

    return QUESTION_12

async def question_22 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='친절한 설명 덕분에 힘이 난다💪🏻 다음은 22번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c22.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 식을 세워봤는데 말이야~ 30×18÷2가 나왔어!\n\n내가 구한 게 정답일까😙?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 22

    return QUESTION_22

async def question_23 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='나도 그렇게 생각해👏🏻 다음은 23번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c23.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 4×20÷2야!\n\n내가 구한 식이 맞다고 생각해?😆",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 23

    return QUESTION_23

async def question_24 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='알려줘서 고마워! 다음 문제도 잘 부탁해🤩 이제 24번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c24.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 9×8이라고 생각하는데 어때?\n\n내 식이 맞을까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 24

    return QUESTION_24

async def question_25 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='알려줘서 고마워! 다음은 25번 문제야~💪🏻',
    )

    await context.bot.send_photo(
        chat_id, open('c25.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 (9+14)×12÷2인데,\n\n내가 구한 결과가 어떻다고 생각해?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 25

    return QUESTION_25

async def question_26 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나~ 너랑 같이 공부할 수 있어서 행복해🤗 다음 26번 문제도 잘 부탁해!',
    )

    await context.bot.send_photo(
        chat_id, open('c26.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 세운 식은 25x16이야!\n\n내가 구한 게 맞았니?🧐",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 26

    return QUESTION_26

async def question_27 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='자세한 설명 고마워👍🏻 다음 문제는 27번이야~',
    )

    await context.bot.send_photo(
        chat_id, open('c27.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 구해봤는데, 24x10÷2가 나왔어!!\n\n내가 구한 게 정답이라고 생각해?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 27

    return QUESTION_27

async def question_28 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='나도 너와 같은 생각이야👊🏻 다음 28번 문제도 잘 부탁해~',
    )

    await context.bot.send_photo(
        chat_id, open('c28.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각해봤는데, 식은 180×90÷2인 것 같아!\n\n내가 구한 식이 맞다고 생각해?🤔",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 28

    return QUESTION_28

async def question_29 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나! 너의 설명 잊지 않도록 노력해볼게💪🏻 다음은 29번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c29.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 6×12라고 생각하는데 어때?\n\n내 식이 맞을까?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 29

    return QUESTION_29

async def question_30 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='친절하게 설명해줘서 고마워!😇 이제 30번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c30.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 세운 식은 6×3이야!!\n\n내가 잘 풀었다고 생각해~?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 30

    return QUESTION_30

async def question_31 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='너가 도와줘서 문제 푸는게 재밌어😙 다음은 31번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c31.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="식을 구해보니, 11×11이 나왔어!!\n\n내가 구한 게 정답일까??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 31

    return QUESTION_31

async def question_32 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='그렇구나😲 다음은 32번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c32.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 5×12야~\n\n내가 잘 풀은걸까?🧐",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 32

    return QUESTION_32

async def question_33 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='날 도와줘서 정말 고마워🥺 조금만 더 힘내보자! 다음은 33번 문제야!',
    )

    await context.bot.send_photo(
        chat_id, open('c33.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="나는 식이 20×15÷2라고 생각해!!\n\n너는 내 식이 맞았다고 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 33

    return QUESTION_33

async def question_34 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='다음 문제도 잘 부탁해☺️ 다음은 34번 문제야~',
    )

    await context.bot.send_photo(
        chat_id, open('c34.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 생각한 식은 18×10÷2야.\n\n내가 구한 게 맞았니?",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 34

    return QUESTION_34

async def question_35 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text='나도 그렇게 생각해! 이제 마지막 문제야😆',
    )

    await context.bot.send_photo(
        chat_id, open('c35.png', 'rb')
    )

    ox_button = [[InlineKeyboardButton('맞아', callback_data='맞아')], [InlineKeyboardButton('틀렸어', callback_data='틀렸어')]]
    reply_markup = InlineKeyboardMarkup(ox_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text="내가 구한 마지막 문제의 식은 (6+10)×5÷2야!\n\n너는 내 식에 대해 어떻게 생각해??",
        reply_markup=reply_markup
    )

    # context.job_queue.run_once(callback_second, 2, chat_id=chat_id, name=str(chat_id), data=open('P-1-2.png', 'rb'))
    # context.job_queue.run_once(callback_second, 4, chat_id=chat_id, name=str(chat_id), data=open('P-1-3.png', 'rb'))

    context.user_data["question_id"] = 35

    return QUESTION_35

async def answer_o(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, "hw_c", question_id, user.first_name)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    answer_text = ["내가 맞았구나!🥳\n식을 구하는 과정을 설명해줄 수 있니?",
                   "와 맞았다!!😆\n식을 구하는 과정을 설명해줄래?",
                   "내 식이 맞다니 다행이야😙\n식을 구하는 과정은 어떻게 되니?"]

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text=answer_text[question_id % 3],
        reply_markup=reply_markup
    )

    return 2 * question_id + 3

async def answer_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id
    question_id = context.user_data["question_id"]

    args = (chat_id, update.callback_query.data, "hw_c", question_id, user.first_name)
    # logger.info("Answer of %s: %s", user.first_name, update.message.text)
    cursor.execute('INSERT INTO messages (chat_id, ox, cond, question_id, user_id) VALUES (%s, %s, %s, %s, %s)', args)
    db.commit()

    answer_text = ["내 식이 틀렸구나ㅠㅠ\n그럼 식을 구하는 과정을 설명해줄래?",
                   "앗 내가 틀렸구나😭\n식을 구하는 과정이 어떻게 알려줄래?",
                   "내가 틀리게 풀었구나😔\n식을 구하는 법을 설명해줄 수 있니?"]

    submit_button = [[InlineKeyboardButton('설명 마치기',  callback_data='설명 마치기')]]
    reply_markup = InlineKeyboardMarkup(submit_button)

    await context.bot.send_message(
        chat_id=chat_id,
        text=answer_text[question_id % 3],
        reply_markup=reply_markup
    )

    return 2 * question_id + 3

async def end (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.callback_query.message.chat.id

    await context.bot.send_message(
        chat_id=chat_id, text="내가 오늘 준비한 수학 문제는 여기까지야!\n다음에 또 같이 공부하자ㅎㅎ 오늘 함께해줘서 고마워~👍🏻"
    )

    return ConversationHandler.END

async def warning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chat_id = update.message.chat.id

    if not context.user_data:
        context.user_data["question_id"] = 1

    callback_number = 2 * context.user_data["question_id"] + 2

    await context.bot.send_message(
        chat_id=chat_id, text="버튼을 눌러서 알려줘!"
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
    application = Application.builder().token('5838635966:AAFi6chZeiqY0Ks359PR_RccmbZIo0T61fQ').build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", intro)],
        states={

            INTRO:[
                MessageHandler(filters.Regex("."), intro2)
            ],

            INTRO2: [
                CallbackQueryHandler(intro3, pattern="^\s*좋아\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],

            INTRO3: [
                CallbackQueryHandler(start, pattern="^\s*알겠어!\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],

            START: [
                CallbackQueryHandler(question_1, pattern="^\s*준비됐어💪🏻\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
                # MessageHandler(filters.Regex("^\s*준비됐어\s*"), question_1),
                #MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_1: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_1_ADDED: [
                CallbackQueryHandler(question_2, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_2: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_2_ADDED: [
                CallbackQueryHandler(question_3, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_3: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_3_ADDED: [
                CallbackQueryHandler(question_4, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_4: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_4_ADDED: [
                CallbackQueryHandler(question_5, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_5: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_5_ADDED: [
                CallbackQueryHandler(question_6, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_6: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_6_ADDED: [
                CallbackQueryHandler(question_7, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_7: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_7_ADDED: [
                CallbackQueryHandler(question_8, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_8: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_8_ADDED: [
                CallbackQueryHandler(question_9, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_9: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_9_ADDED: [
                CallbackQueryHandler(question_10, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_10: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_10_ADDED: [
                CallbackQueryHandler(question_11, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_11: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_11_ADDED: [
                CallbackQueryHandler(question_12, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_12: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_12_ADDED: [
                CallbackQueryHandler(question_13, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_13: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_13_ADDED: [
                CallbackQueryHandler(question_14, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_14: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_14_ADDED: [
                CallbackQueryHandler(question_15, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_15: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_15_ADDED: [
                CallbackQueryHandler(question_16, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_16: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_16_ADDED: [
                CallbackQueryHandler(question_17, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_17: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_17_ADDED: [
                CallbackQueryHandler(question_18, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_18: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_18_ADDED: [
                CallbackQueryHandler(question_19, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_19: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_19_ADDED: [
                CallbackQueryHandler(question_20, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_20: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_20_ADDED: [
                CallbackQueryHandler(question_21, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_21: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_21_ADDED: [
                CallbackQueryHandler(question_22, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_22: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_22_ADDED: [
                CallbackQueryHandler(question_23, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_23: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_23_ADDED: [
                CallbackQueryHandler(question_24, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_24: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_24_ADDED: [
                CallbackQueryHandler(question_25, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_25: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_25_ADDED: [
                CallbackQueryHandler(question_26, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_26: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_26_ADDED: [
                CallbackQueryHandler(question_27, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_27: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_27_ADDED: [
                CallbackQueryHandler(question_28, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_28: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_28_ADDED: [
                CallbackQueryHandler(question_29, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_29: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_29_ADDED: [
                CallbackQueryHandler(question_30, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_30: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_30_ADDED: [
                CallbackQueryHandler(question_31, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_31: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_31_ADDED: [
                CallbackQueryHandler(question_32, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_32: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_32_ADDED: [
                CallbackQueryHandler(question_33, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_33: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_33_ADDED: [
                CallbackQueryHandler(question_34, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_34: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_34_ADDED: [
                CallbackQueryHandler(question_35, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ],
            QUESTION_35: [
                CallbackQueryHandler(answer_o, pattern="^\s*맞아\s*"),
                CallbackQueryHandler(answer_x, pattern="^\s*틀렸어\s*"),
                MessageHandler(filters.Regex("^[^/cancel]"), warning)
            ],
            QUESTION_35_ADDED: [
                CallbackQueryHandler(end, pattern="^설명 마치기"),
                MessageHandler(filters.Regex("^[^/cancel]"), explanation)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
