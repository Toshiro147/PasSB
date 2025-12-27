from gui import App
from encryptor import Encryptor
from database import Database
from tkinter import messagebox
import os
import pyautogui
import time

class VaultController:
    def __init__(self):
        self.db = Database()
        self.encryptor = None
        self.app = App(self)
        self.app.mainloop()

    def handle_auth(self):
        password = self.app.password_entry.get()
        if len(password) < 4:
            messagebox.showerror("Hata", "Şifre çok kısa!")
            return

        is_new = not os.path.exists("vault_data/.salt")
        self.encryptor = Encryptor(password)
        if is_new: messagebox.showinfo("Başarılı", "Kasa oluşturuldu!")
        self.show_main_vault()

    def handle_save(self, data):
        encrypted = self.encryptor.encrypt(data['pass'])
        self.db.add_entry(data['app'], data['user'], encrypted, data['title'])
        self.show_main_vault()

    def show_main_vault(self):
        entries = self.db.get_all_entries()
        self.app.show_dashboard(entries)

    def handle_fill(self, entry):
        decrypted = self.encryptor.decrypt(entry[3])
        if decrypted:
            messagebox.showinfo("Bilgi", "5 saniye içinde kutucuğa tıklayın.")
            time.sleep(5)
            pyautogui.write(entry[2])
            pyautogui.press('tab')
            pyautogui.write(decrypted)
            pyautogui.press('enter')
        else:
            messagebox.showerror("Hata", "Şifre çözülemedi!")

if __name__ == "__main__":
    VaultController()