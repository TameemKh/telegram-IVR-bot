import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 هندسة أنظمة الحاسوب", callback_data="cse")],
        [InlineKeyboardButton("❓ أسئلة شائعة", callback_data="faq")],
        [InlineKeyboardButton("📚 هندسة الميكانيك", callback_data="me")], 
        [InlineKeyboardButton("📚 الهندسة الكهربائية", callback_data="ee")], 
        [InlineKeyboardButton("📚 هندسة الطاقة", callback_data="ene")] 
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "أهلاً بك 👋\nاختر ما تريد:",
        reply_markup=reply_markup
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cse":
        keyboard = [
            [InlineKeyboardButton("📘 المواد", callback_data="subjects")],
            [InlineKeyboardButton("🗺 Roadmaps", callback_data="roadmaps")],
            [InlineKeyboardButton("رجوع ➔", callback_data="back_main")]
        ]
        await query.edit_message_text(
            text="هندسة أنظمة الحاسوب:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "faq":
        keyboard = [
          [InlineKeyboardButton("رجوع ➔", callback_data="back_cse")]
        ]
        await query.edit_message_text(
            "❓ الأسئلة الشائعة:\n\n"
            "• كيف أجد مواد كل مساق؟\n"
            "→ من قسم المواد.\n\n"
            "• هل المحتوى يتحدث؟\n"
            "→ نعم، يتم تحديثه دوريًا."
        )
    elif query.data == "subjects":
        keyboard = [
            [InlineKeyboardButton("🧮 مواد السنة الأولى", callback_data="cse_year1")],
            [InlineKeyboardButton("💻 مواد السنة الثانية", callback_data="cse_year2")],
            [InlineKeyboardButton("⚙️ مواد السنة الثالثة", callback_data="cse_year3")],
            [InlineKeyboardButton("رجوع ➔", callback_data="back_cse")]
        ]
        await query.edit_message_text(
            text="📘 مواد هندسة أنظمة الحاسوب:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "back_cse":
        keyboard = [
          [InlineKeyboardButton("📘 المواد", callback_data="subjects")],
          [InlineKeyboardButton("🗺 Roadmaps", callback_data="roadmaps")],
          [InlineKeyboardButton("رجوع ➔", callback_data="back_main")]
          
        ]
        await query.edit_message_text(
          text="هندسة أنظمة الحاسوب:",
          reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "back_main":
      keyboard = [
        [InlineKeyboardButton("📚 هندسة أنظمة الحاسوب", callback_data="cse")],
        [InlineKeyboardButton("❓ أسئلة شائعة", callback_data="faq")],
        [InlineKeyboardButton("📚 هندسة الميكانيك", callback_data="me")]
      ]
      await query.edit_message_text(
        text="أهلاً بك 👋\nاختر ما تريد:",
        reply_markup=InlineKeyboardMarkup(keyboard)
      )
    elif query.data == "roadmaps":
      file_path = "resonsOfIOSStrength.docx"
      await context.bot.send_document(
          chat_id=query.message.chat_id,
          document=open(file_path, "rb"),
          caption="🗺 Roadmap هندسة أنظمة الحاسوب"
      )
      keyboard = [
          [InlineKeyboardButton("📘 المواد", callback_data="subjects")],
          [InlineKeyboardButton("🗺 Roadmaps", callback_data="roadmaps")],
          [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
      ]
      await query.edit_message_text(
          text="هندسة أنظمة الحاسوب:",
          reply_markup=InlineKeyboardMarkup(keyboard)
      )
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()