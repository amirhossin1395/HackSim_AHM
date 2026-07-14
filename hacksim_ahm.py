#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  🔥 HackSim AHM - بهترین شبیه‌ساز هک جهان                 ║
║  ساخته شده توسط: امیرحسین حاجی مرادخانی                    ║
║  کرمان، ایران - ۱۴۰۵                                     ║
╚══════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import random, time, json, os, threading, webbrowser
from datetime import datetime

# ════════════════ CONFIG ════════════════
VERSION = "1.0.0"
AUTHOR = "امیرحسین حاجی مرادخانی"
COLORS = {
    "bg": "#0a0a0a",
    "fg": "#00ff00",
    "accent": "#00cc00",
    "error": "#ff0000",
    "warning": "#ffff00",
    "text": "#ffffff"
}

PROGRESS_FILE = "hacksim_progress.json"

# ════════════════ DATA ════════════════
CHALLENGES = {
    "آسان": [
        {"name": "اسکن پورت", "tool": "Nmap", "desc": "پورت‌های باز رو پیدا کن!", "solution": "22,80,443"},
        {"name": "حدس عدد", "tool": "Hydra", "desc": "عدد بین ۱ تا ۱۰۰ رو حدس بزن!", "solution": random.randint(1,100)},
        {"name": "شنود پیام", "tool": "Wireshark", "desc": "پیام مخفی رو پیدا کن!", "solution": "hacksim_ahm"},
        {"name": "رمز ۴ رقمی", "tool": "John", "desc": "رمز ۴ رقمی رو پیدا کن!", "solution": "1234"},
        {"name": "پینگ شبکه", "tool": "Nmap", "desc": "آی‌پی روتر رو پیدا کن!", "solution": "192.168.1.1"},
        {"name": "تزریق SQL ساده", "tool": "SQLmap", "desc": "با تزریق SQL به دیتابیس نفوذ کن!", "solution": "admin' --"},
        {"name": "اسکن دایرکتوری", "tool": "Nikto", "desc": "پیدا کردن دایرکتوری مخفی", "solution": "/admin"},
        {"name": "شکستن WEP", "tool": "Aircrack", "desc": "کلید WEP رو پیدا کن!", "solution": "1234567890"},
        {"name": "شناسایی فیشینگ", "tool": "SocialFish", "desc": "آدرس فیشینگ رو شناسایی کن!", "solution": "http://fake-bank.com"},
        {"name": "آنالیز هدر", "tool": "Burp Suite", "desc": "توکن مخفی رو پیدا کن!", "solution": "X-SECRET-TOKEN: ahm2026"}
    ],
    "معمولی": [
        {"name": "اسکن پیشرفته", "tool": "Nmap", "desc": "سیستم‌عامل دستگاه رو پیدا کن!", "solution": "Linux"},
        {"name": "کرک پسورد", "tool": "Hydra", "desc": "پسورد ۵ رقمی رو پیدا کن!", "solution": "99999"},
        {"name": "رمزگشایی هش", "tool": "John", "desc": "هش SHA-256 رو رمزگشایی کن!", "solution": "hacksim"},
        {"name": "شنود HTTPS", "tool": "Wireshark", "desc": "داده‌های رمزنگاری شده رو پیدا کن!", "solution": "SNI: example.com"},
        {"name": "SQL Injection", "tool": "SQLmap", "desc": "با SQL Injection وارد ادمین شو!", "solution": "admin' OR '1'='1"},
        {"name": "حملات XSS", "tool": "Burp Suite", "desc": "یه XSS ساده اجرا کن!", "solution": "<script>alert('HackSim AHM')</script>"},
        {"name": "کرک WPA", "tool": "Aircrack", "desc": "رمز WPA رو با دیکشنری پیدا کن!", "solution": "password123"},
        {"name": "مهندسی اجتماعی", "tool": "SocialFish", "desc": "صفحه فیشینگ بانک رو شناسایی کن!", "solution": "https://fake-bank.ir"},
        {"name": "اسکن آسیب‌پذیری", "tool": "Nikto", "desc": "آسیب‌پذیری سرور رو پیدا کن!", "solution": "CVE-2021-44228"},
        {"name": "دسترسی به فایل", "tool": "Metasploit", "desc": "فایل /etc/passwd رو بخون!", "solution": "root:x:0:0:root:/root:/bin/bash"}
    ],
    "سخت": [
        # ... چالش‌های سطح سخت
    ],
    "خیلی سخت": [
        # ... چالش‌های سطح خیلی سخت
    ],
    "فوق‌العاده سخت": [
        # ... چالش‌های سطح فوق‌العاده سخت
    ]
}

