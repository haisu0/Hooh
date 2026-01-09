# ========== BAGIAN 1 ==========
# IMPORT, KONFIG, ACCOUNTS, SETUP DASAR

import asyncio
import os
import re
import mimetypes
import aiohttp
import speech_recognition as sr
from pydub import AudioSegment
from telethon import types
from datetime import datetime
from zoneinfo import ZoneInfo

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetCommonChatsRequest

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, unquote
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.types import InputPhoto
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest

from telethon.tl.functions.account import GetPrivacyRequest, SetPrivacyRequest
from telethon.tl.types import (
    InputPrivacyKeyProfilePhoto, InputPrivacyKeyAbout,
    InputPrivacyValueAllowUsers, InputPrivacyValueDisallowAll
)

import os, mimetypes
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.account import UpdateProfileRequest, GetPrivacyRequest, SetPrivacyRequest
from telethon.tl.types import (
    InputPrivacyKeyProfilePhoto, InputPrivacyKeyAbout,
    InputPrivacyValueDisallowAll, InputPrivacyValueAllowUsers,
    InputPhoto
)




# === KONFIGURASI UTAMA ===
API_ID = 20958475
API_HASH = '1cfb28ef51c138a027786e43a27a8225'

# === DAFTAR AKUN ===
ACCOUNTS = [
    {
        "session": "1BVtsOKgBu1U0o7Ey4oqcQwY-cwZUUrbH7Sg1FmmohHhNqKlg4ZwW0zCgWsqCwPiGGyVqzdrNdY_CKCa64TU5mEAhifyoS1B-Ujcw2xIDgYLRodYVCUoIs2HnPkZg0_tp0Q6zYTO6nR8tqCPAslc2e3-d00lnqW450oVTrNBjnMXQmPt9aHDwETiVJecviMFnkoQG3zdazRZrjevbTm6yJhkJdWuLxiQhv3QSY82eHFBAkVNyFIn0QFVzsUhNuaAvMPBYolh3YPFWMka9eZAJfEdDg7nV6TOIoEvdE56rYhBUheEoPTGB-jwnFS1H_4wQHJMrrpk6gHeAWVUaOVjH1KCINnRwsqo=",
        "log_channel": None,
        "log_admin": 8229706287,
        "features": [
            "anti_view_once",
            "ping",
            "heartbeat",
            "save_media",
            "clearch",
            "whois",
            "downloader",
            "hilih",
            "tictactoe",
            "vn_to_text",
            "tekateki",
            "asahotak",
            "siapakahaku",
            "tebakkata",
            "confess",
            "ai",
            "kuis",
            "tebaklagu",
            "tebakgambar",
            "lengkapikalimat",
            "tebaklirik",
            "caklontong",
            "tebaktebakan",
            "math",
            "susunkata",
            "random",
            "cecan",
        ],
    }
]

# list global client (diisi di main)
clients = []

# waktu start untuk /ping uptime
start_time_global = datetime.now()









async def game_handler(event, client):
    

    games = [
        ("tictactoe", "TicTacToe"),
        ("tekateki", "Teka-teki"),
        ("asahotak", "Asah Otak"),
        ("siapakahaku", "Siapakah Aku"),
        ("tebakkata", "Tebak Kata"),
        ("kuis", "Kuis"),
        ("tebaklagu", "Tebak Lagu"),
        ("tebakgambar", "Tebak Gambar"),
        ("lengkapikalimat", "Lengkapi Kalimat"),
        ("tebaklirik", "Tebak Lirik"),
        ("caklontong", "Cak Lontong"),
        ("tebaktebakan", "Tebak Tebakan"),
        ("math", "Math"),
        ("tebakhewan", "Tebak Hewan"),
        ("susunkata", "Susun Kata"),
    ]

    text = "🎮 **Daftar Game yang tersedia:**\n\n"
    for cmd, name in games:
        text += f"• `{cmd}` → {name}\n"

    text += "\n📌 Cara main: ketik `/namagame` untuk memulai.\n"
    text += "Contoh: `/tictactoe` untuk main TicTacToe."

    await event.respond(text)



import random

CECAN_ENDPOINTS = {
    "china": "https://api.siputzx.my.id/api/r/cecan/china",
    "indonesia": "https://api.siputzx.my.id/api/r/cecan/indonesia",
    "japan": "https://api.siputzx.my.id/api/r/cecan/japan",
    "korea": "https://api.siputzx.my.id/api/r/cecan/korea",
    "thailand": "https://api.siputzx.my.id/api/r/cecan/thailand",
    "vietnam": "https://api.siputzx.my.id/api/r/cecan/vietnam",
}

async def cecan_handler(event, client):
    me = await client.get_me()
    if not event.is_private or event.sender_id != me.id:
        return

    args = event.raw_text.strip().split()
    if len(args) == 1:
        negara, url = random.choice(list(CECAN_ENDPOINTS.items()))
    else:
        negara = args[1].lower()
        url = CECAN_ENDPOINTS.get(negara)
        if not url:
            await event.respond("❌ Negara tidak tersedia.")
            return

    await event.respond(f"📸 Sedang mengambil cecan {negara.capitalize()}...")

    try:
        await client.send_file(
            event.chat_id,
            url,  # langsung pakai link API
            caption=f"✨ Cecan {negara.capitalize()}",
            force_document=False  # penting: kirim sebagai foto
        )
    except Exception as e:
        await event.respond(f"❌ Gagal mengambil cecan: {e}")




# === RANDOM SEMUA (CERDAS CERMAT + TEKA-TEKI + TICTACTOE) ===
async def random_all_handler(event, client):
    pilihan = random.choice([
        ("tictactoe", "TicTacToe"),
        ("tekateki", "Teka-teki"),
        ("asahotak", "Asah Otak"),
        ("siapakahaku", "Siapakah Aku"),
        ("tebakkata", "Tebak Kata"),
        ("kuis", "Kuis"),
        ("tebaklagu", "Tebak Lagu"),
        ("tebakgambar", "Tebak Gambar"),
        ("lengkapikalimat", "Lengkapi Kalimat"),
        ("tebaklirik", "Tebak Lirik"),
        ("caklontong", "Cak Lontong"),
        ("tebaktebakan", "Tebak Tebakan"),
        ("math", "Math"),
        ("tebakhewan", "Tebak Hewan"),
        ("susunkata", "Susun Kata")
    ])

    kode, nama = pilihan
    await event.respond(f"🎲 Random memilih game: **{nama}**")

    if kode == "tictactoe":
        return await tictactoe_handler(event, client)
    elif kode == "tekateki":
        return await tekateki_handler(event, client)
    elif kode == "asahotak":
        return await asahotak_handler(event, client)
    elif kode == "siapakahaku":
        return await siapakahaku_handler(event, client)
    elif kode == "tebakkata":
        return await tebakkata_handler(event, client)
    elif kode == "kuis":
        return await kuis_handler(event, client)
    elif kode == "tebaklagu":
        return await tebaklagu_handler(event, client)
    elif kode == "tebakgambar":
        return await tebakgambar_handler(event, client)
    elif kode == "lengkapikalimat":
        return await lengkapikalimat_handler(event, client)
    elif kode == "tebaklirik":
        return await tebaklirik_handler(event, client)
    elif kode == "caklontong":
        return await caklontong_handler(event, client)
    elif kode == "tebaktebakan":
        return await tebaktebakan_handler(event, client)
    elif kode == "math":
        return await math_handler(event, client)
    elif kode == "tebakhewan":
        return await tebakhewan_handler(event, client)
    elif kode == "susunkata":
        return await susunkata_handler(event, client)



# === CLASS SUSUN KATA ===
class SusunKataGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.soal = None
        self.tipe = None
        self.answer = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        import requests
        url = "https://api.vreden.my.id/api/v1/game/susunkata"
        resp = requests.get(url)
        data = resp.json()
        q = data["result"]
        self.soal = q["soal"]
        self.tipe = q["tipe"]
        self.answer = q["jawaban"].lower().strip()


# === STATE GAME PER CHAT ===
def _ensure_susunkata_state(client, chat_id):
    if not hasattr(client, "susunkata_rooms"):
        client.susunkata_rooms = {}
    if chat_id not in client.susunkata_rooms:
        client.susunkata_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def susunkata_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_susunkata_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.susunkata_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Susun Kata berjalan.\nGunakan /nyerah untuk menyerah.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.susunkata_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Load soal
        await waiting_room["game"].load_question()
        soal = waiting_room["game"].soal
        tipe = waiting_room["game"].tipe

        msg = (f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
               f"🔤 Susun Kata:\n**{soal}**\nTipe: {tipe}\n\n"
               f"⏱ Waktu menjawab: 1 menit\n"
               f"Susun huruf menjadi kata yang benar!")
        await event.respond(msg)

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(
                    f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer.upper()}**"
                )
                try: del client.susunkata_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"susunkata-{chat_id}-{int(datetime.now().timestamp())}"
        game = SusunKataGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.susunkata_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /susunkata untuk join.")


# === HANDLER JAWABAN ===
async def susunkata_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_susunkata_state(client, chat_id)

    room = None
    for r in client.susunkata_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Cek jawaban
    if text == game.answer:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(
            f"✅ Benar!\nJawaban: **{game.answer.upper()}**\n🏆 Pemenang: <b>{winner_label}</b>",
            parse_mode="html"
        )
        try: del client.susunkata_rooms[chat_id][room["id"]]
        except: pass
    else:
        # Jangan balas kalau salah
        return


# === CLASS MATH GAME ===
class MathGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.question = None
        self.choices = {}
        self.answer = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        import requests
        url = "https://api.vreden.my.id/api/v1/game/math"
        resp = requests.get(url)
        data = resp.json()
        q = data["result"]
        self.question = q["question"]
        self.choices = q["choices"]
        self.answer = q["correctAnswer"].lower().strip()
        

# === STATE GAME PER CHAT ===
def _ensure_math_state(client, chat_id):
    if not hasattr(client, "math_rooms"):
        client.math_rooms = {}
    if chat_id not in client.math_rooms:
        client.math_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def math_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_math_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.math_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Math Quiz berjalan.\nGunakan /nyerah untuk menyerah.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.math_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"
        waiting_room["answered"] = {}

        # Load soal
        await waiting_room["game"].load_question()
        soal = waiting_room["game"].question
        choices = waiting_room["game"].choices

        msg = (f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
               f"➗ Math Quiz:\n**{soal}**\n\n"
               f"A. {choices['A']}\nB. {choices['B']}\nC. {choices['C']}\n\n"
               f"⏱ Waktu menjawab: 1 menit\n"
               f"Jawab hanya dengan `a`, `b`, atau `c`.")
        await event.respond(msg)

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(
                    f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer.upper()}**"
                )
                try: del client.math_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"math-{chat_id}-{int(datetime.now().timestamp())}"
        game = MathGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.math_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /math untuk join.")


# === HANDLER JAWABAN ===
async def math_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_math_state(client, chat_id)

    room = None
    for r in client.math_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Hanya playerX/playerO yang boleh menjawab
    if event.sender_id not in (room["playerX"], room["playerO"]):
        return

    # Jawaban hanya a, b, c (case-insensitive)
    if text not in ["a", "b", "c"]:
        return

    if "answered" not in room:
        room["answered"] = {}

    # Cek apakah pemain sudah pernah menjawab
    if event.sender_id in room["answered"]:
        await event.reply("❌ Kamu sudah menjawab sekali, tidak bisa menjawab lagi.")
        return

    # Tandai pemain sudah menjawab
    room["answered"][event.sender_id] = text

    # Jika benar → langsung menang
    if text == game.answer:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(
            f"✅ Benar!\nJawaban: **{game.answer.upper()}**\n🏆 Pemenang: <b>{winner_label}</b>",
            parse_mode="html"
        )
        try: del client.math_rooms[chat_id][room["id"]]
        except: pass
        return

    # Jika salah → kirim pesan salah sambil reply
    await event.reply(f"❌ Jawaban salah: {text.upper()}", reply_to=event.message.id)

    # Jika kedua pemain sudah menjawab (dan tidak ada yang benar) → akhiri room
    pX_done = room["playerX"] in room["answered"]
    pO_done = room["playerO"] in room["answered"]
    if pX_done and pO_done:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        await event.respond(
            f"⏹️ Math Quiz berakhir!\nJawaban yang benar: **{game.answer.upper()}**"
        )
        try: del client.math_rooms[chat_id][room["id"]]
        except: pass



# === CLASS TEBAK TEBAKAN ===
class TebakTebakanGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.question = None
        self.answer = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        import requests
        url = "https://api.vreden.my.id/api/v1/game/tebak/tebakan"
        resp = requests.get(url)
        data = resp.json()
        q = data["result"]
        self.question = q["soal"]
        self.answer = q["jawaban"].lower().strip()


# === STATE GAME PER CHAT ===
def _ensure_tebaktebakan_state(client, chat_id):
    if not hasattr(client, "tebaktebakan_rooms"):
        client.tebaktebakan_rooms = {}
    if chat_id not in client.tebaktebakan_rooms:
        client.tebaktebakan_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def tebaktebakan_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_tebaktebakan_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.tebaktebakan_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Tebak Tebakan berjalan.\nGunakan /nyerah untuk menyerah.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.tebaktebakan_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Load soal
        await waiting_room["game"].load_question()
        soal = waiting_room["game"].question

        msg = (f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
               f"🤔 Tebak Tebakan:\n**{soal}**\n\n"
               f"⏱ Waktu menjawab: 1 menit")
        await event.respond(msg)

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(
                    f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer}**"
                )
                try: del client.tebaktebakan_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"tebaktebakan-{chat_id}-{int(datetime.now().timestamp())}"
        game = TebakTebakanGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.tebaktebakan_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /tebaktebakan untuk join.")


# === HANDLER JAWABAN ===
async def tebaktebakan_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_tebaktebakan_state(client, chat_id)

    room = None
    for r in client.tebaktebakan_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Cek jawaban
    if text == game.answer:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(
            f"✅ Benar!\nJawaban: **{game.answer}**\n🏆 Pemenang: <b>{winner_label}</b>",
            parse_mode="html"
        )
        try: del client.tebaktebakan_rooms[chat_id][room["id"]]
        except: pass
    else:
        # Jangan balas kalau salah
        return



# === CLASS CAK LONTONG ===
class CakLontongGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.question = None
        self.answer = None
        self.desc = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        import requests
        url = "https://api.vreden.my.id/api/v1/game/caklontong"
        resp = requests.get(url)
        data = resp.json()
        q = data["result"]
        self.question = q["soal"]
        self.answer = q["jawaban"].lower().strip()
        self.desc = q.get("deskripsi", "")
        

