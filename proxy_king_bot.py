# PROXY KING BOT - UPGRADED VERSION
# Features: 1k-10k proxies, File upload, Stop/Refresh, Exact count
# By Just-Lisa

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

# ========= CONFIGURATION =========
BOT_TOKEN = os.environ.get('BOT_TOKEN', "7851076883:AAFTgTd9ycUiuBZFYDthRx1IBjqCHeHtZCc")
ADMIN_ID = int(os.environ.get('ADMIN_ID', 8332683304))

bot = telebot.TeleBot(BOT_TOKEN)

# Global variables for stop/refresh
checking_active = True
current_check = None

print("="*50)
print("🔥 PROXY KING BOT UPGRADED 🔥")
print("="*50)
print(f"🤖 Bot Token: {BOT_TOKEN[:15]}...")
print(f"👑 Admin ID: {ADMIN_ID}")
print(f"📱 Bot Username: @ProxyCheckerSpecial_bot")
print("✅ Features: 1k-10k | File Upload | Stop/Refresh")
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
        self.is_checking = False
        
    # PROXY SOURCES - JAHAN SE PROXY AATE HAIN
    def get_proxy_sources_info(self):
        return """
📡 **PROXY SOURCES:**

🌐 **HTTP/HTTPS Sources:**
• proxyscrape.com - Free HTTP proxy list
• TheSpeedX GitHub - Public proxy archive
• roosterkid GitHub - HTTPS proxies
• Self-generated fallback (random IPs)

🔒 **SOCKS5 Sources:**
• proxyscrape.com - SOCKS5 list
• TheSpeedX SOCKS-List - GitHub

🏠 **RESIDENTIAL (Simulated):**
• Random ISP IP ranges
• Realistic port patterns

📱 **MOBILE (Simulated):**
• 4G/5G carrier IP ranges
• Mobile network patterns
"""
    
    def get_residential_proxies(self, count=1000):
        """Generate EXACT count residential proxies"""
        proxies = []
        for _ in range(count):
            ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            port = random.choice([8080, 3128, 80, 443, 1080, 8888, 8000, 8081, 8443])
            proxies.append(f"http://{ip}:{port}")
        return proxies
    
    def get_mobile_proxies(self, count=1000):
        """Generate EXACT count mobile proxies"""
        proxies = []
        mobile_networks = ["100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111"]
        for _ in range(count):
            ip = f"{random.choice(mobile_networks)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            port = random.choice([8080, 3128, 80, 8081, 8888])
            proxies.append(f"http://{ip}:{port}")
        return proxies
    
    def get_socks5_proxies(self, count=1000):
        """Generate EXACT count SOCKS5 proxies"""
        proxies = []
        socks_sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"
        ]
        
        for source in socks_sources:
            try:
                response = requests.get(source, timeout=15)
                if response.status_code == 200:
                    found = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}', response.text)
                    for proxy in found:
                        if len(proxies) < count:
                            proxies.append(f"socks5://{proxy}")
            except:
                pass
        
        # Generate fallback if needed
        while len(proxies) < count:
            ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            port = random.choice([1080, 1081, 9050, 9150, 1085, 1086])
            proxies.append(f"socks5://{ip}:{port}")
        
        return proxies[:count]
    
    def get_http_proxies(self, count=1000):
        """Generate EXACT count HTTP proxies"""
        proxies = []
        http_sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://www.proxy-list.download/api/v1/get?type=http"
        ]
        
        for source in http_sources:
            try:
                response = requests.get(source, timeout=15)
                if response.status_code == 200:
                    found = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}', response.text)
                    for proxy in found:
                        if len(proxies) < count:
                            proxies.append(f"http://{proxy}")
            except:
                pass
        
        # Generate fallback if needed
        while len(proxies) < count:
            ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            port = random.choice([8080, 3128, 80, 443, 8000, 8888, 8081, 8443])
            proxies.append(f"http://{ip}:{port}")
        
        return proxies[:count]
    
    def check_single_proxy(self, proxy):
        """Check if proxy is alive"""
        global checking_active
        if not checking_active:
            return False
            
        test_url = "http://httpbin.org/ip"
        proxy_dict = {"http": proxy, "https": proxy}
        try:
            start = time.time()
            response = requests.get(test_url, proxies=proxy_dict, timeout=10)
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
    
    def check_proxies_batch(self, proxies, progress_callback, message_id=None, chat_id=None):
        """Check proxies with real-time updates and stop support"""
        global checking_active
        checking_active = True
        self.is_checking = True
        
        self.total = len(proxies)
        self.checked = 0
        self.bad = 0
        self.hits = 0
        self.errors = 0
        self.live_proxies = []
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(self.check_single_proxy, proxy): proxy for proxy in proxies}
            
            for future in as_completed(futures):
                if not checking_active:
                    self.is_checking = False
                    return self.live_proxies
                    
                self.checked += 1
                
                if progress_callback and (self.checked % 10 == 0 or self.checked == self.total):
                    progress = (self.checked / self.total) * 100
                    progress_callback(self.checked, self.total, self.hits, self.bad, self.errors, progress, message_id, chat_id)
        
        self.is_checking = False
        return self.live_proxies
    
    def check_custom_proxies(self, proxy_list, progress_callback, message_id=None, chat_id=None):
        """Check user-uploaded proxies"""
        return self.check_proxies_batch(proxy_list, progress_callback, message_id, chat_id)

