# tg2vk

A Telegram bot that forwards messages containing **text**, **multiple
photos**, or **multiple videos** to both a Telegram channel and a
VKontakte (VK) group. The bot includes a confirmation workflow,
authorization system, and supports rich multi-media posting.

## Features

-   **Cross-Platform Posting**\
    Simultaneously publishes content to a Telegram channel and a VK
    group.
-   **Advanced Media Support**\
    Supports **multiple photos**, **multiple videos**, or mixed media in
    a single message.
-   **Confirmation Workflow**\
    Generates a preview and requires user confirmation via inline
    keyboard before publishing.
-   **Authorization System**\
    Only user IDs listed in the `.env` file can use the bot.
-   **Asynchronous**\
    Built with `aiogram` and `aiohttp` for efficient, non-blocking
    processing.
-   **Logging**\
    All activity and errors are logged both to the console and
    `bot.log`.

## How It Works

1.  An authorized user sends text, multiple photos, videos, or mixed
    content to the bot.\
2.  The bot processes the message and prepares a preview:
    -   Caption snippet
    -   Number of media items\
3.  The bot sends a message with inline buttons:
    -   **Confirm**\
    -   **Cancel**\
4.  On confirmation, the bot publishes the content to:
    -   The configured Telegram channel\
    -   The configured VK group\
5.  On cancellation, the operation is aborted.

## Getting a VK Access Token

1.  Go to https://vkhost.github.io/\
2.  Click **Settings**\
3.  Log into your VK account\
4.  Approve the requested permissions\
5.  Copy the token from the `access_token=` part of the redirected URL.

Make sure the token includes permissions for: - wall - photos - video

## Installation

``` bash
git clone https://github.com/humoridze/tg2vk.git
cd tg2vk
python -m venv venv
source venv/bin/activate  # Windows: venv/Scripts/activate
pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` into `.env`:

    TELEGRAM_BOT_TOKEN=your_bot_token_here
    TELEGRAM_CHANNEL_ID=-1001234567890
    VK_USER_TOKEN=your_vk_user_token_here
    VK_GROUP_ID=123456789
    ALLOWED_USER_IDS=123456789,987654321

## Usage

``` bash
python main.py
```

## Project Structure

    ├── main.py
    ├── requirements.txt
    ├── .env.example
    ├── bot/
    │   ├── config/settings.py
    │   ├── core/
    │   │   ├── bot.py
    │   │   └── logger.py
    │   ├── handlers/message_handler.py
    │   ├── middleware/auth_middleware.py
    │   ├── services/
    │   │   ├── telegram_publisher.py
    │   │   └── vk_publisher.py
    │   └── utils/media_processor.py

## License

MIT License.