# === STATE GAME PER CHAT ===
def _ensure_caklontong_state(client, chat_id):
    if not hasattr(client, "caklontong_rooms"):
        client.caklontong_rooms = {}
    if chat_id not in client.caklontong_rooms:
        client.caklontong_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def caklontong_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_caklontong_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.caklontong_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Cak Lontong berjalan.\nGunakan /nyerah untuk menyerah.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.caklontong_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Load soal
        await waiting_room["game"].load_question()
        soal = waiting_room["game"].question

        msg = (f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
               f"🤣 Cak Lontong:\n**{soal}**\n\n"
               f"⏱ Waktu menjawab: 1 menit")
        await event.respond(msg)

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(
                    f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer.upper()}**\nℹ️ {waiting_room['game'].desc}"
                )
                try: del client.caklontong_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"caklontong-{chat_id}-{int(datetime.now().timestamp())}"
        game = CakLontongGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.caklontong_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /caklontong untuk join.")


# === HANDLER JAWABAN ===
async def caklontong_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_caklontong_state(client, chat_id)

    room = None
    for r in client.caklontong_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Cek jawaban
    if text == game.answer:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(
            f"✅ Benar!\nJawaban: **{game.answer.upper()}**\nℹ️ {game.desc}\n🏆 Pemenang: <b>{winner_label}</b>",
            parse_mode="html"
        )
        try: del client.caklontong_rooms[chat_id][room["id"]]
        except: pass
    else:
        # Jangan balas kalau salah
        return



# === CLASS TEBAK LIRIK ===
class TebakLirikGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.question = None
        self.answer = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        import requests
        url = "https://api.vreden.my.id/api/v1/game/tebak/lirik"
        resp = requests.get(url)
        data = resp.json()
        q = data["result"]
        self.question = q["soal"]
        self.answer = q["jawaban"].lower().strip()


# === STATE GAME PER CHAT ===
def _ensure_tebaklirik_state(client, chat_id):
    if not hasattr(client, "tebaklirik_rooms"):
        client.tebaklirik_rooms = {}
    if chat_id not in client.tebaklirik_rooms:
        client.tebaklirik_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def tebaklirik_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_tebaklirik_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.tebaklirik_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Tebak Lirik berjalan.\nGunakan /nyerah untuk menyerah.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.tebaklirik_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Load soal
        await waiting_room["game"].load_question()
        soal = waiting_room["game"].question

        msg = (f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
               f"🎤 Tebak Lirik:\n**{soal}**\n\n"
               f"⏱ Waktu menjawab: 1 menit")
        await event.respond(msg)

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(
                    f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer}**"
                )
                try: del client.tebaklirik_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"tebaklirik-{chat_id}-{int(datetime.now().timestamp())}"
        game = TebakLirikGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.tebaklirik_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /tebaklirik untuk join.")


# === HANDLER JAWABAN ===
async def tebaklirik_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_tebaklirik_state(client, chat_id)

    room = None
    for r in client.tebaklirik_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Cek jawaban
    if text == game.answer:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(
            f"✅ Benar!\nJawaban: **{game.answer}**\n🏆 Pemenang: <b>{winner_label}</b>",
            parse_mode="html"
        )
        try: del client.tebaklirik_rooms[chat_id][room["id"]]
        except: pass
    else:
        # Jangan balas kalau salah
        return



# === CLASS LENGKAPI KALIMAT ===
class LengkapiKalimatGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.question = None
        self.answer = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        import requests
        url = "https://api.vreden.my.id/api/v1/game/lengkapikalimat"
        resp = requests.get(url)
        data = resp.json()
        q = data["result"]
        self.question = q["soal"]
        self.answer = q["jawaban"].lower().strip()


# === STATE GAME PER CHAT ===
def _ensure_lengkapikalimat_state(client, chat_id):
    if not hasattr(client, "lengkapikalimat_rooms"):
        client.lengkapikalimat_rooms = {}
    if chat_id not in client.lengkapikalimat_rooms:
        client.lengkapikalimat_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def lengkapikalimat_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_lengkapikalimat_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.lengkapikalimat_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Lengkapi Kalimat berjalan.\nGunakan /nyerah untuk menyerah.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.lengkapikalimat_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Load soal
        await waiting_room["game"].load_question()
        soal = waiting_room["game"].question

        msg = (f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
               f"✍️ Lengkapi Kalimat:\n**{soal}**\n\n"
               f"⏱ Waktu menjawab: 1 menit")
        await event.respond(msg)

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(
                    f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer}**"
                )
                try: del client.lengkapikalimat_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"lengkapikalimat-{chat_id}-{int(datetime.now().timestamp())}"
        game = LengkapiKalimatGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.lengkapikalimat_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /lengkapikalimat untuk join.")


# === HANDLER JAWABAN ===
async def lengkapikalimat_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_lengkapikalimat_state(client, chat_id)

    room = None
    for r in client.lengkapikalimat_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Cek jawaban
    if text == game.answer:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(
            f"✅ Benar!\nJawaban: **{game.answer}**\n🏆 Pemenang: <b>{winner_label}</b>",
            parse_mode="html"
        )
        try: del client.lengkapikalimat_rooms[chat_id][room["id"]]
        except: pass
    else:
        # Jangan balas kalau salah
        return




# === CLASS TEBAK GAMBAR ===
class TebakGambarGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.img_url = None
        self.answer = None
        self.desc = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        import requests
        url = "https://api.vreden.my.id/api/v1/game/tebak/gambar"
        resp = requests.get(url)
        data = resp.json()
        q = data["result"]
        self.img_url = q["img"]
        self.answer = q["jawaban"].lower().strip()
        self.desc = q.get("deskripsi", "")
        

# === STATE GAME PER CHAT ===
def _ensure_tebakgambar_state(client, chat_id):
    if not hasattr(client, "tebakgambar_rooms"):
        client.tebakgambar_rooms = {}
    if chat_id not in client.tebakgambar_rooms:
        client.tebakgambar_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def tebakgambar_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_tebakgambar_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.tebakgambar_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Tebak Gambar berjalan.\nGunakan /nyerah untuk menyerah.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.tebakgambar_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Load soal
        await waiting_room["game"].load_question()
        img_url = waiting_room["game"].img_url

        # Pesan teks instruksi
        msg_text = (
            f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
            f"🖼️ Tebak Gambar:\n"
            f"⏱ Waktu menjawab: 1 menit\n"
            f"Tebak jawaban dari gambar berikut!"
        )
        await event.respond(msg_text)

        # Kirim gambar langsung
        await client.send_file(chat_id, img_url, caption="🖼️ Silakan tebak gambar ini!")

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(
                    f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer.upper()}**"
                )
                try: del client.tebakgambar_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"tebakgambar-{chat_id}-{int(datetime.now().timestamp())}"
        game = TebakGambarGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.tebakgambar_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /tebakgambar untuk join.")


# === HANDLER JAWABAN ===
async def tebakgambar_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_tebakgambar_state(client, chat_id)

    room = None
    for r in client.tebakgambar_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Cek jawaban
    if text == game.answer:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(
            f"✅ Benar!\nJawaban: **{game.answer.upper()}**\n🏆 Pemenang: <b>{winner_label}</b>",
            parse_mode="html"
        )
        try: del client.tebakgambar_rooms[chat_id][room["id"]]
        except: pass
    else:
        # Jangan balas kalau salah
        return



# === CLASS TEBAK LAGU ===
class TebakLaguGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.song_url = None
        self.answer_title = None
        self.answer_artist = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        import requests
        url = "https://api.vreden.my.id/api/v1/game/tebak/lagu"
        resp = requests.get(url)
        data = resp.json()
        q = data["result"]
        self.song_url = q["lagu"]
        self.answer_title = q["judul"].lower().strip()
        self.answer_artist = q["artis"].lower().strip()


# === STATE GAME PER CHAT ===
def _ensure_tebaklagu_state(client, chat_id):
    if not hasattr(client, "tebaklagu_rooms"):
        client.tebaklagu_rooms = {}
    if chat_id not in client.tebaklagu_rooms:
        client.tebaklagu_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def tebaklagu_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_tebaklagu_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.tebaklagu_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Tebak Lagu berjalan.\nGunakan /nyerah untuk menyerah.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.tebaklagu_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Load soal
        await waiting_room["game"].load_question()
        song_url = waiting_room["game"].song_url

        # Pesan teks instruksi 
        msg_text = ( 
            f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n" 
            f"🎵 Tebak Lagu:\n" 
            f"⏱ Waktu menjawab: 1 menit\n" 
            f"Tebak judul atau artisnya!"
        ) 
        await event.respond(msg_text)
        await client.send_file(chat_id, song_url, caption="🎶 Dengarkan lagunya di sini")

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(
                    f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer_title.title()}** - {waiting_room['game'].answer_artist.title()}"
                )
                try: del client.tebaklagu_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"tebaklagu-{chat_id}-{int(datetime.now().timestamp())}"
        game = TebakLaguGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.tebaklagu_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /tebaklagu untuk join.")


# === HANDLER JAWABAN ===
async def tebaklagu_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_tebaklagu_state(client, chat_id)

    room = None
    for r in client.tebaklagu_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Cek jawaban (judul atau artis)
    if text == game.answer_title or text == game.answer_artist:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(
            f"✅ Benar!\nJawaban: **{game.answer_title.title()}** - {game.answer_artist.title()}\n🏆 Pemenang: <b>{winner_label}</b>",
            parse_mode="html"
        )
        try: del client.tebaklagu_rooms[chat_id][room["id"]]
        except: pass
    else:
        # Jangan balas kalau salah
        return



# === CLASS KUIS ===
class KuisGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.question = None
        self.choices = {}
        self.answer = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        import requests
        url = "https://api.vreden.my.id/api/v1/game/kuis"
        resp = requests.get(url)
        data = resp.json()
        q = data["result"]
        self.question = q["question"]
        self.choices = q["choices"]
        self.answer = q["correctAnswer"].lower().strip()


# === STATE GAME PER CHAT ===
def _ensure_kuis_state(client, chat_id):
    if not hasattr(client, "kuis_rooms"):
        client.kuis_rooms = {}
    if chat_id not in client.kuis_rooms:
        client.kuis_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def kuis_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_kuis_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.kuis_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Kuis berjalan.\nGunakan /nyerah untuk menyerah.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.kuis_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Init answered tracker
        waiting_room["answered"] = {}  # {user_id: 'a'/'b'/'c'}

        # Load soal
        await waiting_room["game"].load_question()
        soal = waiting_room["game"].question
        choices = waiting_room["game"].choices

        msg = (f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
               f"❓ Kuis:\n**{soal}**\n\n"
               f"A. {choices['A']}\nB. {choices['B']}\nC. {choices['C']}\n\n"
               f"⏱ Waktu menjawab: 1 menit\n"
               f"Jawab hanya dengan `a`, `b`, atau `c` (huruf kecil/besar).")
        await event.respond(msg)

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer.upper()}**")
                try: del client.kuis_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"kuis-{chat_id}-{int(datetime.now().timestamp())}"
        game = KuisGame(sender)
        new_room = {
            "id": room_id,
            "game": game,
            "playerX": sender,
            "playerO": None,
            "state": "WAITING"
        }
        client.kuis_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /kuis untuk join.")


# === HANDLER JAWABAN KUIS (satu kesempatan per pemain) ===
async def kuis_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_kuis_state(client, chat_id)

    # Temukan room PLAYING
    room = None
    for r in client.kuis_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Hanya pemain X/O yang boleh menjawab
    if event.sender_id not in (room["playerX"], room["playerO"]):
        return

    # Jawaban hanya a, b, c (case-insensitive)
    if text not in ["a", "b", "c"]:
        return

    # Inisialisasi tracker jika belum ada
    if "answered" not in room:
        room["answered"] = {}

    # Jika room sudah selesai—blok jawaban
    if room["state"] != "PLAYING":
        return

    # Cek apakah pemain sudah pernah menjawab
    if event.sender_id in room["answered"]:
        await event.reply("❌ Kamu sudah menjawab sekali, tidak bisa menjawab lagi.")
        return

    # Tandai pemain sudah menjawab
    room["answered"][event.sender_id] = text

    # Jika benar → langsung menang, akhiri room
    if text == game.answer:
        room["state"] = "FINISHED"
        if game.timeout_task:
            try: game.timeout_task.cancel()
            except: pass
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(
            f"✅ Benar!\nJawaban: **{game.answer.upper()}**\n🏆 Pemenang: <b>{winner_label}</b>",
            parse_mode="html"
        )
        try:
            del client.kuis_rooms[chat_id][room["id"]]
        except:
            pass
        return

    # Jika salah → kirim pesan salah sambil reply ke jawaban
    await event.reply(f"❌ Jawaban salah: {text.upper()}", reply_to=event.message.id)

    # Jika kedua pemain sudah menjawab (dan tidak ada yang benar) → akhiri room, kirim jawaban benar
    pX_done = room["playerX"] in room["answered"]
    pO_done = room["playerO"] in room["answered"]
    if pX_done and pO_done:
        room["state"] = "FINISHED"
        if game.timeout_task:
            try: game.timeout_task.cancel()
            except: pass
        await event.respond(
            f"⏹️ Kuis berakhir!\nJawaban yang benar: **{game.answer.upper()}**"
        )
        try:
            del client.kuis_rooms[chat_id][room["id"]]
        except:
            pass





# === FITUR: AI CHAT ===

async def ai_handler(event, client):
    # hanya aktif di private chat
    if not event.is_private:
        return

    me = await client.get_me()
    if event.sender_id != me.id:
        return

    # Ambil teks dari argumen
    input_text = (event.pattern_match.group(1) or "").strip()

    # Jika reply ke pesan lain
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply:
            # Jika reply adalah media (foto, video, audio, dokumen), tolak
            if reply.media:
                return

            # Ambil isi text dari reply
            if reply.message:
                if input_text:
                    input_text = f"{input_text}\n\n{reply.message.strip()}"
                else:
                    input_text = reply.message.strip()

    if not input_text:
        await event.reply("❌ Harus ada teks atau reply pesan.")
        return

    # 🔄 pesan loading keren
    loading_msg = await event.reply("🤖✨ AI sedang berpikir keras...")

    try:
        # panggil API
        url = f"https://api.siputzx.my.id/api/ai/metaai?query={input_text}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=60) as resp:
                data = await resp.json()

        if data.get("status") and "data" in data:
            output = data["data"]
        else:
            output = "⚠ AI tidak memberikan respon."

        await loading_msg.edit(f"{output}", parse_mode="markdown")

    except Exception as e:
        await loading_msg.edit(f"⚠ Error AI: `{e}`")



