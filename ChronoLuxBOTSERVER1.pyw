import logging
import datetime
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    ContextTypes, ConversationHandler
)

# 1. Configuration
TOKEN = 'PASTE_YOUR_NEW_TOKEN_HERE'  # Get a fresh one from @BotFather
PROXY = 'http://svxobnel:4gcoinj6azqa@31.59.20.176:6754'
OWNER_USERNAME = "@YourUsername" # Put your Telegram @ username here

# Conversation States
SELECT_PAYMENT, SELECT_COUNTRY = range(2)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Step 1: User selects Payment"""
    keyboard = [
        [InlineKeyboardButton("💳 Crypto (BTC/ETH)", callback_data='Crypto')],
        [InlineKeyboardButton("🎁 Giftcards", callback_data='Giftcard')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to *ChronoLux Luxury* ⌚\n\nStep 1: Please select your *Payment Method*:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    return SELECT_PAYMENT

async def payment_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Step 2: Save payment and ask for Country"""
    query = update.callback_query
    await query.answer()
    
    # Save the payment choice in user_data
    context.user_data['payment'] = query.data
    
    keyboard = [
        [InlineKeyboardButton("🇺🇸 USA", callback_data='USA'), InlineKeyboardButton("🇬🇧 UK", callback_data='UK')],
        [InlineKeyboardButton("🇪🇺 Europe", callback_data='Europe'), InlineKeyboardButton("🌍 Other", callback_data='Other')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"✅ Payment: *{query.data}*\n\nStep 2: Please select your *Shipping Region*:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    return SELECT_COUNTRY

async def country_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Step 3: Show Final Summary and Link to Owner"""
    query = update.callback_query
    await query.answer()
    
    payment = context.user_data.get('payment')
    country = query.data
    
    summary = (
        "📊 *ORDER SUMMARY*\n"
        "━━━━━━━━━━━━━━━\n"
        f"💳 *Payment:* {payment}\n"
        f"🌍 *Shipping:* {country}\n"
        "━━━━━━━━━━━━━━━\n\n"
        f"Please click below to contact the owner and complete your order:"
    )
    
    keyboard = [[InlineKeyboardButton("📩 Contact Owner", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(summary, parse_mode='Markdown', reply_markup=reply_markup)
    return ConversationHandler.END

if __name__ == '__main__':
    proxy_config = httpx.Proxy(url=PROXY)
    app = ApplicationBuilder().token(TOKEN).proxy(proxy_config).get_updates_proxy(proxy_config).build()

    # Create the conversation flow
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_PAYMENT: [CallbackQueryHandler(payment_choice)],
            SELECT_COUNTRY: [CallbackQueryHandler(country_choice)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    app.add_handler(conv_handler)
    
    print("🚀 ChronoLux Professional is live...")
    app.run_polling()