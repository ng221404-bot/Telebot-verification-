# Telegram Secure Access Verification Bot

This is a premium Telegram bot designed for secure manual access verification. It features an animated user experience, inline keyboard input for access codes, and a robust admin approval system.

## Features

*   **Premium Welcome**: Custom welcome image and caption in multiple languages.
*   **Automated Proceed**: Seamless user flow to initiate verification.
*   **Secure Contact Sharing**: Users share their Telegram phone number securely.
*   **Admin Notification**: Admin receives user details and verification requests.
*   **Animated Messages**: Smooth, waiting-style animated messages during verification steps.
*   **Manual Code Entry**: Users enter a secure access code via an inline numeric keypad.
*   **Admin Approval**: Admin manually approves or rejects access codes.
*   **Access Grant/Denial**: Clear feedback to the user upon verification outcome.
*   **Multi-user State Management**: Handles multiple concurrent verification flows.
*   **Scalable Architecture**: Designed for future expansion and integration with other bots.

## Technical Stack

*   **Language**: Python
*   **Bot Framework**: `python-telegram-bot`
*   **Environment Management**: `python-dotenv`

## Project Structure

```
telegram_secure_access_bot/
├── bot/
│   ├── __init__.py
│   ├── main.py                 # Entry point for the bot
│   ├── config.py               # Configuration settings (API tokens, admin IDs, messages)
│   ├── handlers.py             # Defines all bot command and message handlers
│   ├── keyboards.py            # Generates inline and reply keyboards
│   ├── utils.py                # Utility functions (e.g., animated messages, message editing)
├── .env.example                # Example environment variables file
├── .gitignore                  # Git ignore file
├── README.md                   # Project README with setup and usage instructions
├── requirements.txt            # Python dependencies
```

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/telegram_secure_access_bot.git
cd telegram_secure_access_bot
```

### 2. Create a Telegram Bot

1.  Talk to the BotFather on Telegram (`@BotFather`).
2.  Use the `/newbot` command to create a new bot.
3.  Follow the instructions to set up a name and username for your bot.
4.  BotFather will give you an **API Token**. Keep this token secure.

### 3. Get Your Admin Chat ID

1.  Start a chat with your new bot.
2.  Forward any message from yourself to the `userinfobot` (`@userinfobot`).
3.  The `userinfobot` will provide your `Chat ID`. This will be your `ADMIN_CHAT_ID`.
    *If you want to use a private group as admin chat, add your bot to the group and make it an administrator. Then, send any message to the group and forward it to `@userinfobot` to get the group's chat ID. Remember that group chat IDs are usually negative.*

### 4. Environment Variables

Create a `.env` file in the root directory of the project (`telegram_secure_access_bot/`) based on the `.env.example` file:

```dotenv
BOT_TOKEN="YOUR_TELEGRAM_BOT_API_TOKEN"
ADMIN_CHAT_ID="YOUR_ADMIN_CHAT_ID"
WELCOME_IMAGE_URL="https://example.com/your_welcome_image.jpg" # Optional: URL for the welcome image
```

Replace the placeholder values with your actual bot token, admin chat ID, and optionally, a URL for your welcome image.

### 5. Install Dependencies

It's recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
pip install -r requirements.txt
```

### 6. Run the Bot

```bash
python3 bot/main.py
```

Your bot should now be running and ready to receive messages!

## Usage

1.  **Start the Bot**: Send `/start` to your bot.
2.  **Proceed**: Click the "Proceed Automatically" button.
3.  **Share Contact**: Share your phone number when prompted.
4.  **Admin Action**: The admin will receive a notification and can send a secure code to the user.
5.  **Enter Code**: The user enters the secure code using the inline keypad.
6.  **Verification**: The admin approves or rejects the entered code.
7.  **Access Granted/Denied**: The user receives feedback.

## Extending the Bot

*   **State Management**: For persistent user states beyond a single session, consider integrating a database (e.g., SQLite, PostgreSQL) instead of in-memory storage.
*   **Premium Features**: Integrate your premium features/tools to be unlocked upon successful verification.
*   **Multi-bot Integration**: The core verification logic is designed to be reusable. You can integrate this `bot` directory as a module into other Telegram bot projects.

## Contributing

Feel free to fork the repository, make improvements, and submit pull requests.

## License

This project is open-source and available under the MIT License. (You can choose your preferred license.)
