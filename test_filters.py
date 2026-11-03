from types import SimpleNamespace
from algamlgram import filters

def msg(**kwargs):
    defaults = dict(is_private=True, is_group=False, is_channel=False,
                    outgoing=False, text="/start", sender_id=12, chat_id=34)
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)

def test_composition():
    m = msg()
    assert (filters.private & filters.text)(m)
    assert (filters.private | filters.group)(m)
    assert (~filters.group)(m)

def test_command():
    assert filters.command("start")(msg())
    assert filters.command(["help", "start"])(msg(text="/start@my_bot"))
    assert not filters.command("help")(msg())

def test_user_chat():
    m = msg()
    assert filters.user(12)(m)
    assert filters.chat([34, 35])(m)