async def ai2_handler(event, client):
    # hanya aktif di private chat
    if not event.is_private:
        return

    me = await client.get_me()
    if event.sender_id != me.id:
        return

    # Ambil teks dari argumen
    input_text = (event.pattern_match.group(1) or "").strip()

    # Jika reply ke pesan lain
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply:
            # Jika reply adalah media (foto, video, audio, dokumen), tolak
            if reply.media:
                return

            # Ambil isi text dari reply
            if reply.message:
                if input_text:
                    input_text = f"{input_text}\n\n{reply.message.strip()}"
                else:
                    input_text = reply.message.strip()

    if not input_text:
        await event.reply("❌ Harus ada teks atau reply pesan.")
        return

    # 🔄 pesan loading keren
    loading_msg = await event.reply("🤖✨ AI sedang berpikir keras...")

    try:
        # panggil API
        url = f"https://zelapioffciall.koyeb.app/ai/castorice?text={input_text}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=60) as resp:
                data = await resp.json()

        if data.get("status") and "answer" in data:
            output = data["answer"]
        else:
            output = "⚠ AI tidak memberikan respon."

        await loading_msg.edit(f"{output}", parse_mode="markdown")

    except Exception as e:
        await loading_msg.edit(f"⚠ Error AI: `{e}`")


async def ai3_handler(event, client):
    # hanya aktif di private chat
    if not event.is_private:
        return

    me = await client.get_me()
    if event.sender_id != me.id:
        return

    # Ambil teks dari argumen
    input_text = (event.pattern_match.group(1) or "").strip()

    # Jika reply ke pesan lain
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply:
            # Jika reply adalah media (foto, video, audio, dokumen), tolak
            if reply.media:
                return

            # Ambil isi text dari reply
            if reply.message:
                if input_text:
                    input_text = f"{input_text}\n\n{reply.message.strip()}"
                else:
                    input_text = reply.message.strip()

    if not input_text:
        await event.reply("❌ Harus ada teks atau reply pesan.")
        return

    # 🔄 pesan loading keren
    loading_msg = await event.reply("🤖✨ AI sedang berpikir keras...")

    try:
        # panggil API
        url = f"https://zelapioffciall.koyeb.app/ai/felo?q={input_text}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=60) as resp:
                data = await resp.json()

        if data.get("status") and "result" in data:
            output = data["result"]
            answer = output["answer"]
            
        else:
            answer = "⚠ AI tidak memberikan respon."

        await loading_msg.edit(f"{answer}", parse_mode="markdown")

    except Exception as e:
        await loading_msg.edit(f"⚠ Error AI: `{e}`")


async def ai4_handler(event, client):
    # hanya aktif di private chat
    if not event.is_private:
        return

    me = await client.get_me()
    if event.sender_id != me.id:
        return

    # Ambil teks dari argumen
    input_text = (event.pattern_match.group(1) or "").strip()

    # Jika reply ke pesan lain
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply:
            # Jika reply adalah media (foto, video, audio, dokumen), tolak
            if reply.media:
                return

            # Ambil isi text dari reply
            if reply.message:
                if input_text:
                    input_text = f"{input_text}\n\n{reply.message.strip()}"
                else:
                    input_text = reply.message.strip()

    if not input_text:
        await event.reply("❌ Harus ada teks atau reply pesan.")
        return

    # 🔄 pesan loading keren
    loading_msg = await event.reply("🤖✨ AI sedang berpikir keras...")

    try:
        # panggil API
        url = f"https://zelapioffciall.koyeb.app/ai/kimi?text={input_text}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=60) as resp:
                data = await resp.json()

        if data.get("status") and "result" in data:
            output = data["result"]
            answer = output["response"]
            
        else:
            answer = "⚠ AI tidak memberikan respon."

        await loading_msg.edit(f"{answer}", parse_mode="markdown")

    except Exception as e:
        await loading_msg.edit(f"⚠ Error AI: `{e}`")


async def ai5_handler(event, client):
    # hanya aktif di private chat
    if not event.is_private:
        return

    me = await client.get_me()
    if event.sender_id != me.id:
        return

    # Ambil teks dari argumen
    input_text = (event.pattern_match.group(1) or "").strip()

    # Jika reply ke pesan lain
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply:
            # Jika reply adalah media (foto, video, audio, dokumen), tolak
            if reply.media:
                return

            # Ambil isi text dari reply
            if reply.message:
                if input_text:
                    input_text = f"{input_text}\n\n{reply.message.strip()}"
                else:
                    input_text = reply.message.strip()

    if not input_text:
        await event.reply("❌ Harus ada teks atau reply pesan.")
        return

    # 🔄 pesan loading keren
    loading_msg = await event.reply("🤖✨ AI sedang berpikir keras...")

    try:
        # panggil API
        url = f"https://zelapioffciall.koyeb.app/ai/luminai?text={input_text}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=60) as resp:
                data = await resp.json()

        if data.get("status") and "result" in data:
            output = data["result"]
            
        else:
            output = "⚠ AI tidak memberikan respon."

        await loading_msg.edit(f"{output}", parse_mode="markdown")

    except Exception as e:
        await loading_msg.edit(f"⚠ Error AI: `{e}`")




# ===== FITUR CONFESS =====
import asyncio, random, string
from telethon import events

# State global, dipisahkan per akun (client)
confess_sessions = {}    # {client_id: {user_id: True}}
pending_confess = {}     # {client_id: {msg_id: {"sender": id, "target": id}}}
rooms = {}               # {client_id: {room_id: {"sender": id, "target": id, "messages": [], "expire": task}}}

def gen_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def _init_client_state(client):
    cid = id(client)
    confess_sessions.setdefault(cid, {})
    pending_confess.setdefault(cid, {})
    rooms.setdefault(cid, {})
    return cid

def _user_in_active_room(cid, user_id):
    for rid, room in rooms[cid].items():
        if user_id in (room["sender"], room["target"]):
            return rid
    return None

def _user_has_pending_confess(cid, user_id):
    for mid, data in pending_confess[cid].items():
        if data.get("sender") == user_id or data.get("target") == user_id:
            return True
    return False

async def confess_handler(event, client):
    if not event.is_private:
        return  # hanya aktif di private chat

    text = (event.message.message or "").strip()
    sender_id = event.sender_id
    cid = _init_client_state(client)

    # === /cancel: batalkan sesi pengisian format ===
    if text == "/cancel":
        if confess_sessions[cid].pop(sender_id, None):
            await event.reply("✅ Sesi confess dibatalkan.")
        else:
            await event.reply("ℹ️ Tidak ada sesi confess yang aktif.")
        return

    # === /confess: mulai sesi, blokir jika user sedang aktif/pending ===
    if text == "/confess":
        if _user_in_active_room(cid, sender_id):
            await event.reply("❌ Kamu masih berada di room anonim yang aktif. Selesaikan dulu dengan `/endchat`.")
            return
        if _user_has_pending_confess(cid, sender_id):
            await event.reply("❌ Kamu masih punya confess yang menunggu respon. Tunggu /accept atau /reject.")
            return

        confess_sessions[cid][sender_id] = True
        await event.reply(
            "💌 FORMAT CONFESS\n\n"
            "CONFESS\n"
            "From: (opsional)\n"
            "To:\n"
            "Message:\n\n"
            "Ketik `/cancel` untuk membatalkan sesi."
        )
        return

    # === Isi format confess ===
    if confess_sessions[cid].get(sender_id):
        if not text.startswith("💌 FORMAT CONFESS"):
            await event.reply("❌ Format harus diawali `CONFESS`.\nKetik `/cancel` untuk membatalkan sesi.")
            return

        import re
        to_match = re.search(r'To:\s*(.+)', text, re.I)
        msg_match = re.search(r'Message:\s*([\s\S]+)', text, re.I)
        from_match = re.search(r'From:\s*(.*)', text, re.I)

        to = to_match.group(1).strip() if to_match else None
        body = msg_match.group(1).strip() if msg_match else None
        from_name = from_match.group(1).strip() if from_match else "Anonim"

        if not to or not body:
            await event.reply("❌ `To` atau `Message` belum diisi.\nKetik `/cancel` untuk membatalkan sesi.")
            return

        try:
            entity = await client.get_entity(to)
        except:
            await event.reply("❌ Target tidak ditemukan. Ketik `/cancel` untuk membatalkan sesi.")
            return

        # cek apakah target sedang aktif di room atau pending confess
        if _user_in_active_room(cid, entity.id):
            await event.reply("❌ Target sedang berada di room anonim aktif. Tidak bisa di-confess sekarang.")
            confess_sessions[cid].pop(sender_id, None)
            return
        if _user_has_pending_confess(cid, entity.id):
            await event.reply("❌ Target sedang menerima confess lain. Tunggu sampai selesai.")
            confess_sessions[cid].pop(sender_id, None)
            return

        sent = await client.send_message(
            entity,
            f"💌 Anonymous Confession\n\n"
            f"💬 Dari: {from_name}\n"
            f"━━━━━━━━━━━━━━\n"
            f"{body}\n\n"
            f"Reply pesan ini:\n"
            f"/accept atau /reject"
        )

        pending_confess[cid][sent.id] = {"sender": sender_id, "target": entity.id}
        confess_sessions[cid].pop(sender_id, None)
        await event.reply("✅ Confess terkirim. Tunggu respon target (/accept atau /reject).")
        return

    # === Accept / Reject oleh target ===
    if text in ["/accept", "/reject"] and event.is_reply:
        reply_id = event.message.reply_to_msg_id
        data = pending_confess[cid].get(reply_id)
        if not data:
            return

        if text == "/reject":
            await client.send_message(data["sender"], "❌ Confess ditolak")
            pending_confess[cid].pop(reply_id, None)
            return

        # accept → buat room anonim
        room_id = gen_id()

        async def expire_room():
            await asyncio.sleep(120)  # 1 jam
            room = rooms[cid].get(room_id)
            if room:
                await client.send_message(room["sender"], "⌛ Room berakhir (2 menit)")
                await client.send_message(room["target"], "⌛ Room berakhir (2 menit)")
                rooms[cid].pop(room_id, None)

        task = asyncio.create_task(expire_room())
        rooms[cid][room_id] = {
            "sender": data["sender"],
            "target": data["target"],
            "messages": [],
            "expire": task
        }
        pending_confess[cid].pop(reply_id, None)

        await client.send_message(data["sender"], "💬 Confess diterima. Room dimulai.")
        await event.reply("💬 Room chat anonim dimulai.")
        return

    # === Relay pesan dalam room (ketat) ===
    for rid, room in list(rooms[cid].items()):
        if not event.is_private:
            return  # hanya relay di private chat

        if sender_id == room["sender"]:
            to = room["target"]
        elif sender_id == room["target"]:
            to = room["sender"]
        else:
            continue

        # hanya relay jika chat_id sesuai (private chat dengan bot)
        if event.chat_id not in (room["sender"], room["target"]):
            continue

        room["messages"].append(event.message.id)
        await client.send_message(to, text)
        return

    # === Endchat ===
    if text == "/endchat":
        for rid, room in list(rooms[cid].items()):
            if event.chat_id in (room["sender"], room["target"]):
                try:
                    room["expire"].cancel()
                except:
                    pass
                await client.send_message(room["sender"], "✅ Room selesai")
                await client.send_message(room["target"], "✅ Room selesai")
                rooms[cid].pop(rid, None)
                return
        await event.reply("ℹ️ Tidak ada room anonim aktif untuk diakhiri.")
        return
        





# === CLASS TEBAK KATA ===
class TebakKataGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.question = None
        self.answer = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        url = "https://storage.vynaa.web.id/api/raw?path=game%2Ftebakkata.json"
        resp = requests.get(url)
        data = resp.json()

        # Ambil soal random
        q = random.choice(data)
        self.question = q["soal"]
        self.answer = q["jawaban"].lower().strip()


# === STATE GAME PER CHAT ===
def _ensure_tebak_state(client, chat_id):
    if not hasattr(client, "tebak_rooms"):
        client.tebak_rooms = {}
    if chat_id not in client.tebak_rooms:
        client.tebak_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def tebakkata_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_tebak_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.tebak_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Tebak Kata berjalan.\nGunakan /nyerah untuk mengakhiri.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.tebak_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Load soal
        await waiting_room["game"].load_question()
        soal = waiting_room["game"].question

        msg = (f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
               f"🔤 Tebak Kata:\n**{soal}**\n\n"
               f"⏱ Waktu menjawab: 1 menit")
        await event.respond(msg)

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer}**")
                try: del client.tebak_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"tebakkata-{chat_id}-{int(datetime.now().timestamp())}"
        game = TebakKataGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.tebak_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /tebakkata untuk join.")


# === HANDLER JAWABAN ===
async def tebakkata_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_tebak_state(client, chat_id)

    room = None
    for r in client.tebak_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Cek jawaban
    if text == game.answer.lower():
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(f"✅ Benar!\nJawaban: **{game.answer}**\n🏆 Pemenang: <b>{winner_label}</b>", parse_mode="html")
        try: del client.tebak_rooms[chat_id][room["id"]]
        except: pass
    else:
        # Jangan balas kalau salah
        return



# === CLASS SIAPAKAH AKU ===
class SiapakahAkuGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.question = None
        self.answer = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        url = "https://storage.vynaa.web.id/api/raw?path=game%2Fsiapakahaku.json"
        resp = requests.get(url)
        data = resp.json()

        # Ambil soal random
        q = random.choice(data)
        self.question = q["soal"]
        self.answer = q["jawaban"].lower().strip()


# === STATE GAME PER CHAT ===
def _ensure_siapakah_state(client, chat_id):
    if not hasattr(client, "siapakah_rooms"):
        client.siapakah_rooms = {}
    if chat_id not in client.siapakah_rooms:
        client.siapakah_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def siapakahaku_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_siapakah_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.siapakah_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Siapakah Aku berjalan.\nGunakan /nyerah untuk mengakhiri.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.siapakah_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Load soal
        await waiting_room["game"].load_question()
        soal = waiting_room["game"].question

        msg = (f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
               f"❓ Siapakah Aku:\n**{soal}**\n\n"
               f"⏱ Waktu menjawab: 1 menit")
        await event.respond(msg)

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer}**")
                try: del client.siapakah_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"siapakahaku-{chat_id}-{int(datetime.now().timestamp())}"
        game = SiapakahAkuGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.siapakah_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /siapakahaku untuk join.")


