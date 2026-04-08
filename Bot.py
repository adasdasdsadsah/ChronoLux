import logging
import datetime
import httpx
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    ContextTypes, ConversationHandler
)

# --- CONFIGURATION ---
TOKEN = '8765635249:AAGpqMpTpSJljmpoKVV2ChLUOuTcqAqQy88'
PROXY = 'http://svxobnel:4gcoinj6azqa@31.59.20.176:6754'
OWNER_USERNAME = "@ShiiroX1" # Update this!
LOGO_PATH = r"C:\Users\seise\Downloads\Luxurious gold ChronoLux logo.jpg"

# States
MAIN_MENU, SELECT_PAYMENT, SELECT_COUNTRY = range(3)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Luxury Landing Page"""
    keyboard = [
        [InlineKeyboardButton("💎 Start New Order", callback_data='PROCEED_ORDER')],
        [InlineKeyboardButton("📜 Terms", callback_data='SHOW_TOS'), 
         InlineKeyboardButton("❓ Help / FAQ", callback_data='SHOW_FAQ')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "✨ *CHRONOLUX LUXURY CONCIERGE*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Welcome to the premier destination for high-end timekeeping.\n\n"
        "Please select an option to begin:"
    )

    # Use the local file
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, 'rb') as photo:
            if update.message:
                await update.message.reply_photo(photo=photo, caption=welcome_text, parse_mode='Markdown', reply_markup=reply_markup)
            else:
                # If coming from a 'Back' button
                query = update.callback_query
                await query.edit_message_caption(caption=welcome_text, parse_mode='Markdown', reply_markup=reply_markup)
    else:
        if update.message:
            await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            query = update.callback_query
            await query.edit_message_text(text=welcome_text, parse_mode='Markdown', reply_markup=reply_markup)
    
    return MAIN_MENU

async def show_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the Help/FAQ Button"""
    query = update.callback_query
    await query.answer()
    
    faq_text = (
        "❓ *FREQUENTLY ASKED QUESTIONS*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "*Q: How long is shipping?*\n"
        "A: Priority shipping takes 3-5 business days.\n\n"
        "*Q: Is my payment secure?*\n"
        "A: All transactions are encrypted and handled via secure blockchain or giftcard validation.\n\n"
        "Need more help? Contact @ShiiroX1"
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='BACK_TO_START')]]
    
    try:
        await query.edit_message_caption(caption=faq_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        await query.edit_message_text(text=faq_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    return MAIN_MENU

async def show_tos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the Terms of Service Button"""
    query = update.callback_query
    await query.answer()
    
    tos_text = (
        "📜 *TERMS OF SERVICE*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "1. All sales are final once tracking is provided.\n"
        "2. ChronoLux is not responsible for customs delays.\n"
        "3. Payment must be confirmed before dispatch."
    )
    keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='BACK_TO_START')]]
    
    try:
        await query.edit_message_caption(caption=tos_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        await query.edit_message_text(text=tos_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    return MAIN_MENU

async def proceed_to_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("💳 Cryptocurrency", callback_data='Crypto')],
        [InlineKeyboardButton("🎁 International Giftcards", callback_data='Giftcards')],
        [InlineKeyboardButton("⬅️ Back", callback_data='BACK_TO_START')]
    ]
    text = "🔒 *SECURE CHECKOUT - STEP 1*\n\nPlease select your payment method:"
    
    try:
        await query.edit_message_caption(caption=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    
    return SELECT_PAYMENT

async def payment_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['payment'] = query.data

    keyboard = [
        [InlineKeyboardButton("🇫🇷 France", callback_data='France'), InlineKeyboardButton("🇩🇪 Germany", callback_data='Germany')],
        [InlineKeyboardButton("🇭🇺 Hungary", callback_data='Hungary'), InlineKeyboardButton("🇦🇹 Austria", callback_data='Austria')],
        [InlineKeyboardButton("🇬🇧 UK", callback_data='UK'), InlineKeyboardButton("🇺🇸 USA", callback_data='USA')],
        [InlineKeyboardButton("🇸🇪 Sweden", callback_data='Sweden'), InlineKeyboardButton("🇳🇱 Netherlands", callback_data='Netherlands')],
    ]
    text = f"✅ *METHOD:* {query.data}\n\n📍 *STEP 2:* Select Shipping Destination:"
    
    try:
        await query.edit_message_caption(caption=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    
    return SELECT_COUNTRY

async def country_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    payment = context.user_data.get('payment')
    country = query.data
    user = update.effective_user

    summary = (
        "📜 *OFFICIAL ORDER INVOICE*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *CLIENT:* @{user.username if user.username else 'Private User'}\n"
        f"💳 *PAYMENT:* {payment}\n"
        f"🌍 *DESTINATION:* {country}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "To finalize this order, click below:"
    )

    contact_button = [[InlineKeyboardButton("📩 Finalize with Admin", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")]]
    
    try:
        await query.edit_message_caption(caption=summary, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(contact_button))
    except:
        await query.edit_message_text(text=summary, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(contact_button))
    
    return ConversationHandler.END

if __name__ == '__main__':
    proxy_config = httpx.Proxy(url=PROXY)
    app = ApplicationBuilder().token(TOKEN).proxy(proxy_config).get_updates_proxy(proxy_config).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(proceed_to_payment, pattern='^PROCEED_ORDER$'),
                CallbackQueryHandler(show_faq, pattern='^SHOW_FAQ$'),
                CallbackQueryHandler(show_tos, pattern='^SHOW_TOS$'),
                CallbackQueryHandler(start, pattern='^BACK_TO_START$')
            ],
            SELECT_PAYMENT: [
                CallbackQueryHandler(payment_choice, pattern='^(Crypto|Giftcards)$'),
                CallbackQueryHandler(start, pattern='^BACK_TO_START$')
            ],
            SELECT_COUNTRY: [CallbackQueryHandler(country_choice)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    app.add_handler(conv_handler)
    print("🚀 ChronoLux GOLD EDITION is live...")
    app.run_polling()
