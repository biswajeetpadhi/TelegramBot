
import os
#from keep_alive import keep_alive
#from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Replace 'YOUR_BOT_TOKEN' with your actual API token
# ""
#load_dotenv()
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your new bot.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echoes the user's message."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a help message."""
    help_text = """
    Available commands:
    /start - Start the bot
    /help - Show this help message
    /caps <text> - Convert text to uppercase
    /button - Display inline buttons
    /stop - Stop the bot
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Converts text to uppercase."""
    if context.args:
        text_caps = ' '.join(context.args).upper()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide text to convert to uppercase.")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with an inline button."""
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='1'),
         InlineKeyboardButton("Option 2", callback_data='2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose:', reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles inline keyboard button clicks."""
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    await query.edit_message_text(text=f"Selected option: {query.data}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles photo messages."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Nice photo!"
    )

async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stops the bot gracefully."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Stopping the bot..."
    )
    context.application.stop()

def main():
    """Starts the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("caps", caps))
    application.add_handler(CommandHandler("button", button))
    application.add_handler(CommandHandler("stop", stop_bot))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    #keep_alive()
    
    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