# === HANDLER JAWABAN ===
async def siapakahaku_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_siapakah_state(client, chat_id)

    room = None
    for r in client.siapakah_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Cek jawaban
    if text == game.answer:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(f"✅ Benar!\nJawaban: **{game.answer}**\n🏆 Pemenang: <b>{winner_label}</b>", parse_mode="html")
        try: del client.siapakah_rooms[chat_id][room["id"]]
        except: pass
    else:
        # Jangan balas kalau salah
        return



# === CLASS ASAH OTAK ===
class AsahOtakGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.question = None
        self.answer = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        url = "https://storage.vynaa.web.id/api/raw?path=game%2Fasahotak.json"
        resp = requests.get(url)
        data = resp.json()

        # Ambil soal random
        q = random.choice(data)
        self.question = q["soal"]
        self.answer = q["jawaban"].lower().strip()


# === STATE GAME PER CHAT ===
def _ensure_asah_state(client, chat_id):
    if not hasattr(client, "asah_rooms"):
        client.asah_rooms = {}
    if chat_id not in client.asah_rooms:
        client.asah_rooms[chat_id] = {}


# === HANDLER BUAT / JOIN ROOM ===
async def asahotak_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_asah_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.asah_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada Asah Otak berjalan.\nGunakan /nyerah untuk mengakhiri.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.asah_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Load soal
        await waiting_room["game"].load_question()
        soal = waiting_room["game"].question

        msg = (f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
               f"🧠 Asah Otak:\n**{soal}**\n\n"
               f"⏱ Waktu menjawab: 1 menit")
        await event.respond(msg)

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer}**")
                try: del client.asah_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"asahotak-{chat_id}-{int(datetime.now().timestamp())}"
        game = AsahOtakGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.asah_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /asahotak untuk join.")


# === HANDLER JAWABAN ===
async def asahotak_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_asah_state(client, chat_id)

    room = None
    for r in client.asah_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Cek jawaban
    if text == game.answer:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(f"✅ Benar!\nJawaban: **{game.answer}**\n🏆 Pemenang: <b>{winner_label}</b>", parse_mode="html")
        try: del client.asah_rooms[chat_id][room["id"]]
        except: pass
    else:
        # Jangan balas kalau salah
        return



# === CLASS TEKA TEKI ===
class TekaTekiGame:
    def __init__(self, player_x):
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.question = None
        self.answer = None
        self.names = {player_x: "Pembuat room"}
        self.timeout_task = None

    async def load_question(self):
        url = "https://storage.vynaa.web.id/api/raw?path=game%2Ftekateki.json"
        resp = requests.get(url)
        data = resp.json()

        # Ambil hanya item yang valid
        valid_items = [item["data"] for item in data if item.get("status") and "data" in item]
        q = random.choice(valid_items)

        self.question = q["pertanyaan"]
        self.answer = q["jawaban"].lower().strip()


# === STATE GAME PER CHAT ===
def _ensure_teka_state(client, chat_id):
    if not hasattr(client, "teka_rooms"):
        client.teka_rooms = {}
    if chat_id not in client.teka_rooms:
        client.teka_rooms[chat_id] = {}


# === HANDLER BUAT  JOIN ROOM ===
async def tekateki_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_teka_state(client, chat_id)

    # Cek apakah sudah ada room PLAYING
    for r in client.teka_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada teka-teki berjalan.\nGunakan /nyerah untuk mengakhiri.")
            return

    # Cari room waiting
    waiting_room = None
    for r in client.teka_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Kamu sudah membuat room ini. Tunggu partner join.")
            return

        # Join sebagai Partner
        waiting_room["game"].playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        waiting_room["game"].names[sender] = "Partner"

        # Load soal
        await waiting_room["game"].load_question()
        soal = waiting_room["game"].question

        msg = (f"Partner ditemukan!\nRoom ID: {waiting_room['id']}\n\n"
               f"🧩 Teka-Teki:\n**{soal}**\n\n"
               f"⏱ Waktu menjawab: 1 menit")
        await event.respond(msg)

        # Set timeout 1 menit
        async def timeout_answer():
            await asyncio.sleep(60)
            if waiting_room["state"] == "PLAYING":
                waiting_room["state"] = "FINISHED"
                await event.respond(f"⏰ Waktu habis!\nJawaban: **{waiting_room['game'].answer}**")
                try: del client.teka_rooms[chat_id][waiting_room["id"]]
                except: pass

        waiting_room["game"].timeout_task = asyncio.create_task(timeout_answer())

    else:
        # Buat room baru
        room_id = f"tekateki-{chat_id}-{int(datetime.now().timestamp())}"
        game = TekaTekiGame(sender)
        new_room = {"id": room_id,"game": game,"playerX": sender,
                    "playerO": None,"state": "WAITING"}
        client.teka_rooms[chat_id][room_id] = new_room
        await event.respond("Menunggu partner join...\nGunakan /tekateki untuk join.")


# === HANDLER JAWABAN ===
async def tekateki_answer_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()
    _ensure_teka_state(client, chat_id)

    room = None
    for r in client.teka_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    # Cek jawaban
    if text == game.answer:
        room["state"] = "FINISHED"
        if game.timeout_task:
            game.timeout_task.cancel()
        winner_label = game.names.get(event.sender_id, str(event.sender_id))
        await event.reply(f"✅ Benar!\nJawaban: **{game.answer}**\n🏆 Pemenang: <b>{winner_label}</b>", parse_mode="html")
        try: del client.teka_rooms[chat_id][room["id"]]
        except: pass
    else:
        # Jangan balas kalau salah
        return




# === FITUR: VN TO TEXT (Reply Only, SpeechRecognition) === 
import os
import speech_recognition as sr
from pydub import AudioSegment
import asyncio

async def vn_to_text_handler(event, client, log_channel=None, log_admin=None):
    if not event.is_private:
        return

    if not event.is_reply:
        await event.reply("❌ Harus reply ke VN/audio dengan `/stt`")
        return

    reply = await event.get_reply_message()
    if not reply.voice and not reply.audio:
        await event.reply("❌ Reply harus ke voice note/audio")
        return

    # 🔄 kirim pesan loading
    loading_msg = await event.reply("🎙 Sedang mengubah VN ke teks...")

    try:
        folder = "111VNtoText"
        os.makedirs(folder, exist_ok=True)
        file_path = await reply.download_media(file=folder)

        wav_path = file_path + ".wav"

        # Jalankan konversi audio di thread terpisah
        await asyncio.to_thread(AudioSegment.from_file(file_path).export, wav_path, format="wav")

        # Jalankan speech recognition di thread terpisah
        recognizer = sr.Recognizer()
        def recognize():
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio_data, language="id-ID")
            except sr.UnknownValueError:
                return "Tidak bisa mengenali suara"
            except sr.RequestError as e:
                return f"Error API: {e}"

        text = await asyncio.to_thread(recognize)

        caption = (
            "🎙 **VN → Text**\n\n"
            f"📝 {text}"
        )
        await loading_msg.edit(caption, parse_mode="markdown")

        # Bersihkan file
        for f in [file_path, wav_path]:
            if f and os.path.exists(f):
                os.remove(f)

    except Exception as e:
        await loading_msg.edit(f"⚠ Error VN→Text: `{e}`", parse_mode="markdown")
        






# === FITUR: HILIH ===
async def hilih_handler(event, client):
    if not event.is_private:
        return
    me = await client.get_me()
    if event.sender_id != me.id:
        return

    # Ambil teks dari argumen atau reply
    input_text = event.pattern_match.group(2).strip() if event.pattern_match.group(2) else ''
    if event.is_reply and not input_text:
        reply = await event.get_reply_message()
        if reply and reply.message:
            input_text = reply.message.strip()

    if not input_text:
        await event.reply("❌ Harus ada teks atau reply pesan.")
        return

    target = event.pattern_match.group(1).lower() if event.pattern_match.group(1) else 'i'

    def replace_vowels(text, t):
        vokal = "aiueo"
        res = []
        for ch in text:
            if ch.lower() in vokal:
                res.append(t.upper() if ch.isupper() else t)
            else:
                res.append(ch)
        return "".join(res)

    output = replace_vowels(input_text, target)
    await event.reply(output)



from telethon import events
from datetime import datetime
import random

# === CLASS TIC TAC TOE ===
class TicTacToe:
    def __init__(self, player_x):
        self.board = [str(i) for i in range(1, 10)]
        self.playerX = player_x
        self.playerO = None
        self.currentTurn = player_x
        self.winner = None
        self.names = {player_x: "Pembuat room"}
        self.moves = {"X": [], "O": []}

        # === PILIH PAPAN SECARA RANDOM (1X SAJA) ===
        self.board_style = random.choice([1, 2])

    # Emoji mapping
    def render(self):
        mapping = {
            "X": "❌", "O": "⭕",
            "1": "1️⃣","2": "2️⃣","3": "3️⃣",
            "4": "4️⃣","5": "5️⃣","6": "6️⃣",
            "7": "7️⃣","8": "8️⃣","9": "9️⃣",
        }
        return [mapping.get(v, v) for v in self.board]

    # === BOARD STYLE 1 ===
    def render_board_box(self):
        arr = self.render()
        return (
            "┌────┬────┬────┐\n"
            f"│   {arr[0]}    │   {arr[1]}   │   {arr[2]}    │\n"
            "├────┼────┼────┤\n"
            f"│   {arr[3]}    │   {arr[4]}   │   {arr[5]}    │\n"
            "├────┼────┼────┤\n"
            f"│   {arr[6]}    │   {arr[7]}   │   {arr[8]}    │\n"
            "└────┴────┴────┘"
        )

    # === BOARD STYLE 2 (YANG BARU) ===
    def render_board_box_style2(self):
        arr = self.render()
        return (
            "╔════╦════╦════╗\n"
            f"║   {arr[0]}    ║   {arr[1]}   ║   {arr[2]}    ║\n"
            "╠════╬════╬════╣\n"
            f"║   {arr[3]}    ║   {arr[4]}   ║   {arr[5]}    ║\n"
            "╠════╬════╬════╣\n"
            f"║   {arr[6]}    ║   {arr[7]}   ║   {arr[8]}    ║\n"
            "╚════╩════╩════╝"
        )

    # === RENDER UTAMA (DISPATCHER) ===
    def render_board(self):
        if self.board_style == 1:
            return self.render_board_box()
        else:
            return self.render_board_box_style2()

    def move(self, player, pos):
        if pos < 1 or pos > 9:
            return False

        mark = "X" if player == self.playerX else "O"

        if self.board[pos - 1] in ["X", "O"]:
            return False

        self.moves[mark].append(pos)

        if len(self.moves[mark]) > 3:
            removed = self.moves[mark].pop(0)
            self.board[removed - 1] = str(removed)

        self.board[pos - 1] = mark
        self.currentTurn = self.playerO if player == self.playerX else self.playerX
        self.check_winner()
        return True

    def check_winner(self):
        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] in ["X","O"]:
                self.winner = self.board[a]
                return self.winner
        return None


# === GAME STATE PER CHAT ===
def _ensure_game_state(client, chat_id):
    if not hasattr(client, "game_rooms"):
        client.game_rooms = {}
    if chat_id not in client.game_rooms:
        client.game_rooms[chat_id] = {}


# === HANDLER /tictactoe ===
async def tictactoe_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id
    _ensure_game_state(client, chat_id)

    # Cek game berjalan
    for r in client.game_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            await event.respond("❌ Sudah ada game berjalan.\nGunakan /nyerah dulu.")
            return

    waiting_room = None
    for r in client.game_rooms[chat_id].values():
        if r["state"] == "WAITING":
            waiting_room = r
            break

    if waiting_room:
        if sender == waiting_room["playerX"]:
            await event.respond("❌ Tunggu partner lain.")
            return

        game = waiting_room["game"]
        game.playerO = sender
        waiting_room["playerO"] = sender
        waiting_room["state"] = "PLAYING"
        game.names[sender] = "Partner"

        game.currentTurn = random.choice([waiting_room["playerX"], sender])
        board = game.render_board()
        turn = game.names[game.currentTurn]

        await event.respond(
            f"🎮 Partner ditemukan!\n\n{board}\n\nGiliran: <b>{turn}</b>",
            parse_mode="html"
        )

    else:
        room_id = f"tictactoe-{chat_id}-{int(datetime.now().timestamp())}"
        game = TicTacToe(sender)
        client.game_rooms[chat_id][room_id] = {
            "id": room_id,
            "game": game,
            "playerX": sender,
            "playerO": None,
            "state": "WAITING"
        }
        await event.respond("⌛ Menunggu partner join...\nGunakan /tictactoe untuk join.")


# === HANDLER LANGKAH 1–9 ===
async def tictactoe_move_handler(event, client):
    chat_id = event.chat_id
    text = event.raw_text.strip()

    if text not in [str(i) for i in range(1, 10)]:
        return

    _ensure_game_state(client, chat_id)

    room = None
    for r in client.game_rooms[chat_id].values():
        if r["state"] == "PLAYING":
            room = r
            break
    if not room:
        return

    game = room["game"]

    if event.sender_id != game.currentTurn:
        await event.reply("❌ Bukan giliran kamu.")
        return

    if not game.move(event.sender_id, int(text)):
        await event.reply("❌ Posisi tidak valid.")
        return

    board = game.render_board()

    if game.winner:
        winner = game.names[room["playerX"]] if game.winner == "X" else game.names[room["playerO"]]
        await event.reply(f"{board}\n\n🏆 Pemenang: <b>{winner}</b>", parse_mode="html")
        del client.game_rooms[chat_id][room["id"]]
    else:
        turn = game.names[game.currentTurn]
        await event.reply(f"{board}\n\nGiliran: <b>{turn}</b>", parse_mode="html")





# === HANDLER MENYERAH (gabungan semua game) ===
async def surrender_room_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id

    # List semua state dict per game
    state_attrs = [
        ("tictactoe", "game_rooms"),
        ("tekateki", "teka_rooms"),
        ("asahotak", "asah_rooms"),
        ("siapakahaku", "siapakah_rooms"),
        ("tebakkata", "tebak_rooms"),
        ("kuis", "kuis_rooms"),
        ("tebaklagu", "tebaklagu_rooms"),
        ("tebakgambar", "tebakgambar_rooms"),
        ("lengkapikalimat", "lengkapikalimat_rooms"),
        ("tebaklirik", "tebaklirik_rooms"),
        ("caklontong", "caklontong_rooms"),
        ("tebaktebakan", "tebaktebakan_rooms"),
        ("math", "math_rooms"),
        ("susunkata", "susunkata_rooms"),
    ]

    found_room = None
    found_game = None

    for game_name, attr in state_attrs:
        if hasattr(client, attr) and chat_id in getattr(client, attr):
            rooms = getattr(client, attr)[chat_id]
            for r in rooms.values():
                if r["state"] == "PLAYING":
                    found_room = r
                    found_game = game_name
                    break
        if found_room:
            break

    if not found_room:
        await event.respond("❌ Tidak ada game yang sedang dimainkan untuk diserahkan.")
        return

    game = found_room["game"]
    opponent = game.playerO if sender == game.playerX else game.playerX
    found_room["state"] = "FINISHED"
    try:
        del getattr(client, state_attrs[[g for g, a in state_attrs].index(found_game)][1])[chat_id][found_room["id"]]
    except:
        pass

    loser_label = game.names.get(sender, str(sender))
    winner_label = game.names.get(opponent, str(opponent))
    await event.respond(
        f"🏳️ Pemain <b>{loser_label}</b> menyerah!\n\n"
        f"🏆 Pemenang otomatis: <b>{winner_label}</b>\n"
        f"🎮 Game: {found_game}",
        parse_mode="html"
    )

