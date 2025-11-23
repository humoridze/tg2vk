import asyncio
from bot.core.bot import TelegramBot
from bot.core.logger import setup_logger

async def main():
    logger = setup_logger()
    logger.info("Starting bot...")
    
    bot = TelegramBot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())