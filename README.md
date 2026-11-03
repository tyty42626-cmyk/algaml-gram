# ALGAMLGRAM

**ALGAMLGRAM** is an early-stage Python library that provides a small,
Pyrogram-inspired interface for Telegram client automation.

> **Transport note:** version 0.2.x uses [Telethon](https://github.com/LonamiWebs/Telethon)
> for its MTProto connection. ALGAMLGRAM is currently a wrapper/API layer,
> not an independent MTProto implementation and not a drop-in Pyrogram replacement.

## Requirements

- Python 3.10 or newer
- A Telegram API ID and API hash from Telegram's official developer portal
- A Telegram account you are authorized to use

## Install from source

```bash
python -m pip install .
```

When the package is published to PyPI under the `algamlgram` distribution name,
the intended installation command will be:

```bash
python -m pip install algamlgram
```

The PyPI command will work only after the project owner successfully publishes
the package and confirms the name is available.

## Quick start

```python
from algamlgram import Client, filters

app = Client(
    "my_session",
    api_id=123456,
    api_hash="YOUR_API_HASH",
)

@app.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    await message.reply("Welcome to ALGAMLGRAM!")

app.run()
```

The first run may ask you to complete Telegram's normal sign-in flow. Keep the
created session file private.

## Basic async usage

```python
import asyncio
from algamlgram import Client

async def main():
    app = Client("my_session", 123456, "YOUR_API_HASH")
    await app.start()
    try:
        await app.send_message("me", "Hello from ALGAMLGRAM")
    finally:
        await app.stop()

asyncio.run(main())
```

## Current API

- `Client.start()` / `Client.stop()`
- `Client.run()` / `Client.run_until_disconnected()`
- `Client.send_message()` / `Client.send_file()`
- `Client.edit_message()` / `Client.delete_messages()`
- `Client.get_me()` / `Client.get_messages()` / `Client.get_dialogs()`
- `Client.download_media()`
- `Client.on_message(filter)` for message handlers
- `Message.reply()` / `Message.edit()` / `Message.delete()` / `Message.download()`
- Filters: `private`, `group`, `channel`, `incoming`, `outgoing`, `text`,
  `photo`, `video`, `document`, `media`, `command()`, `user()`, and `chat()`
- Filter composition with `&`, `|`, and `~`

## Development and tests

```bash
python -m pip install -e ".[test]"
python -m pytest
```

Build the distribution archives:

```bash
python -m build
python -m twine check dist/*
```

## Security

- Never publish `api_hash`, phone numbers, login codes, passwords, or session files.
- Keep session files outside public repositories.
- Do not commit `.env`, `*.session`, or local configuration files.
- Use the library only with accounts you control or are authorized to operate,
  and follow Telegram's terms and applicable laws.

## Project status

ALGAMLGRAM is in alpha. Public method names and behavior may change before 1.0.
The package has not yet been independently audited or certified as fully
compatible with Pyrogram.

## License and contact

Released under the MIT License.

Project contact / credits: **@mo7sle**
