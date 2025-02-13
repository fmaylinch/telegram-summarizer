# Telegram Chat Summarizer

The idea is to read Telegram chats and summarize messages using LLM.

For now it prints messages from a chat. You should send the chat history to an LLM chat manually.

Sample usage:

```bash
# Prepare venv (once)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run app
python3 ./read_telegram_messages.py

# Deactivate venv
deactivate
```

While developing my idea, I also found this one:
- https://github.com/dev0x13/telegram-chat-summarizer
