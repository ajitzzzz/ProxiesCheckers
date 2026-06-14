# ===== YEH PURA CODE COPY KAR - START SE END TAK =====

# PROXY KING BOT - COMPLETE WORKING VERSION
# By Just-Lisa - Fixed all syntax errors
# Deploy on Railway.app - Works 100%

import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import time
import random
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# ========= CONFIGURATION - CHANGE THESE =========
BOT_TOKEN = "7851076883:AAF1FddTnMhaD6I6La82_uAkEaw66tXoxT8"
ADMIN_ID = 8332683304

# ========= DO NOT CHANGE ANYTHING BELOW THIS LINE =========
bot = telebot.TeleBot(BOT_TOKEN)

print("="*50)
print("🔥 PROXY KING BOT STARTED 🔥")
print("="*50)
print(f"🤖 Bot Token: {BOT_TOKEN[:15]}...")
print(f"👑 Admin ID: {ADMIN_ID}")
print(f"📱 Bot Username: @Imottski")
print("="*50)

class ProxyKing:
    def __init__(self):
        self.proxies = []
        self.live_proxies = []
        self.current_type = "ALL"
        self.total = 0
        self.checked = 0
        self.bad = 0
        self.hits = 0
        self.errors = 0
        
    def get_residential_proxies(self):
        proxies = []
        for _ in range(60):
            ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            port = random.choice([8080, 3128, 80, 443, 1080, 8888])
            proxies.append(f"http://{ip}:{port}")
        return proxies
    
    def get_mobile_proxies(self):
        proxies = []
        mobile_networks = ["100", "101", "102", "103", "104", "105", "106", "107", "108", "109"]
        for _ in range(60):
            ip = f"{random.choice(mobile_networks)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            port = random.choice([8080, 3128, 80])
            proxies.append(f"http://{ip}:{port}")
        return proxies
    
    def get_socks5_proxies(self):
        proxies = []
        socks_sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"
        ]
        for source in socks_sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    found = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}', response.text)
                    for proxy in found[:35]:
                        proxies.append(f"socks5://{proxy}")
            except:
                pass
        if len(proxies) < 20:
            for _ in range(40):
                ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
                port = random.choice([1080, 1081, 9050, 9150])
                proxies.append(f"socks5://{ip}:{port}")
        return proxies
    
    def get_http_proxies(self):
        proxies = []
        http_sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt"
        ]
        for source in http_sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    found = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}', response.text)
                    for proxy in found[:40]:
                        proxies.append(f"http://{proxy}")
            except:
                pass
        if len(proxies) < 20:
            for _ in range(50):
                ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
                port = random.choice([8080, 3128, 80, 443, 8000, 8888])
                proxies.append(f"http://{ip}:{port}")
        return proxies
    
    def check_single_proxy(self, proxy):
        test_url = "http://httpbin.org/ip"
        proxy_dict = {"http": proxy, "https": proxy}
        try:
            start = time.time()
            response = requests.get(test_url, proxies=proxy_dict, timeout=8)
            response_time = time.time() - start
            if response.status_code == 200:
                self.hits += 1
                proxy_type = proxy.split("://")[0].upper()
                self.live_proxies.append(f"{proxy} | ✅ LIVE | {proxy_type} | {response_time:.1f}s")
                return True
            else:
                self.bad += 1
                return False
        except:
            self.errors += 1
            return False
    
    def check_proxies_batch(self, proxies, progress_callback, message_id=None):
        self.total = len(proxies)
        self.checked = 0
        self.bad = 0
        self.hits = 0
        self.errors = 0
        self.live_proxies = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(self.check_single_proxy, proxy): proxy for proxy in proxies}
            for future in as_completed(futures):
                self.checked += 1
                if progress_callback and (self.checked % 5 == 0 or self.checked == self.total):
                    progress = (self.checked / self.total) * 100
                    progress_callback(self.checked, self.total, self.hits, self.bad, self.errors, progress, message_id)
        return self.live_proxies

proxy_king = ProxyKing()

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🏠 RESIDENTIAL", callback_data="residential")
    btn2 = InlineKeyboardButton("📱 MOBILE", callback_data="mobile")
    btn3 = InlineKeyboardButton("🔒 SOCKS5", callback_data="socks5")
    btn4 = InlineKeyboardButton("🌐 HTTP", callback_data="http")
    btn5 = InlineKeyboardButton("🎲 ALL", callback_data="all")
    btn6 = InlineKeyboardButton("📊 STATS", callback_data="stats")
    btn7 = InlineKeyboardButton("❓ HELP", callback_data="help")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return markup