# === HANDLER BATALKAN ROOM (gabungan semua game) ===
async def cancel_room_handler(event, client):
    chat_id = event.chat_id
    sender = event.sender_id

    # List semua state dict per game
    state_attrs = [
        ("tictactoe", "game_rooms"),
        ("tekateki", "teka_rooms"),
        ("asahotak", "asah_rooms"),
        ("siapakahaku", "siapakah_rooms"),
        ("tebakkata", "tebak_rooms"),
        ("kuis", "kuis_rooms"),
        ("tebaklagu", "tebaklagu_rooms"),
        ("tebakgambar", "tebakgambar_rooms"),
        ("lengkapikalimat", "lengkapikalimat_rooms"),
        ("tebaklirik", "tebaklirik_rooms"),
        ("caklontong", "caklontong_rooms"),
        ("tebaktebakan", "tebaktebakan_rooms"),
        ("math", "math_rooms"),
        ("susunkata", "susunkata_rooms"),
    ]

    found_room = None
    found_game = None

    for game_name, attr in state_attrs:
        if hasattr(client, attr) and chat_id in getattr(client, attr):
            rooms = getattr(client, attr)[chat_id]
            for r in rooms.values():
                if r["state"] == "WAITING":
                    found_room = r
                    found_game = game_name
                    break
        if found_room:
            break

    if not found_room:
        await event.respond("❌ Tidak ada room yang bisa dibatalkan.")
        return

    # Validasi pembuat room
    if sender != found_room["playerX"]:
        await event.respond("❌ Hanya pembuat room yang bisa membatalkan.")
        return

    if found_room.get("playerO"):
        await event.respond("❌ Room sudah ada partner. Tidak bisa dibatalkan, gunakan /nyerah jika ingin berhenti.")
        return

    try:
        del getattr(client, state_attrs[[g for g, a in state_attrs].index(found_game)][1])[chat_id][found_room["id"]]
    except:
        pass

    await event.respond(f"❌ Room {found_game} dibatalkan oleh pembuat.")







# === Fungsi Normalisasi ===
def normalize_text(text: str) -> str:
    # ubah huruf berulang jadi satu
    return re.sub(r'(.)\1+', r'\1', text.lower()).strip()

# === FITUR: AUTO FORWARD SPAM ===
async def auto_forward_spam(event, client, spam_config):
    if not event.is_private:
        return

    msg_text = normalize_text(event.message.message or "")

    # === GLOBAL TRIGGERS (string) ===
    global_triggers = [normalize_text(t) for t in spam_config if isinstance(t, str)]
    if any(trigger in msg_text for trigger in global_triggers):
        sender = await event.get_sender()
        sender_id = sender.id
        for _ in range(10):
            try:
                await client.forward_messages(sender_id, event.message)
                await asyncio.sleep(0.3)
            except:
                break
        return

    # === PER-CHAT TRIGGERS (dict) ===
    for entry in spam_config:
        if isinstance(entry, dict):
            if entry.get("chat_id") == event.chat_id:
                chat_triggers = [normalize_text(t) for t in entry.get("triggers", [])]
                if any(trigger in msg_text for trigger in chat_triggers):
                    sender = await event.get_sender()
                    sender_id = sender.id
                    for _ in range(10):
                        try:
                            await client.forward_messages(sender_id, event.message)
                            await asyncio.sleep(0.3)
                        except:
                            break
                    return
                  
# === FITUR: AUTO-PIN ===
async def autopin_handler(event, client, autopin_config):
    if not event.is_private:
        return

    text = normalize_text(event.message.message or "")

    # === GLOBAL KEYWORDS ===
    global_keywords = [normalize_text(kw) for kw in autopin_config if isinstance(kw, str)]
    if any(keyword in text for keyword in global_keywords):
        try:
            await client.pin_message(event.chat_id, event.message.id)
        except:
            pass
        return

    # === PER-CHAT KEYWORDS ===
    for entry in autopin_config:
        if isinstance(entry, dict):
            if entry.get("chat_id") == event.chat_id:
                chat_keywords = [normalize_text(kw) for kw in entry.get("keywords", [])]
                if any(keyword in text for keyword in chat_keywords):
                    try:
                        await client.pin_message(event.chat_id, event.message.id)
                    except:
                        pass
                    return




# === FITUR: ANTI VIEW-ONCE ===
async def anti_view_once_and_ttl(event, client, log_channel, log_admin):
    if not event.is_private:
        return

    msg = event.message
    ttl = getattr(msg.media, "ttl_seconds", None)

    if not msg.media or not ttl:
        return

    try:
        sender = await msg.get_sender()
        sender_name = sender.first_name or "Unknown"
        sender_username = f"@{sender.username}" if sender.username else "-"
        sender_id = sender.id

        chat = await event.get_chat()
        chat_title = getattr(chat, "title", "Private Chat")
        chat_id = chat.id

        caption = (
            "🔓 **MEDIA VIEW-ONCE / TIMER TERTANGKAP**\n\n"
            f"👤 **Pengirim:** `{sender_name}`\n"
            f"🔗 **Username:** {sender_username}\n"
            f"🆔 **User ID:** `{sender_id}`\n\n"
            f"💬 **Dari Chat:** `{chat_title}`\n"
            f"🆔 **Chat ID:** `{chat_id}`\n\n"
            f"⏱ **Timer:** `{ttl} detik`\n"
            f"📥 **Status:** Berhasil disalin ✅"
        )

        folder = "111AntiViewOnce"
        os.makedirs(folder, exist_ok=True)
        file = await msg.download_media(file=folder)

        if log_channel:
            await client.send_file(log_channel, file, caption=caption)
        if log_admin:
            await client.send_file(log_admin, file, caption=caption)

        if file and os.path.exists(file):
            os.remove(file)

    except Exception as e:
        if log_admin:
            await client.send_message(log_admin, f"⚠ Error anti-viewonce: `{e}`")

# === FITUR: PING ===
async def ping_handler(event, client):
    if not event.is_private:
        return

    try:
        start = datetime.now()
        msg = await event.reply("⏳ Pinging...")
        end = datetime.now()

        ms = (end - start).microseconds // 1000
        uptime = datetime.now() - start_time_global
        uptime_str = str(uptime).split('.')[0]

        me = await client.get_me()
        akun_nama = me.first_name or "Akun"

        # Status emoji
        if ms < 30:
            status = "⚡️ Ultra Instan" 
        elif ms < 75:
            status = "💨 Super Cepat"
        elif ms < 150:
            status = "🟢 Cepat Stabil"
        elif ms < 250:
            status = "🟡 Cukup Lancar"
        elif ms < 400:
            status = "🟠 Agak Berat"
        elif ms < 700:
            status = "🔴 Sangat Lambat"
        else:
            status = "⚫️ Nyaris Down"

        text = (
            f"🏓 **PONG!** 🏓\n\n"
            f"⚡ Latency: `{ms} ms`\n"
            f"👤 **Akun:** {akun_nama}\n"
            f"⏱ **Uptime:** `{uptime_str}`\n"
            f"📡 **Status:** {status}\n"
            f"🕒 **Server:** {datetime.now(ZoneInfo('Asia/Jakarta')).strftime('%H:%M:%S || %d-%m-%Y')}"
        )

        await msg.edit(text)

    except Exception as e:
        await event.reply(f"⚠ Error /ping: `{e}`")


# === FITUR: HEARTBEAT ===
async def heartbeat(client, log_admin, log_channel, akun_nama):
    last_msg_id = None
    start_time = datetime.now()

    while True:
        try:
            uptime = datetime.now() - start_time
            uptime_str = str(uptime).split('.')[0]
            server_time = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%H:%M:%S || %d-%m-%Y")

            start = datetime.now()
            end = datetime.now()
            ms = (end - start).microseconds // 1000
            
            # Status emoji
            if ms < 30:
                status = "⚡️ Ultra Instan" 
            elif ms < 75:
                status = "💨 Super Cepat"
            elif ms < 150:
                status = "🟢 Cepat Stabil"
            elif ms < 250:
                status = "🟡 Cukup Lancar"
            elif ms < 400:
                status = "🟠 Agak Berat"
            elif ms < 700:
                status = "🔴 Sangat Lambat"
            else:
                status = "⚫️ Nyaris Down"


            if last_msg_id:
                try:
                    if log_admin:
                        await client.delete_messages(log_admin, last_msg_id)
                except:
                    pass

            text = (
                f"💓 **HEARTBEAT CHECK** 💓\n\n"
                f"👤 Akun: {akun_nama}\n"
                f"⏱ Uptime: `{uptime_str}`\n"
                f"📡 **Status:** {status}\n"
                f"🕒 Server: {server_time}\n"
            )

            msg = None
            if log_admin:
                msg = await client.send_message(log_admin, text)

            if msg:
                last_msg_id = msg.id

        except Exception as e:
            if log_admin:
                await client.send_message(log_admin, f"⚠ Heartbeat Error: `{e}`")

        await asyncio.sleep(300)

# === FITUR SAVE MEDIA ===
link_regex = re.compile(
    r'(?:https?://)?t\.me/(c/\d+|[a-zA-Z0-9_]+)/(\d+)(?:\?.*?)?',
    re.IGNORECASE
)

async def process_link(event, client, chat_part, msg_id, target_chat=None):
    if not event.is_private:
        return
    
    me = await client.get_me()
    if event.sender_id != me.id:
        return

    from telethon.errors import (
        RPCError,
        ChannelPrivateError,
        ChannelInvalidError,
        MessageIdInvalidError,
        UserNotParticipantError
    )

    try:
        # Proses chat ID
        if chat_part.startswith("c/"):
            internal_id = chat_part[2:]
            chat_id = int(f"-100{internal_id}")

            try:
                await client.get_permissions(chat_id, 'me')
            except:
                await event.reply(f"🚫 Ubot belum join channel `{chat_part}`.")
                return

        else:
            try:
                entity = await client.get_entity(chat_part)
                chat_id = entity.id
            except:
                await event.reply(f"❌ Channel/grup `{chat_part}` tidak ditemukan.")
                return

        message = await client.get_messages(chat_id, ids=msg_id)
        if not message:
            await event.reply(f"❌ Pesan {msg_id} tidak ditemukan.")
            return

        send_to = target_chat or event.chat_id  # Tentukan chat target atau chat tempat command digunakan
        
        # === PATCH: cek kalau media adalah sticker ===
        if message.media and message.sticker:
            await client.send_file(
                send_to,
                message.media,
                force_document=False  # penting agar tetap sticker (termasuk .tgs animasi)
            )
            return  # selesai, jangan lanjut ke grouped_id

        grouped_id = message.grouped_id
        if grouped_id:
            all_msgs = await client.get_messages(chat_id, limit=200)
            same_group = [m for m in all_msgs if m.grouped_id == grouped_id]
            same_group.sort(key=lambda m: m.id)

            files = []
            first_caption = None
            first_buttons = None

            for m in same_group:
                if first_caption is None and (m.message or m.raw_text):
                    first_caption = m.message or m.raw_text

                if first_buttons is None:
                    first_buttons = getattr(m, "buttons", None)

                if m.media:
                    fpath = await client.download_media(m.media)
                    files.append(fpath)
                else:
                    if m.message:
                        await client.send_message(send_to, m.message)

            if files:
                await client.send_file(
                    send_to,
                    files,
                    caption=first_caption or "",
                    buttons=first_buttons,
                    link_preview=False
                )
                for f in files:
                    try:
                        os.remove(f)
                    except:
                        pass

        else:
            buttons = getattr(message, "buttons", None)
            text = message.message or ""

            if message.media:
                fpath = await client.download_media(message.media)
                await client.send_file(
                    send_to,
                    fpath,
                    caption=text,
                    buttons=buttons,
                    link_preview=False
                )
                try:
                    os.remove(fpath)
                except:
                    pass
            else:
                await client.send_message(send_to, text, buttons=buttons)

    except Exception as e:
        await event.reply(f"🚨 Error: `{e}`")


async def handle_save_command(event, client):
    if not event.is_private:
        return
    
    me = await client.get_me()
    if event.sender_id != me.id:
        return
    
    input_text = event.pattern_match.group(2).strip() if event.pattern_match.group(2) else ''
    reply = await event.get_reply_message() if event.is_reply else None

    target_chat = event.chat_id  # Default: chat tempat command digunakan
    links_part = input_text

    # === Cek input yang hanya chat target ===
    if input_text and (re.match(r'^@?[a-zA-Z0-9_]+$', input_text) or re.match(r'^-?\d+$', input_text)):
        target_chat_raw = input_text
        target_chat = int(target_chat_raw) if target_chat_raw.lstrip("-").isdigit() else target_chat_raw
        
        # Ambil link dari reply, bukan dari input_text
        if reply and reply.message:
            links_part = reply.message.strip()
        else:
            await event.reply("❌ Harus reply pesan berisi link kalau cuma kasih target chat.")
            return

    # === Kalau input kosong tapi ada reply ===
    if not links_part and reply and reply.message:
        links_part = reply.message.strip()

    # === Ambil semua link ===
    matches = link_regex.findall(links_part)
    if not matches:
        await event.reply("❌ Tidak ada link valid.")
        return

    loading = await event.reply(f"⏳ Memproses {len(matches)} link...")

    for chat_part, msg_id in matches:
        # Cek apakah ada target chat, jika ada, kirim ke sana
        if target_chat and chat_part and msg_id:
            await process_link(event, client, chat_part, int(msg_id), target_chat)
        else:
            await process_link(event, client, chat_part, int(msg_id), target_chat)

    try:
        await loading.delete()
    except:
        pass
        