proxy_king = ProxyKing()

# ========= BUTTON MENUS =========
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🏠 RESIDENTIAL", callback_data="residential")
    btn2 = InlineKeyboardButton("📱 MOBILE", callback_data="mobile")
    btn3 = InlineKeyboardButton("🔒 SOCKS5", callback_data="socks5")
    btn4 = InlineKeyboardButton("🌐 HTTP", callback_data="http")
    btn5 = InlineKeyboardButton("🎲 ALL TYPES", callback_data="all")
    btn6 = InlineKeyboardButton("📤 UPLOAD FILE", callback_data="upload_file")
    btn7 = InlineKeyboardButton("📡 PROXY SOURCES", callback_data="sources")
    btn8 = InlineKeyboardButton("📊 STATS", callback_data="stats")
    btn9 = InlineKeyboardButton("❓ HELP", callback_data="help")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    markup.add(btn6, btn7)
    markup.add(btn8, btn9)
    return markup

def count_menu(proxy_type):
    markup = InlineKeyboardMarkup(row_width=2)
    btn1k = InlineKeyboardButton("1000", callback_data=f"{proxy_type}_1000")
    btn2k = InlineKeyboardButton("2000", callback_data=f"{proxy_type}_2000")
    btn5k = InlineKeyboardButton("5000", callback_data=f"{proxy_type}_5000")
    btn10k = InlineKeyboardButton("10000", callback_data=f"{proxy_type}_10000")
    back = InlineKeyboardButton("◀️ BACK", callback_data="back")
    markup.add(btn1k, btn2k, btn5k, btn10k, back)
    return markup

def control_buttons(proxy_type, count, msg_id):
    """Stop/Refresh buttons for stuck processes"""
    markup = InlineKeyboardMarkup(row_width=2)
    stop_btn = InlineKeyboardButton("⛔ STOP", callback_data=f"stop_{proxy_type}_{count}_{msg_id}")
    refresh_btn = InlineKeyboardButton("🔄 REFRESH", callback_data=f"refresh_{proxy_type}_{count}_{msg_id}")
    back = InlineKeyboardButton("◀️ BACK TO MENU", callback_data="back")
    markup.add(stop_btn, refresh_btn, back)
    return markup

def progress_bar(percentage):
    filled = int(percentage / 5)
    bar = "█" * filled + "░" * (20 - filled)
    return f"[{bar}] {percentage:.1f}%"

def update_progress(checked, total, hits, bad, errors, progress, msg_id, chat_id):
    bar = progress_bar(progress)
    text = f"""
🔥 **LIVE CHECKING STATUS**
{bar}

📊 **STATS:**
├ 📦 TOTAL: `{total}`
├ ✅ CHECKED: `{checked}`
├ 🎯 HITS: `{hits}`
├ ❌ BAD: `{bad}`
├ ⚠️ ERRORS: `{errors}`
└ 📈 RATE: `{(hits/checked*100) if checked > 0 else 0:.1f}%`

⏱️ **PROGRESS:** `{progress:.1f}%`
⚡ **SPEED:** `{checked/5:.0f}` proxies/sec

_Use STOP button if stuck_
"""
    try:
        bot.edit_message_text(text, chat_id, msg_id, parse_mode='Markdown')
    except:
        pass

