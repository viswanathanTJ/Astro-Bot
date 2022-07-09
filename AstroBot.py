from email import message
import logging
import re
import os
import requests

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
    MessageHandler,
    filters
)
from user import User
import utilities

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

async def help(update: Update, _: CallbackContext):
    logger.info("Requested %s", update.message.text)
    await update.message.reply_text("ஆண்/பெண் பிறந்த தேதி, நேரம் காலை/மாலை ஊர்")
    await update.message.reply_text("Aan 5 9 2000 8 20 am madurai")
    await update.message.reply_text("Pen 5 9 2000 8 20 pm trichy")
    await update.message.reply_text("Scan <filename>")

async def print_horoscope(update: Update, _: CallbackContext):
    global print_done, scan_done
    print_done, scan_done = False, False
    msg = update.message.text
    logger.info("Details entered %s", msg)
    try:
        data = re.split(r"\s|\n|-|/|\.|,", msg)
        user = User(data)
        place = utilities.check_city(user.place.lower())
        if place is None:
            await update.message.reply_text("பிறந்த ஊர் திருத்தம் செய்யவும்")
            return
        await update.message.reply_text(user.get_user())
        print_done = False
        utilities.horoscope(user)
        await update.message.reply_text("கீழே உள்ள ஆப்சனை க்லிக் செய்யவும்", reply_markup=reply_markup)
    except:
        await update.message.reply_text("Error on processing...", reply_markup=ReplyKeyboardRemove())

async def close(update: Update, _: CallbackContext):
    utilities.cancel()
    await update.message.reply_text("ரத்து செய்யப்பட்டது", reply_markup=ReplyKeyboardRemove())

async def print_confirm(update: Update, _: CallbackContext):
    global print_done, send_done
    try:
        flag, msg = utilities.confirm_print()
        if flag:
            print_done = True
            if send_done:
                await update.message.reply_text("பிரிண்ட் செய்யப்பட்டது", reply_markup=ReplyKeyboardRemove())
                utilities.cancel()
            await update.message.reply_text(text="பிரிண்ட் செய்யப்பட்டது", reply_markup=ReplyKeyboardMarkup([['அனுப்பு'],['ரத்து செய்']], resize_keyboard=True, one_time_keyboard=True))
        else:
            if scan_done:
                keyboard = [['அனுப்பு'],['ரத்து செய்']]
                await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(keyboard), resize_keyboard=True, one_time_keyboard=True)
            else:
                await update.message.reply_text(msg, reply_markup=reply_markup)
    except:
        await update.message.reply_text("Error on processing...", reply_markup=ReplyKeyboardRemove())

async def send_horoscope(update: Update, _: CallbackContext):
    global send_done, print_done
    await update.message.reply_text("ஜாதகம் அனுப்படுகிறது...", reply_markup=ReplyKeyboardRemove())
    try:
        res = utilities.send()
        if not res:
            await update.message.reply_text("ஜாதகம் இல்லை. டீடைல் அனுப்பவும்")
            return
        path = "C:\\KkcAstro\\horoscope copy.jpg"
        send_done = True
        if print_done:
            await update.message.reply_text("அப்லோட் ஆகிறது..", reply_markup=ReplyKeyboardRemove())
            utilities.cancel()
        await update.message.reply_text("அப்லோட் ஆகிறது..", reply_markup=ReplyKeyboardMarkup([['பிரிண்ட்'],['ரத்து செய்']], resize_keyboard=True, one_time_keyboard=True))
        await update.message.reply_photo(open(path, 'rb'))
        await update.message.reply_document(open(path, 'rb'))
    except:
        await update.message.reply_text("Error on processing...", reply_markup=ReplyKeyboardRemove())