# === FITUR: CLEAR CHANNEL ===
async def clearch_handler(event, client):
    chat = await event.get_chat()

    if not getattr(chat, "broadcast", False):
        await event.reply("❌ /clearch hanya bisa dipakai di **channel**, bukan grup.")
        return

    perms = await client.get_permissions(chat, 'me')
    if not perms.is_admin or not perms.delete_messages:
        await event.reply("❌ Ubot tidak punya izin **delete messages** di channel ini.")
        return

    await event.reply("🧹 Menghapus semua pesan di channel...")

    async for msg in client.iter_messages(chat.id):
        try:
            await msg.delete()
        except:
            pass

    await client.send_message(chat.id, "✅ Semua pesan berhasil dihapus.")

# === FITUR: WHOIS ===
async def whois_handler(event, client):
    if not event.is_private:
        return

    if not event.is_reply:
        await event.reply("❌ Reply pesan user yang ingin kamu cek.")
        return

    reply = await event.get_reply_message()
    user = await client.get_entity(reply.sender_id)

    try:
        full = await client(GetFullUserRequest(user.id))
        bio = full.full_user.about or "-"
    except Exception as e:
        bio = f"⚠ Tidak bisa ambil bio: {e}"

    # Informasi dasar
    phone = getattr(user, "phone", None)
    phone = f"+{phone}" if phone and not phone.startswith("+") else (phone or "-")
    dc_id = getattr(user, "dc_id", "-")
    verified = "Ya" if getattr(user, "verified", False) else "Tidak"
    scam = "Ya" if getattr(user, "scam", False) else "Tidak"
    restricted = "Ya" if getattr(user, "restricted", False) else "Tidak"
    premium = "Ya" if getattr(user, "premium", False) else "Tidak"
    fullname = f"{user.first_name or '-'} {user.last_name or ''}".strip()
    username = f"@{user.username}" if user.username else "-"

    # Status / Last Seen
    status_text = "-"
    if hasattr(user, "status") and user.status:
        cname = user.status.__class__.__name__
        if cname == "UserStatusOffline":
            last_seen = user.status.was_online
            if last_seen:
                local_time = last_seen.astimezone(ZoneInfo("Asia/Jakarta"))
                status_text = local_time.strftime("%H:%M:%S || %d-%m-%Y")
        elif cname == "UserStatusOnline":
            status_text = "Sedang online"
        elif cname == "UserStatusRecently":
            status_text = "Baru saja online"
        elif cname == "UserStatusLastWeek":
            status_text = "Online minggu lalu"
        elif cname == "UserStatusLastMonth":
            status_text = "Online bulan lalu"
        else:
            status_text = cname.replace("UserStatus", "")

    # Grup bersama
    try:
        common = await client(GetCommonChatsRequest(user_id=user.id, max_id=0, limit=100))
        common_count = len(common.chats)
    except Exception as e:
        common_count = f"⚠ Error ambil grup bersama: {e}"

    # Format teks
    text = (
        f"👤 **WHOIS USER**\n\n"
        f"🆔 ID: `{user.id}`\n"
        f"👥 Nama: {fullname}\n"
        f"🔗 Username: {username}\n"
        f"📞 Phone: {phone}\n"
        f"📖 Bio: {bio}\n"
        f"🏛️ DC ID: {dc_id}\n"
        f"🤖 Bot: {'Ya' if user.bot else 'Tidak'}\n"
        f"🚷 Scam: {scam}\n"
        f"🚫 Restricted: {restricted}\n"
        f"✅ Verified: {verified}\n"
        f"⭐ Premium: {premium}\n"
        f"👁️ Last Seen: {status_text}\n"
        f"👀 Same Groups: {common_count}\n"
        f"🔗 Permanent Link: [Klik di sini](tg://user?id={user.id})\n"
    )


    # Ambil foto profil
    try:
        photos = await client.get_profile_photos(user.id, limit=10)
        files = []
        for p in photos:
            fpath = await client.download_media(p)
            files.append(fpath)

        if files:
            await client.send_file(
                event.chat_id,
                files,
                caption=text,
                link_preview=False
            )
            for f in files:
                try:
                    os.remove(f)
                except:
                    pass
        else:
            await event.reply(text, link_preview=False)
    except Exception as e:
        await event.reply(f"{text}\n\n⚠ Error ambil foto profil: {e}")


# === FITUR: DOWNLOADER ===
def is_valid_url(url):
    """Validasi apakah string adalah URL yang valid"""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

def sanitize_url(url):
    """Membersihkan URL dari tracking parameters"""
    try:
        parsed = urlparse(url)
        tracking_params = ["utm_source", "utm_medium", "utm_campaign", "fbclid", "gclid", "_gl"]
        query_params = parse_qs(parsed.query)
        for param in tracking_params:
            query_params.pop(param, None)
        
        clean_query = urlencode(query_params, doseq=True)
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if clean_query:
            clean_url += f"?{clean_query}"
        return clean_url.strip()
    except:
        return url.strip()

PLATFORM_PATTERNS = {
    'tiktok': re.compile(r'(?:^|\.)tiktok\.com', re.IGNORECASE),
    'instagram': re.compile(r'(?:^|\.)instagram\.com|instagr\.am', re.IGNORECASE),
}

def detect_platform(url):
    """Deteksi platform dari URL dengan regex yang lebih akurat"""
    for platform, pattern in PLATFORM_PATTERNS.items():
        if pattern.search(url):
            return platform
    return None

def get_best_video_url(video_data, platform='tiktok'):
    """Memilih URL video dengan kualitas terbaik berdasarkan prioritas"""
    if platform == 'tiktok':
        # Prioritas: nowatermark_hd > nowatermark > watermark
        if video_data.get('nowatermark_hd'):
            return video_data['nowatermark_hd']
        elif video_data.get('nowatermark'):
            return video_data['nowatermark']
        elif video_data.get('watermark'):
            return video_data['watermark']
    return None

async def download_tiktok(url, quality='best'):
    """Handler untuk download TikTok - updated to match parse-duration.ts"""
    try:
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.tikwm.com',
            'Referer': 'https://www.tikwm.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        params = {
            'url': url,
            'hd': '1' if quality == 'best' else '0'
        }
        
        response = requests.post('https://www.tikwm.com/api/', headers=headers, params=params, timeout=15)
        response.raise_for_status()
        
        json_data = response.json()
        res = json_data.get('data')
        
        if not res:
            return {'success': False, 'message': 'Gagal mengambil data dari TikTok'}
        
        # Format data sesuai parse-duration.ts
        data = []
        if not res.get('size') and not res.get('wm_size') and not res.get('hd_size'):
            # TikTok slideshow/images
            for img_url in res.get('images', []):
                data.append({'type': 'photo', 'url': img_url})
        else:
            # TikTok video
            if res.get('wmplay'):
                data.append({'type': 'watermark', 'url': res['wmplay']})
            if res.get('play'):
                data.append({'type': 'nowatermark', 'url': res['play']})
            if res.get('hdplay'):
                data.append({'type': 'nowatermark_hd', 'url': res['hdplay']})
        
        result = {
            'success': True,
            'platform': 'TikTok',
            'type': 'images' if res.get('images') else 'video',
            'data': data,
            'images': res.get('images', []),
            'video': {
                'watermark': res.get('wmplay', ''),
                'nowatermark': res.get('play', ''),
                'nowatermark_hd': res.get('hdplay', '')
            },
            'author': {
                'id': res.get('author', {}).get('id', ''),
                'username': res.get('author', {}).get('unique_id', ''),
                'nickname': res.get('author', {}).get('nickname', ''),
                'avatar': res.get('author', {}).get('avatar', ''),
            },
            'title': res.get('title', ''),
            'duration': res.get('duration', 0),
            'cover': res.get('cover', ''),
            'music_info': {
                'id': res.get('music_info', {}).get('id', ''),
                'title': res.get('music_info', {}).get('title', ''),
                'author': res.get('music_info', {}).get('author', ''),
                'album': res.get('music_info', {}).get('album'),
                'url': res.get('music') or res.get('music_info', {}).get('play', ''),
            },
            'stats': {
                'views': res.get('play_count', 0),
                'likes': res.get('digg_count', 0),
                'comments': res.get('comment_count', 0),
                'shares': res.get('share_count', 0),
                'downloads': res.get('download_count', 0),
            }
        }
        
        return result
        
    except Exception as e:
        return {'success': False, 'message': f'Error TikTok: {str(e)}'}

async def download_instagram(url, quality='best'):
    """Handler untuk download Instagram - updated to return better data"""
    try:
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://yt1s.io',
            'Referer': 'https://yt1s.io/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        data = {
            'q': url,
            'w': '',
            'p': 'home',
            'lang': 'en'
        }
        
        response = requests.post('https://yt1s.io/api/ajaxSearch', headers=headers, data=data, timeout=15)
        response.raise_for_status()
        
        json_data = response.json()
        html = json_data.get('data', '')
        
        if not html:
            return {'success': False, 'message': 'Tidak ada data dari Instagram'}
        
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True, title=True)
        
        videos = []
        images = []
        thumb = ''
        
        for link in links:
            href = link['href']
            title = link['title'].lower()
            
            # Skip invalid URLs
            if not href.startswith('http') or href == '/en/home':
                continue
            
            if 'thumbnail' in title:
                thumb = href
            elif 'video' in title or 'mp4' in title:
                videos.append({'type': 'video', 'url': href})
            elif 'foto' in title or 'image' in title or 'photo' in title or 'jpg' in title:
                images.append({'type': 'photo', 'url': href})
        
        # Determine media type
        has_videos = len(videos) > 0
        has_images = len(images) > 0
        
        if has_videos and has_images:
            media_type = 'mixed'
        elif has_videos:
            media_type = 'video'
        elif has_images:
            media_type = 'images'
        else:
            media_type = 'unknown'
        
        result = {
            'success': True,
            'platform': 'Instagram',
            'type': media_type,
            'data': videos + images,  # Combined list
            'videos': videos,
            'images': images,
            'thumb': thumb
        }
        
        return result
        
    except Exception as e:
        return {'success': False, 'message': f'Error Instagram: {str(e)}'}

