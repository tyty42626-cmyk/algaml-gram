"""Telegram client wrapper. Telethon currently supplies the MTProto transport."""
import asyncio
import inspect
import os
from telethon import TelegramClient, events
from .types import Message

class Client:
    def __init__(self, name, api_id, api_hash, *, session_dir="sessions",
                 device_model="ALGAMLGRAM", system_version="1.0",
                 app_version="0.2.0", connection_retries=5, retry_delay=2):
        if not api_id or not api_hash:
            raise ValueError("api_id and api_hash are required.")
        self.name = str(name)
        self.api_id, self.api_hash = int(api_id), str(api_hash)
        self.session_dir = session_dir
        self.connection_retries = max(1, int(connection_retries))
        self.retry_delay = max(0, float(retry_delay))
        self._handlers = []
        self._client = None
        self._dispatch_installed = False
        self._device = dict(device_model=device_model, system_version=system_version,
                            app_version=app_version)

    def on_message(self, filter=None):
        """Register a message callback: callback(client, message)."""
        def decorator(func):
            if not callable(func):
                raise TypeError("Handler must be callable.")
            self._handlers.append((filter, func))
            return func
        return decorator

    async def start(self, phone=None):
        if self._client and self._client.is_connected():
            return self
        os.makedirs(self.session_dir, exist_ok=True)
        session_path = os.path.join(self.session_dir, self.name)
        self._client = TelegramClient(
            session_path, self.api_id, self.api_hash, **self._device
        )
        last_error = None
        for attempt in range(self.connection_retries):
            try:
                await self._client.start(phone=phone)
                self._install_handlers()
                return self
            except Exception as exc:
                last_error = exc
                if attempt + 1 < self.connection_retries:
                    await asyncio.sleep(self.retry_delay)
        raise ConnectionError(
            f"ALGAMLGRAM could not connect after {self.connection_retries} attempts."
        ) from last_error

    def _install_handlers(self):
        if self._dispatch_installed:
            return
        @self._client.on(events.NewMessage)
        async def dispatch(event):
            message = Message(self, event.message)
            for filt, callback in tuple(self._handlers):
                if filt is not None and not filt(message):
                    continue
                result = callback(self, message)
                if inspect.isawaitable(result):
                    await result
        self._dispatch_installed = True

    async def stop(self):
        if self._client:
            await self._client.disconnect()

    async def send_message(self, chat_id, text, **kwargs):
        self._require_started()
        return await self._client.send_message(chat_id, text, **kwargs)

    async def send_file(self, chat_id, file, **kwargs):
        self._require_started()
        return await self._client.send_file(chat_id, file, **kwargs)

    async def edit_message(self, chat_id, message, text, **kwargs):
        self._require_started()
        return await self._client.edit_message(chat_id, message, text, **kwargs)

    async def delete_messages(self, chat_id, message_ids, **kwargs):
        self._require_started()
        return await self._client.delete_messages(chat_id, message_ids, **kwargs)

    async def get_me(self):
        self._require_started()
        return await self._client.get_me()

    async def get_messages(self, chat_id, limit=10, **kwargs):
        self._require_started()
        return await self._client.get_messages(chat_id, limit=limit, **kwargs)

    async def get_dialogs(self, limit=None):
        self._require_started()
        return await self._client.get_dialogs(limit=limit)

    async def download_media(self, message, file=None):
        self._require_started()
        raw = getattr(message, "_raw", message)
        return await self._client.download_media(raw, file=file)

    async def run_until_disconnected(self):
        self._require_started()
        await self._client.run_until_disconnected()

    def run(self, phone=None):
        async def runner():
            await self.start(phone=phone)
            try:
                await self.run_until_disconnected()
            finally:
                await self.stop()
        return asyncio.run(runner())

    def _require_started(self):
        if not self._client or not self._client.is_connected():
            raise RuntimeError("Client is not started. Call await app.start() first.")
