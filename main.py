import customtkinter as ctk
from encryptor import Encryptor
from database import Database
from gui import App
from watcher import Watcher 
from tkinter import messagebox
import os
import pyautogui
import time
import sys

class VaultController:
    def __init__(self):
        self.db = Database()
        self.encryptor = None
        self.app = App(self)
        self.watcher = Watcher(self)
        self.app.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.app.mainloop()

    def handle_auth(self):
        password = self.app.password_entry.get()
        if len(password) < 4:
            messagebox.showerror("Hata", "Şifre çok kısa!")
            return

        is_new = not os.path.exists("vault_data/.salt")
        
        try:
            self.encryptor = Encryptor(password)
            
            if is_new:
                canary = self.encryptor.encrypt("VAULT_OK")
                self.db.add_entry("SYSTEM_CHECK", "admin", canary, "CANARY")
                messagebox.showinfo("Başarılı", "Kasa ve Şifre oluşturuldu!")
            else:
                entries = self.db.get_all_entries()
                canary_entry = next((e for e in entries if e[4] == "CANARY"), None)
                
                if canary_entry:
                    decrypted = self.encryptor.decrypt(canary_entry[3])
                    if decrypted != "VAULT_OK":
                        messagebox.showerror("Hata", "Geçersiz Şifre!")
                        self.encryptor = None
                        return
                    
            self.watcher.start()
            self.show_main_vault()
            
        except Exception as e:
            messagebox.showerror("Hata", "Şifre doğrulanamadı!")

    def check_match(self, window_title):
        if not self.encryptor: return 

        entries = self.db.get_all_entries()
        for entry in entries:
            target_app = entry[1].lower()
            current_window = window_title.lower()
            
            if target_app in current_window:
                self.app.after(100, lambda e=entry: self.ask_to_autofill(e))
                break

    def ask_to_autofill(self, entry):
        def show_popup():
            self.app.attributes("-topmost", True)
            self.app.focus_force()
            response = messagebox.askyesno("Oto-Doldur", f"{entry[1]} algılandı. Doldurulsun mu?")
            self.app.attributes("-topmost", False)
            
            if response:
                self.perform_autofill(entry)
        self.app.after(0, show_popup)

    def perform_autofill(self, entry):
        try:
            decrypted = self.encryptor.decrypt(entry[3])
            self.app.iconify()

            if sys.platform == "darwin":
                pyautogui.hotkey('command', 'tab')
            else:
                pyautogui.hotkey('alt', 'tab')  
            
            time.sleep(0.5) 
            pyautogui.write(entry[2])
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.write(decrypted)
            time.sleep(0.1)
            pyautogui.press('enter')

            time.sleep(1)
            self.app.deiconify()
            
        except Exception as e:
            print(f"Hata: {e}")
            self.app.deiconify()

    def handle_save(self, data):
        if self.encryptor:
            encrypted = self.encryptor.encrypt(data['pass'])
            self.db.add_entry(data['app'], data['user'], encrypted, data['title'])
            self.show_main_vault()

    def handle_fill(self, entry):
        self.perform_autofill(entry)

    def show_main_vault(self):
        entries = self.db.get_all_entries()
        self.app.show_dashboard(entries)

    def force_close(self):
        print("Kilitleniyor...")
        self.app.quit()
        sys.exit()

    def on_close(self):
        self.watcher.stop()
        self.app.destroy()

if __name__ == "__main__":
    VaultController()