async def handle_downloader(event, client):
    """Handler utama untuk command /d dan /download"""
    if not event.is_private:
        return
    
    me = await client.get_me()
    if event.sender_id != me.id:
        return
    
    input_text = event.pattern_match.group(2).strip() if event.pattern_match.group(2) else ''
    
    if not input_text:
        if event.is_reply:
            reply = await event.get_reply_message()
            if reply and reply.message:
                input_text = reply.message.strip()
            else:
                await event.reply("❌ Pesan balasan tidak berisi link.")
                return
        else:
            await event.reply(
                "❌ **Cara pakai:**\n"
                "`/d <link>` atau `/download <link>`\n"
                "atau reply pesan yang berisi link\n\n"
                "**Platform support:**\n"
                "• TikTok (video, images, audio)\n"
                "• Instagram (video, images, mixed)"
            )
            return
    
    if not is_valid_url(input_text):
        await event.reply("❌ Input bukan link yang valid!")
        return
    
    clean_url = sanitize_url(input_text)
    platform = detect_platform(clean_url)
    
    if not platform:
        await event.reply("❌ Platform tidak didukung. Gunakan link dari TikTok atau Instagram.")
        return
    
    loading = await event.reply(f"⏳ Mengunduh dari **{platform.title()}**...")
    
    try:
        if platform == 'tiktok':
            result = await download_tiktok(clean_url)
        elif platform == 'instagram':
            result = await download_instagram(clean_url)
        else:
            await loading.edit("❌ Platform belum didukung")
            return
        
        try:
            await loading.delete()
        except:
            pass
        
        if not result.get('success'):
            await event.reply(f"❌ {result.get('message', 'Gagal mengunduh')}")
            return
        
        # ===== TIKTOK HANDLER =====
        if platform == 'tiktok':
            if result['type'] == 'video':
                # Get best quality video
                video_url = get_best_video_url(result['video'], 'tiktok')
                
                if not video_url:
                    await event.reply("❌ Tidak ada URL video yang valid")
                    return
                
                caption = (
                    f"📹 **TikTok Video**\n\n"
                    f"👤 **Author:** @{result['author']['username']}\n"
                    f"📝 **Title:** {result['title']}\n"
                    f"⏱ **Duration:** {result['duration']}s\n"
                    f"👁 **Views:** {result['stats']['views']:,}\n"
                    f"❤️ **Likes:** {result['stats']['likes']:,}\n"
                    f"💬 **Comments:** {result['stats']['comments']:,}"
                )
                
                # Download and send video
                try:
                    video_res = requests.get(video_url, timeout=60, stream=True)
                    if video_res.status_code == 200:
                        video_filename = f"tiktok_{int(datetime.now().timestamp())}.mp4"
                        with open(video_filename, 'wb') as f:
                            for chunk in video_res.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        await client.send_file(event.chat_id, video_filename, caption=caption)
                        os.remove(video_filename)
                    else:
                        await event.reply(f"{caption}\n\n🔗 [Download Video]({video_url})")
                except Exception as e:
                    await event.reply(f"{caption}\n\n🔗 [Download Video]({video_url})\n\n⚠️ Error: {str(e)}")
                
                # Download and send audio/music if available
                music_url = result.get('music_info', {}).get('url')
                if music_url:
                    try:
                        music_caption = (
                            f"🎵 **TikTok Audio**\n\n"
                            f"🎼 **Title:** {result['music_info']['title']}\n"
                            f"👤 **Artist:** {result['music_info']['author']}"
                        )
                        
                        audio_res = requests.get(music_url, timeout=30, stream=True)
                        if audio_res.status_code == 200:
                            audio_filename = f"tiktok_audio_{int(datetime.now().timestamp())}.mp3"
                            with open(audio_filename, 'wb') as f:
                                for chunk in audio_res.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            
                            await client.send_file(
                                event.chat_id, 
                                audio_filename, 
                                caption=music_caption,
                                voice_note=False,
                                attributes=[types.DocumentAttributeAudio(
                                    duration=result['duration'],
                                    title=result['music_info']['title'],
                                    performer=result['music_info']['author']
                                )]
                            )
                            os.remove(audio_filename)
                    except Exception as e:
                        pass  # Silent fail for audio
                        
            elif result['type'] == 'images':
                total_images = len(result['images'])
                caption = (
                    f"🖼 **TikTok Slideshow** ({total_images} foto)\n\n"
                    f"👤 **Author:** @{result['author']['username']}\n"
                    f"📝 **Title:** {result['title'][:100]}{'...' if len(result['title']) > 100 else ''}\n"
                    f"👁 **Views:** {result['stats']['views']:,}\n"
                    f"❤️ **Likes:** {result['stats']['likes']:,}\n"
                    f"💬 **Comments:** {result['stats']['comments']:,}"
                )
                
                # Download semua gambar
                all_files = []
                for idx, img_url in enumerate(result['images'], 1):
                    try:
                        img_res = requests.get(img_url, timeout=20)
                        if img_res.status_code == 200:
                            filename = f"tiktok_img_{int(datetime.now().timestamp())}_{idx}.jpg"
                            with open(filename, 'wb') as f:
                                f.write(img_res.content)
                            all_files.append(filename)
                    except:
                        pass
                
                if all_files:
                    # Split files menjadi chunks of 10
                    for i in range(0, len(all_files), 10):
                        chunk = all_files[i:i+10]
                        is_last_chunk = (i + 10 >= len(all_files))
                        
                        # Caption hanya di chunk terakhir
                        chunk_caption = caption if is_last_chunk else None
                        
                        await client.send_file(event.chat_id, chunk, caption=chunk_caption)
                    
                    # Hapus semua file
                    for f in all_files:
                        try:
                            os.remove(f)
                        except:
                            pass
                else:
                    await event.reply(f"{caption}\n\n⚠️ Gagal mengunduh gambar")
                
                # Send audio for slideshow too
                music_url = result.get('music_info', {}).get('url')
                if music_url:
                    try:
                        music_caption = (
                            f"🎵 **TikTok Audio**\n\n"
                            f"🎼 **Title:** {result['music_info']['title']}\n"
                            f"👤 **Artist:** {result['music_info']['author']}"
                        )
                        
                        audio_res = requests.get(music_url, timeout=30, stream=True)
                        if audio_res.status_code == 200:
                            audio_filename = f"tiktok_audio_{int(datetime.now().timestamp())}.mp3"
                            with open(audio_filename, 'wb') as f:
                                for chunk in audio_res.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            
                            await client.send_file(
                                event.chat_id, 
                                audio_filename, 
                                caption=music_caption,
                                voice_note=False,
                                attributes=[types.DocumentAttributeAudio(
                                    duration=result.get('duration', 0),
                                    title=result['music_info']['title'],
                                    performer=result['music_info']['author']
                                )]
                            )
                            os.remove(audio_filename)
                    except Exception as e:
                        pass  # Silent fail for audio
        
        # ===== INSTAGRAM HANDLER =====
        elif platform == 'instagram':
            if result['type'] == 'video':
                video_items = result['videos']
                total_videos = len(video_items)
                
                if total_videos == 1:
                    # Single video - send directly
                    video_url = video_items[0]['url']
                    caption = f"📹 **Instagram Video**"
                    
                    try:
                        video_res = requests.get(video_url, timeout=60, stream=True)
                        if video_res.status_code == 200:
                            video_filename = f"instagram_{int(datetime.now().timestamp())}.mp4"
                            with open(video_filename, 'wb') as f:
                                for chunk in video_res.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            
                            await client.send_file(event.chat_id, video_filename, caption=caption)
                            os.remove(video_filename)
                        else:
                            await event.reply(f"{caption}\n\n🔗 [Download]({video_url})")
                    except Exception as e:
                        await event.reply(f"{caption}\n\n🔗 [Download]({video_url})")
                else:
                    # Multiple videos - download semua
                    all_files = []
                    for idx, video_item in enumerate(video_items, 1):
                        try:
                            video_url = video_item['url']
                            video_res = requests.get(video_url, timeout=60, stream=True)
                            if video_res.status_code == 200:
                                filename = f"instagram_video_{int(datetime.now().timestamp())}_{idx}.mp4"
                                with open(filename, 'wb') as f:
                                    for chunk in video_res.iter_content(chunk_size=8192):
                                        f.write(chunk)
                                all_files.append(filename)
                        except:
                            pass
                    
                    if all_files:
                        # Split files menjadi chunks of 10
                        for i in range(0, len(all_files), 10):
                            chunk = all_files[i:i+10]
                            is_last_chunk = (i + 10 >= len(all_files))
                            
                            # Caption hanya di chunk terakhir
                            chunk_caption = f"📹 **Instagram Videos** ({len(all_files)} videos)" if is_last_chunk else None
                            
                            await client.send_file(event.chat_id, chunk, caption=chunk_caption)
                        
                        # Hapus semua file
                        for f in all_files:
                            try:
                                os.remove(f)
                            except:
                                pass
                    else:
                        # Fallback to links
                        for idx, video_item in enumerate(video_items[:5], 1):
                            await event.reply(f"📹 **Instagram Video {idx}**\n\n🔗 [Download]({video_item['url']})")
                            
            elif result['type'] == 'images':
                image_items = result['images']
                total_images = len(image_items)
                
                if total_images == 1:
                    # Single image
                    img_url = image_items[0]['url']
                    caption = f"🖼 **Instagram Image**"
                    
                    try:
                        img_res = requests.get(img_url, timeout=20)
                        if img_res.status_code == 200:
                            filename = f"instagram_{int(datetime.now().timestamp())}.jpg"
                            with open(filename, 'wb') as f:
                                f.write(img_res.content)
                            
                            await client.send_file(event.chat_id, filename, caption=caption)
                            os.remove(filename)
                        else:
                            await event.reply(f"{caption}\n\n🔗 [Download]({img_url})")
                    except:
                        await event.reply(f"{caption}\n\n🔗 [Download]({img_url})")
                else:
                    # Multiple images - download semua
                    all_files = []
                    for idx, img_item in enumerate(image_items, 1):
                        try:
                            img_url = img_item['url']
                            img_res = requests.get(img_url, timeout=20)
                            if img_res.status_code == 200:
                                filename = f"instagram_img_{int(datetime.now().timestamp())}_{idx}.jpg"
                                with open(filename, 'wb') as f:
                                    f.write(img_res.content)
                                all_files.append(filename)
                        except:
                            pass
                    
                    if all_files:
                        # Split files menjadi chunks of 10
                        for i in range(0, len(all_files), 10):
                            chunk = all_files[i:i+10]
                            is_last_chunk = (i + 10 >= len(all_files))
                            
                            # Caption hanya di chunk terakhir
                            chunk_caption = f"🖼 **Instagram Images** ({len(all_files)} photos)" if is_last_chunk else None
                            
                            await client.send_file(event.chat_id, chunk, caption=chunk_caption)
                        
                        # Hapus semua file
                        for f in all_files:
                            try:
                                os.remove(f)
                            except:
                                pass
                    else:
                        # Fallback to links
                        for idx, img_item in enumerate(image_items[:10], 1):
                            await event.reply(f"🖼 **Instagram Image {idx}**\n\n🔗 [Download]({img_item['url']})")
                            
            elif result['type'] == 'mixed':
                all_media = result['data']
                total_media = len(all_media)
                
                # Download semua media
                all_files = []
                for idx, media_item in enumerate(all_media, 1):
                    try:
                        media_url = media_item['url']
                        media_type = media_item['type']
                        
                        media_res = requests.get(media_url, timeout=60, stream=True)
                        if media_res.status_code == 200:
                            ext = 'mp4' if media_type == 'video' else 'jpg'
                            filename = f"instagram_mixed_{int(datetime.now().timestamp())}_{idx}.{ext}"
                            
                            with open(filename, 'wb') as f:
                                if media_type == 'video':
                                    for chunk in media_res.iter_content(chunk_size=8192):
                                        f.write(chunk)
                                else:
                                    f.write(media_res.content)
                            
                            all_files.append(filename)
                    except:
                        pass
                
                if all_files:
                    # Hitung total video dan foto
                    video_count = len([m for m in all_media[:len(all_files)] if m['type'] == 'video'])
                    photo_count = len(all_files) - video_count
                    caption = f"📸 **Instagram Media** ({photo_count} photos, {video_count} videos)"
                    
                    # Split files menjadi chunks of 10
                    for i in range(0, len(all_files), 10):
                        chunk = all_files[i:i+10]
                        is_last_chunk = (i + 10 >= len(all_files))
                        
                        # Caption hanya di chunk terakhir
                        chunk_caption = caption if is_last_chunk else None
                        
                        await client.send_file(event.chat_id, chunk, caption=chunk_caption)
                    
                    # Hapus semua file
                    for f in all_files:
                        try:
                            os.remove(f)
                        except:
                            pass
                else:
                    # Fallback to links
                    for idx, media_item in enumerate(all_media[:5], 1):
                        media_type_emoji = "📹" if media_item['type'] == 'video' else "🖼"
                        media_type_text = "Video" if media_item['type'] == 'video' else "Image"
                        await event.reply(f"{media_type_emoji} **Instagram {media_type_text} {idx}**\n\n🔗 [Download]({media_item['url']})")
            else:
                await event.reply("❌ Tidak ada media yang ditemukan")
        
    except Exception as e:
        try:
            await loading.delete()
        except:
            pass
        await event.reply(f"❌ Terjadi error: {str(e)}")





import os, mimetypes
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.account import UpdateProfileRequest, GetPrivacyRequest, SetPrivacyRequest
from telethon.tl.types import (
    InputPrivacyKeyProfilePhoto, InputPrivacyKeyAbout,
    InputPrivacyValueAllowAll, InputPrivacyValueAllowContacts,
    InputPrivacyValueDisallowAll, InputPrivacyValueAllowUsers,
    InputPrivacyValueDisallowUsers,
    InputPhoto
)

# ===== Util: deteksi & normalisasi =====
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp'}
VIDEO_EXTS = {'.mp4', '.webm', '.mkv', '.mov'}

def _ensure_valid_extension(path):
    base, ext = os.path.splitext(path)
    if ext.lower() in IMAGE_EXTS | VIDEO_EXTS:
        return path
    guess = mimetypes.guess_type(path)[0]
    if guess:
        if 'image' in guess:
            new_path = base + '.jpg'; os.rename(path, new_path); return new_path
        if 'video' in guess:
            new_path = base + '.mp4'; os.rename(path, new_path); return new_path
    new_path = base + '.jpg'; os.rename(path, new_path); return new_path