async def scan_horoscope(update: Update, _: CallbackContext):
    logger.info("Scanning horoscope for %s", update.message.text)
    name = ' '.join(update.message.text.split()[1:])+".jpg"
    logger.info("File name %s", name)
    path = "I:\\Customers\\Horoscope"
    fpath = os.path.join(path, name)
    try:
        if os.path.exists(fpath):
            await update.message.reply_text("வேறு பெயரை போடவும்")
            return
        await update.message.reply_text("ஸ்கேன் ஆகிறது...")
        status = utilities.scan(fpath)
        if status:
            await update.message.reply_photo(open(fpath, 'rb'))
            await update.message.reply_document(open(fpath, 'rb'))
            utilities.send_whatsapp(fpath)
        else:
            await update.message.reply_text("பிரின்டர் ஆன் பண்ணவும்")   
    except:
        await update.message.reply_text("Error on processing...", reply_markup=ReplyKeyboardRemove())

async def clear_printer(update: Update, _: CallbackContext):
    try:
        utilities.delete_print_queue()
        await update.message.reply_text("Cleared all queues")
    except:
        await update.message.reply_text("Error on processing...", reply_markup=ReplyKeyboardRemove())

async def off(update: Update, _: CallbackContext):
    os.system("shutdown /s /t 0")

def main() -> None:
    TOKEN = "1578946421:AAHJxmhwOIUQdeF3nS30Oa-vS2hOep27mDI"
    chat_ids = ["1225754548"]
    for chat_id in chat_ids:
        requests.post(
            url='https://api.telegram.org/bot{0}/sendMessage'.format(TOKEN, "sendMessage"),
            data={'chat_id': chat_id, 'text': 'கணிணி ஆன் ஆகிவிட்டது'}
        )
    app = Application.builder().token(TOKEN).read_timeout(15).build()
    delimiter = "(\/|-|\.|\s|,)"
    gender_regex = "(ஆண்|பெண்|female|male|a|p|m|f|M|F|A|P)"
    dob_regex = "(([1-9])|([0][1-9])|([1-2][0-9])|([3][0-1]))"+delimiter+"([1-9]|([0][1-9]|([1][0-2])))"+delimiter+"\d{4}"
    time_regex = "([1-9]|([0][1-9])|([1][0-2]))"+delimiter+"([1-9]|([0-5][0-9]))"
    m_regex = "((a|p)m|a|p|(A/P)(M/m)|காலை|மாலை)"
    place_regex = "([a-zA-Z,\s]*)"

    horoscope_regex = gender_regex + delimiter + dob_regex + delimiter + time_regex + delimiter + m_regex + place_regex
    scan_regex = r"^(((S|s)can|ஸ்கேன்))(\/|-|\.| |\n|,)[\w,\s-]+"

    app.add_handler(CommandHandler("start", help))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.Regex("(^(s|S)end$)|(^அனுப்பு$)"), send_horoscope))
    app.add_handler(MessageHandler(filters.Regex("(^(p|P)rint$)|(^பிரிண்ட்$)"), print_confirm))
    app.add_handler(MessageHandler(filters.Regex("(^(h|H)elp$)"), help))
    app.add_handler(MessageHandler(filters.Regex("(^(c|C)lose$)|(^ரத்து செய்$)"), close))
    app.add_handler(MessageHandler(filters.Regex("^(c|C)lear$"), clear_printer))
    app.add_handler(MessageHandler(filters.Regex("^(o|O)ff$"), off))
    horoscope_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(horoscope_regex), print_horoscope)],
        states = {},
        fallbacks=[CommandHandler("help", help)]
    )
    scan_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(scan_regex), scan_horoscope)],
        states = {},
        fallbacks=[CommandHandler("help", help)]
    )
    app.add_handler(horoscope_handler)
    app.add_handler(scan_handler)
    app.add_handler(MessageHandler(filters.ALL, help))

    app.run_polling()


if __name__ == "__main__":
    reply_markup = ReplyKeyboardMarkup([['பிரிண்ட்','அனுப்பு'],['ரத்து செய்']], resize_keyboard=True, one_time_keyboard=True)
    print_done, scan_done = False, False
    main()