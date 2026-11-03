"""Composable filters for ALGAMLGRAM messages."""
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class Filter:
    predicate: Callable[[Any], bool]

    def __call__(self, message: Any) -> bool:
        try:
            return bool(self.predicate(message))
        except Exception:
            return False

    def __and__(self, other):
        return Filter(lambda m: self(m) and other(m))

    def __or__(self, other):
        return Filter(lambda m: self(m) or other(m))

    def __invert__(self):
        return Filter(lambda m: not self(m))

def _flag(name, expected=True):
    return Filter(lambda m: bool(getattr(m, name, False)) == expected)

private = _flag("is_private")
group = _flag("is_group")
channel = _flag("is_channel")
incoming = _flag("outgoing", False)
outgoing = _flag("outgoing", True)
text = Filter(lambda m: bool(getattr(m, "text", None)))
photo = Filter(lambda m: bool(getattr(m, "photo", None)))
video = Filter(lambda m: bool(getattr(m, "video", None)))
document = Filter(lambda m: bool(getattr(m, "document", None)))
media = Filter(lambda m: any(getattr(m, x, None) for x in ("photo", "video", "document", "audio", "voice")))
all = Filter(lambda m: True)

def command(commands, prefixes=("/", "!")):
    """Match commands such as /start or !help."""
    if isinstance(commands, str):
        commands = [commands]
    accepted = {str(c).lstrip("/!") for c in commands}
    prefixes = tuple(prefixes)
    def check(message):
        value = getattr(message, "text", None) or ""
        if not value or not value.startswith(prefixes):
            return False
        first = value.split(maxsplit=1)[0][1:].split("@", 1)[0]
        return first in accepted
    return Filter(check)

def user(user_ids):
    if isinstance(user_ids, (int, str)):
        user_ids = [user_ids]
    accepted = {int(x) for x in user_ids}
    return Filter(lambda m: getattr(m, "sender_id", None) is not None
                  and int(m.sender_id) in accepted)

def chat(chat_ids):
    if isinstance(chat_ids, (int, str)):
        chat_ids = [chat_ids]
    accepted = {int(x) for x in chat_ids}
    return Filter(lambda m: getattr(m, "chat_id", None) is not None
                  and int(m.chat_id) in accepted)
