
import logging
import AI
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from setting import get_token
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Отправь фото')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def gender_check(update: Update, context: CallbackContext) -> None:
    file_id = update.message.photo[-1].file_id
    new_file = context.bot.get_file(file_id)
    new_file.download('test.jpg')
    photo = './test.jpg'
    genders = AI.resolve(photo)
    if genders:
        for gender in genders:
            update.message.reply_text(gender)
    else:
        update.message.reply_text("Не вижу людей")


def main() -> None:
    updater = Updater(get_token())
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.photo, gender_check))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