# ════════════════ کلاس اصلی ════════════════
class HackSimAHM:
    def __init__(self, root):
        self.root = root
        self.root.title(f"🔥 HackSim AHM v{VERSION}")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(True, True)
        
        self.user_data = self.load_progress()
        self.current_challenge = None
        self.current_level = None
        self.score = 0
        self.completed = 0
        
        self.build_ui()
        self.update_status()
    
    def build_ui(self):
        # ═══ Header ═══
        header = tk.Frame(self.root, bg=COLORS["bg"])
        header.pack(fill=tk.X, padx=20, pady=(20,0))
        
        tk.Label(header, text="🔥 HackSim AHM", font=("Courier", 28, "bold"),
                fg=COLORS["fg"], bg=COLORS["bg"]).pack(side=tk.LEFT)
        
        tk.Label(header, text=f"v{VERSION}", font=("Arial", 12),
                fg=COLORS["accent"], bg=COLORS["bg"]).pack(side=tk.LEFT, padx=10)
        
        tk.Label(header, text=f"👑 {AUTHOR}", font=("Arial", 10),
                fg=COLORS["text"], bg=COLORS["bg"]).pack(side=tk.RIGHT)
        
        # ═══ منو ═══
        menu_frame = tk.Frame(self.root, bg=COLORS["bg"])
        menu_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # انتخاب سطح
        tk.Label(menu_frame, text="📊 سطح:", fg=COLORS["text"], bg=COLORS["bg"],
                font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.level_var = tk.StringVar(value="آسان")
        levels = list(CHALLENGES.keys())
        level_menu = ttk.Combobox(menu_frame, textvariable=self.level_var,
                                 values=levels, state="readonly", width=15)
        level_menu.pack(side=tk.LEFT, padx=5)
        level_menu.bind("<<ComboboxSelected>>", self.on_level_change)
        
        # دکمه‌ها
        tk.Button(menu_frame, text="🎯 شروع چالش", command=self.start_challenge,
                 bg=COLORS["fg"], fg=COLORS["bg"], font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        
        tk.Button(menu_frame, text="📊 آمار", command=self.show_stats,
                 bg=COLORS["accent"], fg=COLORS["bg"], font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(menu_frame, text="💾 ذخیره", command=self.save_progress,
                 bg="#444444", fg=COLORS["text"], font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(menu_frame, text="🌙 تم", command=self.toggle_theme,
                 bg="#333333", fg=COLORS["text"], font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # ═══ نمایش اطلاعات ═══
        info_frame = tk.Frame(self.root, bg=COLORS["bg"])
        info_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.score_label = tk.Label(info_frame, text="🏆 امتیاز: 0", fg=COLORS["fg"],
                                   bg=COLORS["bg"], font=("Arial", 12, "bold"))
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.completed_label = tk.Label(info_frame, text="✅ تکمیل شده: 0", fg=COLORS["accent"],
                                       bg=COLORS["bg"], font=("Arial", 12, "bold"))
        self.completed_label.pack(side=tk.LEFT, padx=20)
        
        self.tool_label = tk.Label(info_frame, text="🔧 ابزار: -", fg=COLORS["text"],
                                  bg=COLORS["bg"], font=("Arial", 11))
        self.tool_label.pack(side=tk.LEFT, padx=20)
        
        self.timer_label = tk.Label(info_frame, text="⏱️ 00:00", fg=COLORS["warning"],
                                   bg=COLORS["bg"], font=("Arial", 12, "bold"))
        self.timer_label.pack(side=tk.RIGHT, padx=10)
        
        # ═══ توضیحات چالش ═══
        self.desc_frame = tk.Frame(self.root, bg="#1a1a1a", relief=tk.FLAT, bd=2)
        self.desc_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.desc_label = tk.Label(self.desc_frame, text="🔐 یک سطح را انتخاب کن و شروع کن!",
                                  fg=COLORS["text"], bg="#1a1a1a",
                                  font=("Arial", 13), wraplength=800, justify=tk.CENTER)
        self.desc_label.pack(pady=20)
        
        # ═══ ورودی و خروجی ═══
        main_frame = tk.Frame(self.root, bg=COLORS["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # ورودی
        input_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(input_frame, text="💬 پاسخ:", fg=COLORS["text"],
                bg=COLORS["bg"], font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.answer_entry = tk.Entry(input_frame, bg="#1a1a1a", fg=COLORS["fg"],
                                    font=("Courier", 12), width=50, relief=tk.FLAT)
        self.answer_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.answer_entry.bind("<Return>", lambda e: self.check_answer())
        
        tk.Button(input_frame, text="✅ بررسی", command=self.check_answer,
                 bg=COLORS["fg"], fg=COLORS["bg"], font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(input_frame, text="💡 راهنما", command=self.show_hint,
                 bg=COLORS["warning"], fg=COLORS["bg"], font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # خروجی
        output_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.output = scrolledtext.ScrolledText(output_frame, bg="#1a1a1a",
                                                fg=COLORS["fg"], font=("Courier", 10),
                                                relief=tk.FLAT, insertbackground=COLORS["fg"],
                                                wrap=tk.WORD, height=12)
        self.output.pack(fill=tk.BOTH, expand=True)
        self.output.insert(tk.END, "🚀 HackSim AHM آماده است!\n")
        self.output.insert(tk.END, "📌 یک سطح انتخاب کن و شروع کن!\n")
        self.output.insert(tk.END, "═" * 60 + "\n")
        self.output.see(tk.END)
        
        # ═══ فوتر ═══
        footer = tk.Frame(self.root, bg=COLORS["bg"])
        footer.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(footer, text=f"© ۱۴۰۵ | ساخته شده در کرمان، ایران 🇮🇷",
                fg="#666666", bg=COLORS["bg"], font=("Arial", 8)).pack(side=tk.LEFT)
        
        tk.Label(footer, text=f"🔥 {AUTHOR} | {VERSION}",
                fg="#666666", bg=COLORS["bg"], font=("Arial", 8)).pack(side=tk.RIGHT)
    
    def on_level_change(self, event):
        level = self.level_var.get()
        if level in CHALLENGES:
            total = len(CHALLENGES[level])
            done = sum(1 for c in CHALLENGES[level] 
                      if f"{level}_{c['name']}" in self.user_data.get("completed", []))
            self.output.insert(tk.END, f"📊 سطح {level}: {done}/{total} چالش تکمیل شده\n")
    
    def start_challenge(self):
        level = self.level_var.get()
        if level not in CHALLENGES:
            messagebox.showerror("خطا", "سطح معتبر نیست!")
            return
        
        # پیدا کردن چالش ناقص
        challenges = CHALLENGES[level]
        completed = set(self.user_data.get("completed", []))
        
        for challenge in challenges:
            key = f"{level}_{challenge['name']}"
            if key not in completed:
                self.current_challenge = challenge
                self.current_level = level
                self.start_timer()
                self.show_challenge()
                return
        
        # همه چالش‌ها تکمیل شدن
        messagebox.showinfo("تبریک! 🎉", f"همه‌ی چالش‌های سطح {level} رو تکمیل کردی!")
        self.output.insert(tk.END, f"🎉 تبریک! همه چالش‌های سطح {level} تکمیل شد!\n")
    
    def show_challenge(self):
        c = self.current_challenge
        self.desc_label.config(text=f"🔧 ابزار: {c['tool']}\n📝 {c['desc']}")
        self.tool_label.config(text=f"🔧 {c['tool']}")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        self.output.insert(tk.END, f"\n{'═' * 60}\n")
        self.output.insert(tk.END, f"🎯 چالش: {c['name']}\n")
        self.output.insert(tk.END, f"🛠️ ابزار: {c['tool']}\n")
        self.output.insert(tk.END, f"📝 {c['desc']}\n")
        self.output.insert(tk.END, "💬 پاسخ خود را وارد کنید:\n")
        self.output.see(tk.END)
    
    def check_answer(self):
        if not self.current_challenge:
            messagebox.showinfo("⚠️", "اول یک چالش شروع کن!")
            return
        
        answer = self.answer_entry.get().strip()
        solution = self.current_challenge['solution']
        
        if str(answer).lower() == str(solution).lower():
            # پاسخ درست
            key = f"{self.current_level}_{self.current_challenge['name']}"
            if key not in self.user_data.get("completed", []):
                self.user_data.setdefault("completed", []).append(key)
                self.user_data["score"] = self.user_data.get("score", 0) + 10
                self.score = self.user_data["score"]
                self.completed = len(self.user_data["completed"])
                self.update_status()
                self.save_progress()
            
            self.output.insert(tk.END, f"✅ پاسخ صحیح! 🎉\n")
            self.output.insert(tk.END, f"🏆 +۱۰ امتیاز! امتیاز کل: {self.score}\n")
            messagebox.showinfo("✅ موفق!", f"آفرین! پاسخ درست بود!\nامتیاز: {self.score}")
            self.stop_timer()
            self.current_challenge = None
            self.start_challenge()
        else:
            self.output.insert(tk.END, f"❌ پاسخ نادرست! دوباره تلاش کن.\n")
            self.answer_entry.delete(0, tk.END)
    
    def show_hint(self):
        if self.current_challenge:
            c = self.current_challenge
            hint = f"💡 راهنما: برای {c['tool']}، معمولاً پاسخ چیزی شبیه به {c['solution'][:10]}... است."
            messagebox.showinfo("💡 راهنما", hint)
    
    def start_timer(self):
        self.timer_seconds = 0
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        if hasattr(self, 'timer_running') and self.timer_running:
            self.timer_seconds += 1
            mins, secs = divmod(self.timer_seconds, 60)
            self.timer_label.config(text=f"⏱️ {mins:02d}:{secs:02d}")
            self.root.after(1000, self.update_timer)
    
    def stop_timer(self):
        self.timer_running = False
    
    def update_status(self):
        self.score_label.config(text=f"🏆 امتیاز: {self.user_data.get('score', 0)}")
        self.completed_label.config(text=f"✅ تکمیل شده: {len(self.user_data.get('completed', []))}")
    
    def show_stats(self):
        total = 0
        done = 0
        for level, challenges in CHALLENGES.items():
            total += len(challenges)
            done += sum(1 for c in challenges 
                       if f"{level}_{c['name']}" in self.user_data.get("completed", []))
        
        stats = f"📊 آمار کلی\n{'═' * 40}\n"
        stats += f"✅ چالش‌های تکمیل شده: {done}/{total}\n"
        stats += f"🏆 امتیاز کل: {self.user_data.get('score', 0)}\n"
        stats += f"📅 آخرین به‌روزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        
        messagebox.showinfo("📊 آمار", stats)
    
    def toggle_theme(self):
        # تغییر تم ساده
        if COLORS["bg"] == "#0a0a0a":
            COLORS["bg"] = "#f0f0f0"
            COLORS["fg"] = "#006600"
            COLORS["text"] = "#000000"
        else:
            COLORS["bg"] = "#0a0a0a"
            COLORS["fg"] = "#00ff00"
            COLORS["text"] = "#ffffff"
        
        self.root.configure(bg=COLORS["bg"])
        messagebox.showinfo("🌙 تم", "تم تغییر کرد! برای اعمال کامل، برنامه رو ری‌استارت کن.")
    
    def load_progress(self):
        if os.path.exists(PROGRESS_FILE):
            try:
                with open(PROGRESS_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {"score": 0, "completed": []}
        return {"score": 0, "completed": []}
    
    def save_progress(self):
        try:
            with open(PROGRESS_FILE, 'w') as f:
                json.dump(self.user_data, f, indent=2)
            self.output.insert(tk.END, "💾 پیشرفت ذخیره شد!\n")
        except Exception as e:
            messagebox.showerror("خطا", f"مشکل در ذخیره: {e}")

# ════════════════ RUN ════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app = HackSimAHM(root)
    root.mainloop()