def _is_image(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in IMAGE_EXTS: return True
    guess = mimetypes.guess_type(path)[0]
    return bool(guess and 'image' in guess)

def _is_video(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in VIDEO_EXTS: return True
    guess = mimetypes.guess_type(path)[0]
    return bool(guess and 'video' in guess)

async def _upload_profile_media(client, path):
    valid_path = _ensure_valid_extension(path)
    fname = os.path.basename(valid_path)
    uploaded = await client.upload_file(valid_path, file_name=fname)
    if _is_video(valid_path):
        return await client(UploadProfilePhotoRequest(video=uploaded, video_start_ts=0.0))
    elif _is_image(valid_path):
        return await client(UploadProfilePhotoRequest(file=uploaded))
    else:
        return await client(UploadProfilePhotoRequest(file=uploaded))

# ===== Helpers: serialize & rebuild privacy rules =====
def _serialize_privacy_rules(rules):
    out = []
    for r in rules or []:
        name = r.__class__.__name__
        item = {"type": name}
        if name in ("PrivacyValueAllowUsers","InputPrivacyValueAllowUsers",
                    "PrivacyValueDisallowUsers","InputPrivacyValueDisallowUsers"):
            user_ids = []
            for u in getattr(r, "users", []) or []:
                uid = getattr(u, "user_id", getattr(u, "id", None))
                if uid is not None: user_ids.append(uid)
            item["user_ids"] = user_ids
        out.append(item)
    return out

async def _build_privacy_rules(client, serialized):
    rules = []
    for item in serialized or []:
        t = item["type"]
        if t in ("PrivacyValueAllowAll","InputPrivacyValueAllowAll"):
            rules.append(InputPrivacyValueAllowAll())
        elif t in ("PrivacyValueAllowContacts","InputPrivacyValueAllowContacts"):
            rules.append(InputPrivacyValueAllowContacts())
        elif t in ("PrivacyValueDisallowAll","InputPrivacyValueDisallowAll"):
            rules.append(InputPrivacyValueDisallowAll())
        elif t in ("PrivacyValueAllowUsers","InputPrivacyValueAllowUsers"):
            users = [await client.get_input_entity(uid) for uid in item.get("user_ids",[])]
            rules.append(InputPrivacyValueAllowUsers(users=users))
        elif t in ("PrivacyValueDisallowUsers","InputPrivacyValueDisallowUsers"):
            users = [await client.get_input_entity(uid) for uid in item.get("user_ids",[])]
            rules.append(InputPrivacyValueDisallowUsers(users=users))
    return rules

# ===== State per akun =====
account_states = {}  # key = user_id

def _blank_state():
    return {
        "first_name": None,
        "last_name": None,
        "bio": None,
        "photos": [],
        "privacy_photo": None,
        "privacy_bio": None,
        "is_cloned": False
    }

# === FITUR: CLONE ===
async def clone_handler(event, client):
    if not event.is_private:
        return
    me = await client.get_me()
    if event.sender_id != me.id:
        return

    state = account_states.get(me.id) or _blank_state()
    account_states[me.id] = state

    if state["is_cloned"]:
        await event.reply("❌ Tidak bisa clone lagi sebelum di-revert."); return
    if not event.is_reply:
        await event.reply("❌ Harus reply pesan user yang mau di-clone."); return

    try:
        reply = await event.get_reply_message()
        target_id = reply.sender_id
        input_target = await client.get_input_entity(target_id)

        # Simpan profil asli
        full_me = await client(GetFullUserRequest(me.id))
        state["first_name"] = me.first_name
        state["last_name"] = me.last_name
        state["bio"] = full_me.full_user.about
        state["photos"] = []
        state["privacy_photo"] = _serialize_privacy_rules(
            (await client(GetPrivacyRequest(InputPrivacyKeyProfilePhoto()))).rules
        )
        state["privacy_bio"] = _serialize_privacy_rules(
            (await client(GetPrivacyRequest(InputPrivacyKeyAbout()))).rules
        )

        # Simpan foto lama
        old_photos = await client.get_profile_photos('me', limit=10)
        for p in old_photos:
            f = await client.download_media(p)
            if f: state["photos"].append(f)

        # Update nama & bio jadi target
        full_target = await client(GetFullUserRequest(target_id))
        target_user = full_target.users[0] if hasattr(full_target, "users") else full_target.user
        await client(UpdateProfileRequest(
            first_name=target_user.first_name,
            last_name=target_user.last_name,
            about=full_target.full_user.about
        ))

        # Hapus foto lama
        if old_photos:
            await client(DeletePhotosRequest([
                InputPhoto(id=p.id, access_hash=p.access_hash, file_reference=p.file_reference)
                for p in old_photos
            ]))

        # Clone foto target
        target_photos = await client.get_profile_photos(target_id, limit=10)
        for tp in reversed(target_photos):
            f = await client.download_media(tp)
            if f:
                uploaded = await client.upload_file(f)
                await client(UploadProfilePhotoRequest(file=uploaded))
                os.remove(f)

        # Atur privasi: blokir semua, kecuali target
        await client(SetPrivacyRequest(
            key=InputPrivacyKeyProfilePhoto(),
            rules=[InputPrivacyValueDisallowAll(), InputPrivacyValueAllowUsers(users=[input_target])]
        ))
        await client(SetPrivacyRequest(
            key=InputPrivacyKeyAbout(),
            rules=[InputPrivacyValueDisallowAll(), InputPrivacyValueAllowUsers(users=[input_target])]
        ))

        state["is_cloned"] = True
        await event.reply("✅ Clone berhasil. Sekarang hanya bisa revert sebelum clone lagi.")

    except Exception as e:
        await event.reply(f"⚠ Error clone: `{e}`")

# === FITUR: REVERT ===
async def revert_handler(event, client):
    if not event.is_private:
        return
    me = await client.get_me()
    if event.sender_id != me.id:
        return

    state = account_states.get(me.id)
    if not state or not state["is_cloned"]:
        await event.reply("❌ Tidak ada clone aktif. Gunakan clone dulu."); return

    try:
        # Kembalikan nama & bio
        await client(UpdateProfileRequest(
            first_name=state["first_name"],
            last_name=state["last_name"],
            about=state["bio"] or ""
        ))

        # Hapus foto hasil clone
        current_photos = await client.get_profile_photos('me', limit=10)
        if current_photos:
            await client(DeletePhotosRequest([
                InputPhoto(id=p.id, access_hash=p.access_hash, file_reference=p.file_reference)
                for p in current_photos
            ]))

        # Upload kembali foto lama
        for f in state["photos"]:
            uploaded = await client.upload_file(f)
            await client(UploadProfilePhotoRequest(file=uploaded))
            os.remove(f)

        # Revert privasi ke aturan awal
        if state["privacy_photo"]:
            restored_photo_rules = await _build_privacy_rules(client, state["privacy_photo"])
            await client(SetPrivacyRequest(key=InputPrivacyKeyProfilePhoto(), rules=restored_photo_rules))
        if state["privacy_bio"]:
            restored_bio_rules = await _build_privacy_rules(client, state["privacy_bio"])
            await client(SetPrivacyRequest(key=InputPrivacyKeyAbout(), rules=restored_bio_rules))

        # Reset state akun ini
        account_states[me.id] = _blank_state()

        # Kirim pesan sukses
        await event.reply("✅ Revert berhasil. Profil, media, dan privasi kembali seperti awal. Clone bisa digunakan lagi.")
    except Exception as e:
        await event.reply(f"⚠ Error revert: `{e}`")



# ========== BAGIAN 3 ==========
# WEB SERVER, RESTART LOOP, MAIN + HANDLER

# === RAILWAY WEB SERVER ===
app = Flask('')

@app.route('/')
def home():
    return "Ubot aktif di Railway!", 200

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()


# === AUTO RESTART LOOP ===
async def run_clients_forever():
    while True:
        tasks = []
        for client, _, _ in clients:
            tasks.append(asyncio.create_task(client.run_until_disconnected()))
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        print("⚠ Client disconnect, restart 5 detik...")
        await asyncio.sleep(5)


# === MAIN ===
async def main():
    keep_alive()

    for index, acc in enumerate(ACCOUNTS, start=1):
        client = TelegramClient(StringSession(acc["session"]), API_ID, API_HASH)
        await client.start()
        akun_nama = f"Akun {index}"

        # === ANTI VIEW-ONCE ===
        if "anti_view_once" in acc["features"]:
            @client.on(events.NewMessage(incoming=True))
            async def handler(event, c=client, lc=acc["log_channel"], la=acc["log_admin"]):
                await anti_view_once_and_ttl(event, c, lc, la)

        # === PING ===
        if "ping" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/ping$"))
            async def ping(event, c=client):
                await ping_handler(event, c)

        # === HEARTBEAT ===
        if "heartbeat" in acc["features"]:
            asyncio.create_task(heartbeat(client, acc["log_admin"], acc["log_channel"], akun_nama))

        # === SAVE MEDIA / COLONG MEDIA ===
        if "save_media" in acc["features"]:
            @client.on(events.NewMessage(pattern=r'^/(save|s)(?:\s+|$)(.*)'))
            async def save_handler(event, c=client):
                await handle_save_command(event, c)
        
        # === DOWNLOADER ===
        if "downloader" in acc["features"]:
            @client.on(events.NewMessage(pattern=r'^/(d|download)(?:\s+|$)(.*)'))
            async def downloader_handler(event, c=client):
                await handle_downloader(event, c)
        
        # === CLEAR CHANNEL (KHUSUS CHANNEL) ===
        if "clearch" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/clearch$"))
            async def clearch(event, c=client):
                await clearch_handler(event, c)

        # === WHOIS (KHUSUS PRIVATE) ===
        if "whois" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/whois$"))
            async def whois(event, c=client):
                await whois_handler(event, c)

        # === CLONE ===
        if "clone" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/clone$"))
            async def clone_cmd(event, c=client):
                await clone_handler(event, c)

        # === REVERT ===
        if "revert" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/revert$"))
            async def revert_cmd(event, c=client):
                await revert_handler(event, c)

        # === SPAM FORWARD ===
        if "spam_forward" in acc["features"]:
          client.add_event_handler(
            lambda e: auto_forward_spam(e, client, acc.get("spam_triggers", [])),
            events.NewMessage()
            )
            
        # === AUTO-PIN (KHUSUS PRIVATE) ===
        if "autopin" in acc["features"]:
          client.add_event_handler(
            lambda e: autopin_handler(e, client, acc.get("autopin_keywords", [])),
            events.NewMessage()
          )

        # === HILIH ===
        if "hilih" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/h([aiueo])l\1h(?: (.+))?"))
            async def hilih_event(event, c=client):
                await hilih_handler(event, c)
                
        # === TIC TAC TOE (buat/join room) ===
        if "tictactoe" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:tictactoe|ttt)$"))
            async def tictactoe_event(event, c=client):
                await tictactoe_handler(event, c)
                
        # === TIC TAC TOE (langkah angka 1–9) ===
        if "tictactoe" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^[1-9]$"))
            async def tictactoe_move_event(event, c=client):
                await tictactoe_move_handler(event, c)
                
        # === VN TO TEXT (Reply Only) ===
        if "vn_to_text" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/stt$"))
            async def stt(event, c=client):
                await vn_to_text_handler(event, c)

        # === TEKA TEKI (buat/join room) ===
        if "tekateki" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:tekateki|ttk)$"))
            async def tekateki_event(event, c=client):
                await tekateki_handler(event, c)

        # === TEKA TEKI (jawaban user) ===
        if "tekateki" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?!/).*"))
            async def tekateki_answer_event(event, c=client):
                await tekateki_answer_handler(event, c)

        # === ASAH OTAK (buat/join room) ===
        if "asahotak" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:asahotak|ao)$"))
            async def asahotak_event(event, c=client):
                await asahotak_handler(event, c)

        # === ASAH OTAK (jawaban user) ===
        if "asahotak" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?!/).*"))
            async def asahotak_answer_event(event, c=client):
                await asahotak_answer_handler(event, c)

        # === SIAPAKAH AKU (buat/join room) ===
        if "siapakahaku" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:siapakahaku|saku)$"))
            async def siapakahaku_event(event, c=client):
                await siapakahaku_handler(event, c)

        # === SIAPAKAH AKU (jawaban user) ===
        if "siapakahaku" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?!/).*"))
            async def siapakahaku_answer_event(event, c=client):
                await siapakahaku_answer_handler(event, c)

        # === TEBAK KATA (buat/join room) ===
        if "tebakkata" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:tebakkata|tk)$"))
            async def tebakkata_event(event, c=client):
                await tebakkata_handler(event, c)

        # === TEBAK KATA (jawaban user) ===
        if "tebakkata" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?!/).*"))
            async def tebakkata_answer_event(event, c=client):
                await tebakkata_answer_handler(event, c)

        # === KUIS (buat/join room) ===
        if "kuis" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:kuis|quiz)$"))
            async def kuis_event(event, c=client):
                await kuis_handler(event, c)

        # === KUIS (jawaban user: a/b/c huruf kecil maupun besar) ===
        if "kuis" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?:[aA]|[bB]|[cC])$"))
            async def kuis_answer_event(event, c=client):
                await kuis_answer_handler(event, c)

        # === TEBAK LAGU (buat/join room) ===
        if "tebaklagu" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:tebaklagu|tl)$"))
            async def tebaklagu_event(event, c=client):
                await tebaklagu_handler(event, c)

        # === TEBAK LAGU (jawaban user) ===
        if "tebaklagu" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?!/).*"))
            async def tebaklagu_answer_event(event, c=client):
                await tebaklagu_answer_handler(event, c)

        # === TEBAK GAMBAR (buat/join room) ===
        if "tebakgambar" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:tebakgambar|tg)$"))
            async def tebakgambar_event(event, c=client):
                await tebakgambar_handler(event, c)

        # === TEBAK GAMBAR (jawaban user) ===
        if "tebakgambar" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?!/).*"))
            async def tebakgambar_answer_event(event, c=client):
                await tebakgambar_answer_handler(event, c)

        # === LENGKAPI KALIMAT (buat/join room) ===
        if "lengkapikalimat" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:lengkapikalimat|lk)$"))
            async def lengkapikalimat_event(event, c=client):
                await lengkapikalimat_handler(event, c)

        # === LENGKAPI KALIMAT (jawaban user) ===
        if "lengkapikalimat" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?!/).*"))
            async def lengkapikalimat_answer_event(event, c=client):
                await lengkapikalimat_answer_handler(event, c)

        # === TEBAK LIRIK (buat/join room) ===
        if "tebaklirik" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:tebaklirik|tlk)$"))
            async def tebaklirik_event(event, c=client):
                await tebaklirik_handler(event, c)

        # === TEBAK LIRIK (jawaban user) ===
        if "tebaklirik" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?!/).*"))
            async def tebaklirik_answer_event(event, c=client):
                await tebaklirik_answer_handler(event, c)

        # === CAK LONTONG (buat/join room) ===
        if "caklontong" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:caklontong|cl)$"))
            async def caklontong_event(event, c=client):
                await caklontong_handler(event, c)

        # === CAK LONTONG (jawaban user) ===
        if "caklontong" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?!/).*"))
            async def caklontong_answer_event(event, c=client):
                await caklontong_answer_handler(event, c)

        # === TEBAK TEBAKAN (buat/join room) ===
        if "tebaktebakan" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:tebaktebakan|ttb)$"))
            async def tebaktebakan_event(event, c=client):
                await tebaktebakan_handler(event, c)

        # === TEBAK TEBAKAN (jawaban user) ===
        if "tebaktebakan" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?!/).*"))
            async def tebaktebakan_answer_event(event, c=client):
                await tebaktebakan_answer_handler(event, c)

        # === MATH QUIZ (buat/join room) ===
        if "math" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:math|mt)$"))
            async def math_event(event, c=client):
                await math_handler(event, c)

        # === MATH QUIZ (jawaban user: a/b/c huruf kecil maupun besar) ===
        if "math" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?:[aA]|[bB]|[cC])$"))
            async def math_answer_event(event, c=client):
                await math_answer_handler(event, c)

        # === SUSUN KATA (buat/join room) ===
        if "susunkata" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/(?:susunkata|sk)$"))
            async def susunkata_event(event, c=client):
                await susunkata_handler(event, c)

        # === SUSUN KATA (jawaban user) ===
        if "susunkata" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^(?!/).*"))
            async def susunkata_answer_event(event, c=client):
                await susunkata_answer_handler(event, c)


        
        # Random Semua
        if "random" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/random$"))
            async def random_all_event(event, c=client):
                await random_all_handler(event, c)















        








        client.add_event_handler(lambda e: game_handler(e, client), events.NewMessage(pattern=r"^/game$"))


        # === NYERAH (gabungan semua game) ===
        @client.on(events.NewMessage(pattern=r"^/nyerah$"))
        async def surrender_event(event, c=client):
            await surrender_room_handler(event, c)

        # === BATALKAN ROOM (gabungan semua game) ===
        @client.on(events.NewMessage(pattern=r"^/batal$"))
        async def cancel_event(event, c=client):
            await cancel_room_handler(event, c)

        if "confess" in acc["features"]:
            client.add_event_handler(lambda e: confess_handler(e, client), events.NewMessage())

        
                
            
        if "ai" in acc["features"]:
            @client.on(events.NewMessage(pattern=r'^/ai(?:\s+(.*))?$'))
            async def ai_command_handler(event, c=client):
                await ai_handler(event, c)

        if "ai" in acc["features"]:
            @client.on(events.NewMessage(pattern=r'^/ai2(?:\s+(.*))?$'))
            async def ai2_command_handler(event, c=client):
                await ai2_handler(event, c)

        if "ai" in acc["features"]:
            @client.on(events.NewMessage(pattern=r'^/ai3(?:\s+(.*))?$'))
            async def ai3_command_handler(event, c=client):
                await ai3_handler(event, c)

        if "ai" in acc["features"]:
            @client.on(events.NewMessage(pattern=r'^/ai4(?:\s+(.*))?$'))
            async def ai4_command_handler(event, c=client):
                await ai4_handler(event, c)

        if "ai" in acc["features"]:
            @client.on(events.NewMessage(pattern=r'^/ai5(?:\s+(.*))?$'))
            async def ai5_command_handler(event, c=client):
                await ai5_handler(event, c)


        

        if "cecan" in acc["features"]:
            @client.on(events.NewMessage(pattern=r"^/cecan(?:\s+\w+)?$"))
            async def cecan_event(event, c=client):
                await cecan_handler(event, c)

        





                             






          

        # === INFO RESTART ===
        fitur_list = acc.get("features", [])
        fitur_str = " | ".join(fitur_list) if fitur_list else "Tidak ada"
        text = (
            f"♻️ **Ubot Aktif**\n\n"
            f"👤 Akun: {akun_nama}\n"
            f"⚙️ Fitur: [{fitur_str}]\n"
            f"🕒 Waktu: {datetime.now(ZoneInfo('Asia/Jakarta')).strftime('%H:%M:%S || %d-%m-%Y')}\n"
            f"📡 Status: 🟢 Online"
        )
        if acc["log_admin"]:
            await client.send_message(acc["log_admin"], text)

        clients.append((client, acc.get("log_channel"), acc.get("log_admin")))

    print(f"✅ Ubot aktif dengan {len(clients)} akun.")
    await run_clients_forever()


asyncio.run(main())
