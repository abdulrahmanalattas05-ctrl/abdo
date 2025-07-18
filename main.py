import os
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# استدعاء مفاتيح التوكن ومفتاح OpenAI من المتغيرات البيئية
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# رسالة ترحيبية تلقائية عند بدء المحادثة
def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "🤖 أهلاً بك في بوت الذكاء الاصطناعي!\n\n"
        "أنا نموذج ذكي من شركة OpenAI، أستطيع مساعدتك في الإجابة على أسئلتك أو التحدث معك في أي موضوع.\n\n"
        "📌 تم تطوير هذا البوت بواسطة: عبدالرحمن جمال عبدالرب العطاس\n"
        "اكتب سؤالك أو رسالتك الآن وسأرد عليك فورًا."
    )
    update.message.reply_text(welcome_message)

# التعامل مع كل الرسائل النصية
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=300,
            temperature=0.7,
        )
        bot_reply = response.choices[0].message['content'].strip()
        update.message.reply_text(bot_reply)

    except Exception as e:
        update.message.reply_text("حدث خطأ أثناء التواصل مع OpenAI:\n" + str(e))

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
