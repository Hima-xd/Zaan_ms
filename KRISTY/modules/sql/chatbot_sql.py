import threading

from sqlalchemy import Column, String

from KRISTY.modules.sql import BASE, SESSION


class aloneChats(BASE):
    __tablename__ = "alone_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


aloneChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_alone(chat_id):
    try:
        chat = SESSION.query(aloneChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_alone(chat_id):
    with INSERTION_LOCK:
        alonechat = SESSION.query(aloneChats).get(str(chat_id))
        if not alonechat:
            alonechat = aloneChats(str(chat_id))
        SESSION.add(alonechat)
        SESSION.commit()


def rem_alone(chat_id):
    with INSERTION_LOCK:
        alonechat = SESSION.query(aloneChats).get(str(chat_id))
        if alonechat:
            SESSION.delete(alonechat)
        SESSION.commit()
