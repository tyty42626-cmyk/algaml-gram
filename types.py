"""Message wrapper with a stable, small public interface."""
class Message:
    def __init__(self, client, raw):
        self._client, self._raw = client, raw

    @property
    def id(self):
        return getattr(self._raw, "id", None)

    @property
    def text(self):
        return getattr(self._raw, "message", None) or getattr(self._raw, "text", None)

    @property
    def chat_id(self):
        return getattr(self._raw, "chat_id", None)

    @property
    def sender_id(self):
        sender = getattr(self._raw, "sender_id", None)
        return sender if sender is not None else getattr(self._raw, "from_id", None)

    @property
    def outgoing(self):
        return bool(getattr(self._raw, "out", False))

    @property
    def is_private(self):
        return bool(getattr(self._raw, "is_private", False))

    @property
    def is_group(self):
        return bool(getattr(self._raw, "is_group", False))

    @property
    def is_channel(self):
        return bool(getattr(self._raw, "is_channel", False))

    @property
    def photo(self):
        return getattr(self._raw, "photo", None)

    @property
    def video(self):
        return getattr(self._raw, "video", None)

    @property
    def document(self):
        return getattr(self._raw, "document", None)

    @property
    def audio(self):
        return getattr(self._raw, "audio", None)

    @property
    def voice(self):
        return getattr(self._raw, "voice", None)

    async def reply(self, text, **kwargs):
        if self.chat_id is None:
            raise ValueError("This message has no chat_id.")
        return await self._client.send_message(
            self.chat_id, text, reply_to=self.id, **kwargs
        )

    async def download(self, file=None):
        return await self._client.download_media(self, file=file)

    async def delete(self, **kwargs):
        return await self._client.delete_messages(self.chat_id, self.id, **kwargs)

    async def edit(self, text, **kwargs):
        return await self._client.edit_message(self.chat_id, self.id, text, **kwargs)
