import os
import time
import random
import re
from threading import Thread
from flask import Flask
from instagrapi import Client

app = Flask(__name__)

@app.route('/')
def home():
    return "VANTA Instagram Bot is active and running for Ahmed! 💀🔥"

def run_bot():
    sessionid = "55171462864%3APW8b1TI7joFJlQ%3A15%3AAYlJUZgLRhlB0y8Ilvn9dhbMFNMFJ8BdMJqxXrgs8w"
    media_url = "https://www.instagram.com/reel/DfNRAqZRdst/?cplk=MWRpdDM1MmlmMGh5Mw=="
    target_count = 50000

    client = Client()
    print("[*] جاري تسجيل الدخول عبر جلسة المتصفح على سحاب ريندر...")
    try:
        client.login_by_sessionid(sessionid)
        print("[+] تم تسجيل الدخول بنجاح على سحاب ريندر.")
    except Exception as e:
        print(f"[-] فشل تسجيل الدخول: {e}")
        return

    try:
        if "instagram.com" in media_url:
            match = re.search(r'/(?:p|reel|reels)/([^/?#&]+)', media_url)
            if match:
                shortcode = match.group(1)
                media_id = client.media_pk_from_code(shortcode)
            else:
                media_id = client.media_pk_from_url(media_url)
        else:
            media_id = media_url
    except Exception as e:
        print(f"[-] خطأ في استخراج معرف المنشور: {e}")
        return

    print(f"[*] معرف المنشور المستهدف: {media_id}")
    print(f"[*] البدء بإرسال حتى {target_count} تعليق (بالسرعة المُسَرّعة)...")

    success_count = 0
    comments_pool = [
        "يالله توفيقك , سبحان الله وبحمده🫀",
        "يا رب توفيقك، سبحان الله وبحمده ✨",
        "سبحان الله وبحمده، يالله توفيقك 🤍",
        "توفيقك يارب، سبحان الله وبحمده لعلها تصيب 🙏",
        "سبحان الله وبحمده 🌺 يالله توفيقك"
    ]

    while success_count < target_count:
        comment_text = random.choice(comments_pool)
        try:
            client.media_comment(media_id, comment_text)
            success_count += 1
            print(f"[✓] تم إرسال التعليق رقم ({success_count}/{target_count}): {comment_text}")
            
            # تم تسريع الإيقاع يدوياً لتصبح الفترة بين 6 إلى 12 ثانية فقط
            time.sleep(random.uniform(6, 12))
            
        except Exception as e:
            print(f"[x] خطأ أثناء النشر: {e}")
            print("[*] تبريد مؤقت للحساب لمدة 5 دقائق تفادياً لأي تقييد...")
            time.sleep(300)

    print(f"[+] اكتملت العملية بنجاح يا سيدي أحمد! الإجمالي المرسل: {success_count}")

@app.before_request
def start_bot_once():
    global bot_started
    try:
        if not globals().get('bot_started', False):
            globals()['bot_started'] = True
            thread = Thread(target=run_bot)
            thread.daemon = True
            thread.start()
    except Exception:
        pass

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