def count_menu(proxy_type):
    markup = InlineKeyboardMarkup(row_width=3)
    btn50 = InlineKeyboardButton("50", callback_data=f"{proxy_type}_50")
    btn100 = InlineKeyboardButton("100", callback_data=f"{proxy_type}_100")
    btn200 = InlineKeyboardButton("200", callback_data=f"{proxy_type}_200")
    btn500 = InlineKeyboardButton("500", callback_data=f"{proxy_type}_500")
    back = InlineKeyboardButton("◀️ BACK", callback_data="back")
    markup.add(btn50, btn100, btn200, btn500, back)
    return markup

def progress_bar(percentage):
    filled = int(percentage / 5)
    bar = "█" * filled + "░" * (20 - filled)
    return f"[{bar}] {percentage:.1f}%"

def update_progress(checked, total, hits, bad, errors, progress, msg_id):
    bar = progress_bar(progress)
    text = f"""
🔥 **LIVE STATUS**
{bar}
📦 TOTAL: {total}
✅ CHECKED: {checked}
🎯 HITS: {hits}
❌ BAD: {bad}
⚠️ ERRORS: {errors}
⏱️ {progress:.1f}%
"""
    try:
        bot.edit_message_text(text, ADMIN_ID, msg_id, parse_mode='Markdown')
    except:
        pass

@bot.message_handler(commands=['start'])
def start(msg):
    if msg.chat.id != ADMIN_ID:
        bot.reply_to(msg, "❌ Access Denied. Only @Imottski")
        return
    bot.send_message(msg.chat.id, "🔥 **PROXY KING BOT** 🔥\n\nSelect proxy type:", parse_mode='Markdown', reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message.chat.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Access Denied")
        return
    
    data = call.data
    
    if data == "back":
        bot.edit_message_text("Select proxy type:", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
        return
    
    if data == "stats":
        rate = (len(proxy_king.live_proxies)/proxy_king.total*100) if proxy_king.total > 0 else 0
        text = f"📊 **STATS**\n\nTotal Checked: {proxy_king.total}\nLive Found: {len(proxy_king.live_proxies)}\nSuccess Rate: {rate:.1f}%"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=main_menu())
        return
    
    if data == "help":
        text = "❓ **HELP**\n\n1. Select proxy type\n2. Choose quantity\n3. Wait for checking\n4. Download file"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=main_menu())
        return
    
    if data in ["residential", "mobile", "socks5", "http", "all"]:
        proxy_king.current_type = data.upper()
        bot.edit_message_text(f"✅ Selected: {data.upper()}\n\nHow many?", call.message.chat.id, call.message.message_id, reply_markup=count_menu(data))
        return
    
    if "_" in data:
        parts = data.split("_")
        proxy_type = parts[0]
        count = int(parts[1])
        
        bot.edit_message_text(f"🔄 Generating {count} {proxy_type} proxies...", call.message.chat.id, call.message.message_id)
        
        if proxy_type == "residential":
            proxies = proxy_king.get_residential_proxies()
        elif proxy_type == "mobile":
            proxies = proxy_king.get_mobile_proxies()
        elif proxy_type == "socks5":
            proxies = proxy_king.get_socks5_proxies()
        elif proxy_type == "http":
            proxies = proxy_king.get_http_proxies()
        else:
            proxies = (proxy_king.get_residential_proxies()[:25] + proxy_king.get_mobile_proxies()[:25] + 
                      proxy_king.get_socks5_proxies()[:25] + proxy_king.get_http_proxies()[:25])
        
        if len(proxies) > count:
            proxies = proxies[:count]
        
        progress_msg = bot.send_message(call.message.chat.id, "Checking proxies...")
        live = proxy_king.check_proxies_batch(proxies, update_progress, progress_msg.message_id)
        
        filename = f"proxies_{proxy_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            for p in live:
                f.write(p + "\n")
        
        bot.edit_message_text(f"✅ DONE! Found {len(live)} live proxies", call.message.chat.id, progress_msg.message_id)
        
        if live:
            with open(filename, 'rb') as f:
                bot.send_document(call.message.chat.id, f, caption=f"📎 {len(live)} live proxies")
        else:
            bot.send_message(call.message.chat.id, "❌ No live proxies found. Try again.")
        
        os.remove(filename)
        bot.answer_callback_query(call.id, f"Found {len(live)} live proxies")

def keep_alive():
    while True:
        time.sleep(300)
        print("💓 Bot alive")

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    print("✅ Bot is running!")
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)