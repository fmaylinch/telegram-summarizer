# pip install -r requirements.txt
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient, functions, types
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

TELEGRAM_GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')

SESSION_NAME = 'my_session'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


async def print_message_reactions(message, chat_id):
    output = []
    if message.reactions:
        result = await client(functions.messages.GetMessageReactionsListRequest(
            peer=chat_id,  # Chat or channel ID/username
            id=message.id,  # Message ID
            limit=100  # Maximum number of reactions to fetch
        ))
        for reaction in result.reactions:
            user_id = reaction.peer_id.user_id
            user = next((u for u in result.users if u.id == user_id), None)
            if user:
                # we ignore other kind of reactions (maybe custom images)
                if hasattr(reaction.reaction, 'emoticon'):
                    output.append(f"- {user.username} reacted: {reaction.reaction.emoticon}")
    return "\n".join(output)


async def message_to_string(message, chat_id):
    #sender = f"{message.sender.first_name} {message.sender.last_name or ""} ({message.sender.username})"
    sender = message.sender.username if message.sender else None
    id = f"{message.id}, reply to {message.reply_to_msg_id}" if message.is_reply else message.id
    
    output = []
    output.append(f"{message.date} (id: {id})")
    output.append(f"{sender}: {message.message}")
    #output.append(await print_message_reactions(message, chat_id))
    output.append("-" * 3)
    
    return "\n".join(output)
    


# Another way of reading messages that I found
async def read_messages_alternative(entity):
    posts = await client(functions.messages.GetHistoryRequest(
        peer=entity,
        limit=3,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0))
    for msg in posts.messages:
        print(f"{msg.date} - {msg.id} - {msg.message}")
        #print(f"{msg}")

async def print_groups():
    dialogs = await client.get_dialogs()
    print("Groups you are a member of:")
    print("-" * 50)
    for dialog in dialogs:
        if dialog.is_group:
            print(f"Group: {dialog.id} - {dialog.name}")



async def main():
    # Connect to the Telegram servers
    await client.start()
    
    try:
        # await print_groups()

        chat_id = int(TELEGRAM_GROUP_ID)
        entity = await client.get_entity(chat_id)

        date = datetime.now() - timedelta(days=30)
        date = datetime(2025, 2, 12)
        #date = datetime.now()

        all_messages = []
        async for message in client.iter_messages(entity=entity, limit=10, offset_date=date, reverse=True):
            message_str = await message_to_string(message, chat_id)
            all_messages.append(message_str)

        with open('prompt.txt', 'r', encoding='utf-8') as f:
            template = f.read()
            messages_str = '\n'.join(all_messages)
            filled_template = template.replace('<messages>', messages_str)
            print(filled_template)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
