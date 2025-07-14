import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui
import keyboard
import sys
import os

class AutoClicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AutoClicker - بورس")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # متغیرها
        self.clicking = False
        self.click_count = 0
        self.click_speed = 0.1  # سرعت کلیک (ثانیه)
        self.target_x = 0
        self.target_y = 0
        
        self.setup_ui()
        self.setup_hotkeys()
        
    def setup_ui(self):
        # عنوان
        title_label = tk.Label(self.root, text="🎯 AutoClicker Pro", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # اطلاعات
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)
        
        # موقعیت ماوس
        self.pos_label = tk.Label(info_frame, text="موقعیت: (0, 0)", 
                                 font=("Arial", 10))
        self.pos_label.pack()
        
        # تعداد کلیک
        self.count_label = tk.Label(info_frame, text="تعداد کلیک: 0", 
                                   font=("Arial", 10))
        self.count_label.pack()
        
        # وضعیت
        self.status_label = tk.Label(info_frame, text="⏹️ متوقف", 
                                    font=("Arial", 12, "bold"))
        self.status_label.pack(pady=5)
        
        # تنظیمات سرعت
        speed_frame = tk.Frame(self.root)
        speed_frame.pack(pady=10)
        
        tk.Label(speed_frame, text="سرعت کلیک:").pack(side=tk.LEFT)
        self.speed_var = tk.StringVar(value="0.1")
        speed_entry = tk.Entry(speed_frame, textvariable=self.speed_var, width=10)
        speed_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(speed_frame, text="ثانیه").pack(side=tk.LEFT)
        
        # دکمه‌ها
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        self.start_btn = tk.Button(btn_frame, text="▶️ شروع", 
                                  command=self.toggle_clicking,
                                  bg="green", fg="white", font=("Arial", 12))
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.set_pos_btn = tk.Button(btn_frame, text="🎯 تنظیم موقعیت", 
                                    command=self.set_position,
                                    bg="blue", fg="white", font=("Arial", 12))
        self.set_pos_btn.pack(side=tk.LEFT, padx=5)
        
        # راهنمای کلیدها
        help_frame = tk.Frame(self.root)
        help_frame.pack(pady=10)
        
        help_text = """
🎮 کلیدهای میانبر:
1: شروع/توقف
2: تنظیم موقعیت
ESC: توقف اضطراری
3: ریست شمارنده
        """
        help_label = tk.Label(help_frame, text=help_text, 
                             font=("Arial", 9), justify=tk.LEFT)
        help_label.pack()
        
        # بروزرسانی موقعیت ماوس
        self.update_mouse_position()
        
    def setup_hotkeys(self):
        """تنظیم کلیدهای میانبر"""
        keyboard.add_hotkey('1', self.toggle_clicking)
        keyboard.add_hotkey('2', self.set_position)
        keyboard.add_hotkey('esc', self.emergency_stop)
        keyboard.add_hotkey('3', self.reset_counter)
        
    def update_mouse_position(self):
        """بروزرسانی موقعیت ماوس"""
        if not self.clicking:
            x, y = pyautogui.position()
            self.pos_label.config(text=f"موقعیت: ({x}, {y})")
        self.root.after(100, self.update_mouse_position)
        
    def set_position(self):
        """تنظیم موقعیت کلیک"""
        if self.clicking:
            return
            
        messagebox.showinfo("تنظیم موقعیت", 
                           "ماوس را در موقعیت مورد نظر قرار دهید و 3 ثانیه صبر کنید...")
        
        def capture_position():
            time.sleep(3)
            self.target_x, self.target_y = pyautogui.position()
            self.pos_label.config(text=f"هدف: ({self.target_x}, {self.target_y})")
            
        threading.Thread(target=capture_position, daemon=True).start()
        
    def toggle_clicking(self):
        """شروع/توقف کلیک"""
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()
            
    def start_clicking(self):
        """شروع کلیک"""
        if self.target_x == 0 and self.target_y == 0:
            messagebox.showwarning("هشدار", "ابتدا موقعیت کلیک را تنظیم کنید!")
            return
            
        try:
            self.click_speed = float(self.speed_var.get())
        except ValueError:
            self.click_speed = 0.1
            
        self.clicking = True
        self.status_label.config(text="▶️ در حال اجرا", fg="green")
        self.start_btn.config(text="⏸️ توقف", bg="red")
        
        # شروع کلیک در thread جداگانه
        threading.Thread(target=self.click_loop, daemon=True).start()
        
    def stop_clicking(self):
        """توقف کلیک"""
        self.clicking = False
        self.status_label.config(text="⏹️ متوقف", fg="red")
        self.start_btn.config(text="▶️ شروع", bg="green")
        
    def emergency_stop(self):
        """توقف اضطراری"""
        self.clicking = False
        self.status_label.config(text="🚨 توقف اضطراری", fg="red")
        self.start_btn.config(text="▶️ شروع", bg="green")
        
    def reset_counter(self):
        """ریست شمارنده"""
        self.click_count = 0
        self.count_label.config(text="تعداد کلیک: 0")
        
    def click_loop(self):
        """حلقه کلیک"""
        while self.clicking:
            try:
                pyautogui.click(self.target_x, self.target_y)
                self.click_count += 1
                self.count_label.config(text=f"تعداد کلیک: {self.click_count}")
                time.sleep(self.click_speed)
            except Exception as e:
                print(f"خطا در کلیک: {e}")
                break
                
    def run(self):
        """اجرای برنامه"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.emergency_stop()
            
if __name__ == "__main__":
    print("🚀 AutoClicker Pro در حال شروع...")
    print("📌 کلیدهای میانبر:")
    print("   1: شروع/توقف")
    print("   2: تنظیم موقعیت")
    print("   ESC: توقف اضطراری")
    print("   3: ریست شمارنده")
    
    app = AutoClicker()
    app.run()
