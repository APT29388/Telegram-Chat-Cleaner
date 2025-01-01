from telethon import TelegramClient
import asyncio
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

API_ID = config.get('Telegram', 'api_id')
API_HASH = config.get('Telegram', 'api_hash')

PROTECTED_CHATS = [
    #Сюда короче id чата, который удалять не ннада
]

async def clean_telegram(client):
    async for dialog in client.iter_dialogs():
        try:
            if dialog.id in PROTECTED_CHATS:
                print(f"Пропуск {dialog.name}")
                continue
    
            print(f"Удаляем {dialog.name}")
            await client.delete_dialog(dialog.id)
            
        except Exception as e:
            print(f"Ошибка {dialog.name}: {str(e)}")
            continue

async def main():
    client = TelegramClient('tg_cleaner_session', API_ID, API_HASH)
    
    try:
        await client.start()
        
        if not await client.is_user_authorized():
            print("Нужно авторизоваться")
            return
            
        await clean_telegram(client)
        
    except Exception as e:
        print(f"Ошибка {str(e)}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
