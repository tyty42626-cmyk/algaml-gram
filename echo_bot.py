from algamlgram import Client, filters

app = Client("echo_session", 123456, "YOUR_API_HASH")

@app.on_message(filters.private & filters.text)
async def echo(client, message):
    if not message.outgoing:
        await message.reply(message.text)

if __name__ == "__main__":
    app.run()
