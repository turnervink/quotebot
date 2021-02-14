import discord
import firebase_admin
from firebase_admin import db, credentials

import os

cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
default_app = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://pe-quote-bot.firebaseio.com/",
    "databaseAuthVariableOverride": {
        "uid": os.environ["DB_AUTH_UID"]
    }
})

db_root = db.reference(os.environ["DB_ROOT"])


def get_quotes():
    return db_root.child("quotes").get()


def add_quote(message_id: str, quote: str, author: str, date: str):
    db_root.child("quotes").child(message_id).set({
        "quote": quote,
        "author": author,
        "date": date
    })


def push_quote(quote: str, author: str, date: str):
    db_root.child("quotes").push({
        "quote": quote,
        "author": author,
        "date": date
    })


def get_author(member: discord.Member):
    return db_root.child("authors").child(str(member.id)).get()
