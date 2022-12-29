import inspect
import re
from pathlib import Path

from pymongo import MongoClient
from telethon import events

from KRISTY import MONGO_DB_URI, telethn

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["KRISTY"]
gbanned = db.gban
