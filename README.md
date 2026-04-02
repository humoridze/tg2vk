# tg2vk

## Getting a VK Access Token

1.  Go to https://vkhost.github.io/
2.  Click **Settings**
3.  Log into your VK account
4.  Approve the requested permissions
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
