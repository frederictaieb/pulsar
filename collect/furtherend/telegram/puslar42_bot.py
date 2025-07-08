import dotenv
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

dotenv.load_dotenv()

TOKEN = "8013259458:AAHC_Cx8ubi9dzdu7DAoL4x3Xunh15vX7JE"
TIMEOUT = 60
API_URL = "https://aemi.frederictaieb.com/api/core/wormhole/send_data"

# In-memory state store
user_states = {}


# ---------------------------
# Helpers
# ---------------------------

async def send_message(target, text):
    """Send a message whether it's an Update or a CallbackQuery."""
    if hasattr(target, "edit_message_text"):
        await target.edit_message_text(text)
    else:
        await target.message.reply_text(text)


def get_user_state(user_id):
    """Get or initialize user state."""
    if user_id not in user_states:
        user_states[user_id] = {}
    return user_states[user_id]


# ---------------------------
# Menu
# ---------------------------

async def show_menu(target, state):
    """Show the menu with current GPS data and options."""
    latitude = state.get("latitude", 0.0000)
    longitude = state.get("longitude", 0.0000)
    msg = f"Latitude: {latitude:.4f}\nLongitude: {longitude:.4f}"

    keyboard = [
        [
            InlineKeyboardButton("📍 GPS", callback_data="gps"),
            InlineKeyboardButton("📤 Send", callback_data="send"),
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await target.message.reply_text(f"{msg}\n\nChoose an option :", reply_markup=markup)


# ---------------------------
# GPS flow
# ---------------------------

async def start_gps_flow(target, state, return_to_send=False):
    """Ask for latitude. Mark if Send should follow after GPS."""
    state["step"] = "awaiting_latitude"
    if return_to_send:
        state["after_gps"] = "send"
    await send_message(target, "Enter your latitude:")


async def handle_latitude(update: Update, state):
    """Parse and validate latitude."""
    text = update.message.text.strip()
    try:
        value = float(text)
        if not -90 <= value <= 90:
            raise ValueError
        state["latitude"] = value
        state["step"] = "awaiting_longitude"
        await update.message.reply_text("Enter your longitude:")
    except ValueError:
        await update.message.reply_text("Invalid latitude. Please enter a number between -90 and +90.")


async def handle_longitude(update: Update, state):
    """Parse and validate longitude."""
    text = update.message.text.strip()
    try:
        value = float(text)
        if not -180 <= value <= 180:
            raise ValueError
        state["longitude"] = value
        await update.message.reply_text(
            f"Coordinates saved!\nLatitude: {state['latitude']:.4f}\nLongitude: {state['longitude']:.4f}"
        )
        # Continue to Send flow if needed
        if state.pop("after_gps", None) == "send":
            await start_send_flow(update, state)
        else:
            state["step"] = None
            await show_menu(update, state)
    except ValueError:
        await update.message.reply_text("Invalid longitude. Please enter a number between -180 and +180.")


# ---------------------------
# Send flow
# ---------------------------

async def start_send_flow(target, state):
    """Start Send: if GPS is missing, redirect to GPS first."""
    if not state.get("latitude") or not state.get("longitude"):
        await start_gps_flow(target, state, return_to_send=True)
    else:
        state["step"] = "awaiting_message"
        await send_message(target, "Enter your message:")


async def handle_send_api(update: Update, state):
    """POST data to external API and show result."""
    payload = {
        "latitude": state["latitude"],
        "longitude": state["longitude"],
        "data": update.message.text.strip(),
    }

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.post(API_URL, json=payload)
            if response.status_code == 200:
                await update.message.reply_text(f"API response: {response.text}")
            else:
                await update.message.reply_text(
                    f"API error: {response.status_code} {response.text}"
                )
        except httpx.RequestError as e:
            await update.message.reply_text(f"Request failed: {e}")

    state["step"] = None
    await show_menu(update, state)


# ---------------------------
# Handlers
# ---------------------------

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    state = get_user_state(user_id)
    await show_menu(update, state)


async def gps_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    state = get_user_state(user_id)
    await start_gps_flow(update, state)


async def send_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    state = get_user_state(user_id)
    await start_send_flow(update, state)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    state = get_user_state(user_id)

    if query.data == "gps":
        await start_gps_flow(query, state)
    elif query.data == "send":
        await start_send_flow(query, state)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    state = get_user_state(user_id)

    if state.get("step") == "awaiting_latitude":
        await handle_latitude(update, state)
    elif state.get("step") == "awaiting_longitude":
        await handle_longitude(update, state)
    elif state.get("step") == "awaiting_message":
        await handle_send_api(update, state)
    else:
        await update.message.reply_text("Please use /menu to start.")


# ---------------------------
# Main entrypoint
# ---------------------------

def main():
    print("Starting bot...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("menu", menu_handler))
    app.add_handler(CommandHandler("gps", gps_handler))
    app.add_handler(CommandHandler("send", send_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