def fake_update_progress(checked, total, hits, bad, errors, progress, msg_id, chat_id):
    """For custom file checking"""
    update_progress(checked, total, hits, bad, errors, progress, msg_id, chat_id)

# ========= BOT COMMANDS =========
@bot.message_handler(commands=['start'])
def start(msg):
    if msg.chat.id != ADMIN_ID:
        bot.reply_to(msg, "❌ Access Denied. Only @Imottski")
        return
    bot.send_message(msg.chat.id, "🔥 **PROXY KING BOT UPGRADED** 🔥\n\n**New Features:**\n• 1000-10000 proxies\n• Upload custom proxy list\n• Stop/Refresh buttons\n• Exact count guaranteed\n\nSelect option:", parse_mode='Markdown', reply_markup=main_menu())

@bot.message_handler(content_types=['document'])
def handle_file(msg):
    if msg.chat.id != ADMIN_ID:
        return
    
    global checking_active
    checking_active = True
    
    file_info = bot.get_file(msg.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Parse proxies from file
    content = downloaded_file.decode('utf-8', errors='ignore')
    lines = content.split('\n')
    
    proxies = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            # Add protocol if missing
            if '://' not in line:
                line = f"http://{line}"
            proxies.append(line)
    
    if not proxies:
        bot.reply_to(msg, "❌ No valid proxies found in file!")
        return
    
    bot.reply_to(msg, f"📁 Found {len(proxies)} proxies in file!\n\n🔄 Starting check...")
    
    progress_msg = bot.send_message(msg.chat.id, "Checking proxies...")
    
    live = proxy_king.check_custom_proxies(proxies, fake_update_progress, progress_msg.message_id, msg.chat.id)
    
    filename = f"custom_proxies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(f"# Custom Proxy Check Results\n")
        f.write(f"# Total: {len(proxies)} | Live: {len(live)}\n\n")
        for p in live:
            f.write(p + "\n")
    
    bot.edit_message_text(f"✅ DONE! Found {len(live)} live proxies", msg.chat.id, progress_msg.message_id)
    
    if live:
        with open(filename, 'rb') as f:
            bot.send_document(msg.chat.id, f, caption=f"📎 {len(live)} live proxies from your file")
    else:
        bot.send_message(msg.chat.id, "❌ No live proxies found in your file.")
    
    os.remove(filename)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message.chat.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Access Denied")
        return
    
    global checking_active, current_check
    data = call.data
    
    if data == "back":
        bot.edit_message_text("Select option:", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
        return
    
    if data == "stats":
        rate = (len(proxy_king.live_proxies)/proxy_king.total*100) if proxy_king.total > 0 else 0
        text = f"📊 **STATS**\n\nTotal Checked: {proxy_king.total}\nLive Found: {len(proxy_king.live_proxies)}\nSuccess Rate: {rate:.1f}%"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=main_menu())
        return
    
    if data == "help":
        text = """❓ **HELP**

**Proxy Types:**
🏠 Residential - Best for Netflix/PSN
📱 Mobile - 4G/5G proxies
🔒 SOCKS5 - Fast general use
🌐 HTTP - Free tier

**Features:**
• Select 1000-10000 proxies
• Upload .txt file with proxies
• STOP button - halt checking
• REFRESH - restart

**Proxy Sources:**
Click "📡 PROXY SOURCES" button"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=main_menu())
        return
    
    if data == "sources":
        text = proxy_king.get_proxy_sources_info()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=main_menu())
        return
    
    if data == "upload_file":
        bot.edit_message_text("📤 **Upload a .txt file** with proxies\n\nFormat: IP:PORT (one per line)\nExample: 192.168.1.1:8080\n\n⚠️ File will be checked automatically!", call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=main_menu())
        return
    
    if data.startswith("stop_"):
        checking_active = False
        bot.edit_message_text("⛔ **Checking stopped by user**\n\nClick REFRESH to start new check or BACK to menu", call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=main_menu())
        bot.answer_callback_query(call.id, "Stopped!")
        return
    
    if data.startswith("refresh_"):
        checking_active = True
        parts = data.split("_")
        proxy_type = parts[1]
        count = int(parts[2])
        bot.edit_message_text(f"🔄 **Refreshing** - Starting new check for {count} {proxy_type} proxies...", call.message.chat.id, call.message.message_id)
        # Recursively start check again
        start_check(call.message.chat.id, call.message.message_id, proxy_type, count)
        return
    
    if data in ["residential", "mobile", "socks5", "http", "all"]:
        proxy_king.current_type = data.upper()
        bot.edit_message_text(f"✅ Selected: {data.upper()}\n\n📊 How many proxies?", call.message.chat.id, call.message.message_id, reply_markup=count_menu(data))
        return
    
    if "_" in data and any(x in data for x in ["1000", "2000", "5000", "10000"]):
        parts = data.split("_")
        proxy_type = parts[0]
        count = int(parts[1])
        start_check(call.message.chat.id, call.message.message_id, proxy_type, count)
        return

def start_check(chat_id, msg_id, proxy_type, count):
    global checking_active
    checking_active = True
    
    bot.edit_message_text(f"🔄 **Generating EXACTLY {count} {proxy_type} proxies...**\n⏳ Please wait (this may take a moment)", chat_id, msg_id)
    
    if proxy_type == "residential":
        proxies = proxy_king.get_residential_proxies(count)
    elif proxy_type == "mobile":
        proxies = proxy_king.get_mobile_proxies(count)
    elif proxy_type == "socks5":
        proxies = proxy_king.get_socks5_proxies(count)
    elif proxy_type == "http":
        proxies = proxy_king.get_http_proxies(count)
    else:
        proxies = (proxy_king.get_residential_proxies(count//4) + 
                  proxy_king.get_mobile_proxies(count//4) +
                  proxy_king.get_socks5_proxies(count//4) +
                  proxy_king.get_http_proxies(count//4))
    
    # Ensure exact count
    if len(proxies) > count:
        proxies = proxies[:count]
    elif len(proxies) < count:
        # Generate more
        while len(proxies) < count:
            proxies.append(f"http://{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}:{random.choice([8080,3128,80,443])}")
    
    bot.edit_message_text(f"🔍 **Checking {len(proxies)} {proxy_type} proxies...**\n⚡ 50 threads\n⏱️ Estimated: ~{len(proxies)//50}s\n\n_Use STOP button if stuck_", chat_id, msg_id, parse_mode='Markdown')
    
    # Add control buttons
    control_msg = bot.send_message(chat_id, "⏳ Starting check...", reply_markup=control_buttons(proxy_type, count, msg_id))
    
    live = proxy_king.check_proxies_batch(proxies, update_progress, control_msg.message_id, chat_id)
    
    filename = f"proxies_{proxy_type}_{count}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(f"# PROXY KING RESULTS\n")
        f.write(f"# Type: {proxy_type.upper()}\n")
        f.write(f"# Requested: {count}\n")
        f.write(f"# Checked: {proxy_king.total}\n")
        f.write(f"# Live Found: {len(live)}\n\n")
        for p in live:
            f.write(p + "\n")
    
    final_text = f"""
✅ **CHECK COMPLETED!**

📊 **FINAL STATISTICS:**
├ 📦 REQUESTED: `{count}`
├ 🎯 GENERATED: `{proxy_king.total}`
├ ✅ LIVE HITS: `{len(live)}`
├ ❌ DEAD: `{proxy_king.bad}`
└ ⚠️ ERRORS: `{proxy_king.errors}`

📈 **SUCCESS RATE:** `{(len(live)/proxy_king.total*100):.1f}%`
📁 **FILE READY:** `{filename}`
"""
    
    bot.edit_message_text(final_text, chat_id, control_msg.message_id, parse_mode='Markdown')
    
    if live:
        with open(filename, 'rb') as f:
            bot.send_document(chat_id, f, caption=f"📎 {len(live)} live proxies from {count} total")
    else:
        bot.send_message(chat_id, "❌ No live proxies found. Try different type or count.")
    
    os.remove(filename)

def keep_alive():
    while True:
        time.sleep(300)
        print("💓 Bot alive")

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    print("✅ Bot is running with UPGRADED features!")
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
