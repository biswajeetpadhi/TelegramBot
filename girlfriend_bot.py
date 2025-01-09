import os
import random
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Replace with your actual bot token (get it from BotFather)
BOT_TOKEN = "8006373572:AAEfCii_u32KsuTXxOZPxlCWw6OdFU5rcgk"

# --- Personalized Messages and Compliments ---
NICKNAME = "Baby"  # Replace with your girlfriend's nickname

compliments = [
    f"{NICKNAME}, you're the most amazing person I know.",
    f"Every time I see you, {NICKNAME}, my heart skips a beat.",
    f"You light up my world, {NICKNAME}.",
    f"You're so smart, funny, and beautiful, {NICKNAME}.",
    f"{NICKNAME}, you make me a better person.",
    f"I'm so lucky to have you in my life, {NICKNAME}.",
    f"You have the most beautiful smile, {NICKNAME}.",
    f"You're my dream come true, {NICKNAME}.",
]

love_messages = [
    f"I love you more than words can say, {NICKNAME}.",
    f"You're my everything, {NICKNAME}.",
    f"I can't imagine my life without you, {NICKNAME}.",
    f"Thinking of you always makes my day better, {NICKNAME}.",
    f"You're the best thing that's ever happened to me, {NICKNAME}.",
    f"I'm so grateful for your love, {NICKNAME}.",
    f"I cherish every moment we spend together, {NICKNAME}.",
]

good_morning_messages = [
    f"Good morning, beautiful {NICKNAME}! I hope you have an amazing day.",
    f"Rise and shine, {NICKNAME}! Sending you lots of love to start your day.",
    f"Good morning, sunshine! You're the first thing on my mind, {NICKNAME}.",
    f"Wake up, my love! I can't wait to see you today (or later), {NICKNAME}.",
]

good_night_messages = [
    f"Good night, my sweet {NICKNAME}. Sleep well and dream of me.",
    f"Sweet dreams, my love. I'll be thinking of you, {NICKNAME}.",
    f"Good night, beautiful. I can't wait to see you in my dreams, {NICKNAME}.",
    f"Sleep tight, {NICKNAME}. I love you to the moon and back.",
]

# --- Bot Functionality ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hello {NICKNAME}! I'm your personalized bot. "
             f"Type /help to see what I can do."
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays a help message."""
    help_text = r"""
    Here are the commands you can use:

    /start - Start the bot
    /help - Show this help message
    /compliment - Get a random compliment
    /love - Get a love message
    /morning - Get a good morning message
    /night - Get a good night message
    /button - See some options
    /send\_pic - to get a random image
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=help_text
    )

async def send_compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a random compliment."""
    compliment = random.choice(compliments)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=compliment
    )

async def send_love_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a random love message."""
    message = random.choice(love_messages)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )

async def send_good_morning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a good morning message."""
    message = random.choice(good_morning_messages)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )

async def send_good_night(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a good night message."""
    message = random.choice(good_night_messages)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )

async def send_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file_id = "AgACAgUAAxkBAAIDYmYw0d5P9XGfAAFl9bN64w_Y-h3nAAJ5zDEbI9lBVYd4zQ_Dk4vWAQADAgADcwADMwQ"
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_file_id)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with an inline button."""
    keyboard = [
        [InlineKeyboardButton("Compliment", callback_data='compliment'),
         InlineKeyboardButton("Love Message", callback_data='love')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose an option:', reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles inline keyboard button clicks."""
    query = update.callback_query
    await query.answer()

    if query.data == 'compliment':
        await send_compliment(update, context)
    elif query.data == 'love':
        await send_love_message(update, context)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles unknown commands."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command. Type /help to see what I can do."
    )

def main():
    """Starts the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("compliment", send_compliment))
    application.add_handler(CommandHandler("love", send_love_message))
    application.add_handler(CommandHandler("morning", send_good_morning))
    application.add_handler(CommandHandler("night", send_good_night))
    application.add_handler(CommandHandler("button", button))
    application.add_handler(CommandHandler("send_pic", send_pic))

    # Add callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    # Handle unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()