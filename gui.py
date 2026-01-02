import customtkinter as ctk
from tkinter import messagebox
import os

class AddPasswordWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_save_callback):
        super().__init__(parent)
        self.title("Yeni Şifre Ekle")
        self.geometry("400x450")
        self.on_save_callback = on_save_callback
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text="Şifre Detayları", font=("Roboto", 18, "bold")).pack(pady=20)
        self.entry_app = ctk.CTkEntry(self, placeholder_text="Uygulama Adı", width=300)
        self.entry_app.pack(pady=10)
        self.entry_user = ctk.CTkEntry(self, placeholder_text="Kullanıcı Adı", width=300)
        self.entry_user.pack(pady=10)
        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Şifre", show="*", width=300)
        self.entry_pass.pack(pady=10)
        self.entry_title = ctk.CTkEntry(self, placeholder_text="Pencere Başlığı", width=300)
        self.entry_title.pack(pady=10)

        ctk.CTkButton(self, text="Kaydet", command=self.save).pack(pady=30)

    def save(self):
        data = {"app": self.entry_app.get(), "user": self.entry_user.get(), 
                "pass": self.entry_pass.get(), "title": self.entry_title.get()}
        if all(data.values()):
            self.on_save_callback(data)
            self.destroy()
        else:
            messagebox.showwarning("Uyarı", "Tüm alanları doldurun!")

class App(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("PasSB - Password Manager")
        self.geometry("800x600")
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.show_login_screen()

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        frame = ctk.CTkFrame(self.container)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        is_registered = os.path.exists("vault_data/.salt")
        title_text = "Şifre Oluştur" if not is_registered else "Giriş Yap"
        
        ctk.CTkLabel(frame, text=title_text, font=("Roboto", 24, "bold")).pack(pady=20)
        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Şifre", show="*", width=250)
        self.password_entry.pack(pady=10)

        btn_text = "Kaydet" if not is_registered else "Giriş"
        ctk.CTkButton(frame, text=btn_text, command=self.controller.handle_auth).pack(pady=20)

    def show_dashboard(self, entries=None):
        self.clear_screen()
        if entries is None: entries = []
        
        top = ctk.CTkFrame(self.container, height=60)
        top.pack(side="top", fill="x", padx=10, pady=10)
        ctk.CTkLabel(top, text="Kayıtlı Şifreler", font=("Roboto", 20)).pack(side="left", padx=20)
        ctk.CTkButton(top, text="+ Yeni Ekle", command=lambda: AddPasswordWindow(self, self.controller.handle_save)).pack(side="right", padx=20)

        scroll = ctk.CTkScrollableFrame(self.container)
        scroll.pack(fill="both", expand=True, padx=20, pady=20)

        for entry in entries:
            row = ctk.CTkFrame(scroll)
            row.pack(fill="x", pady=5)
            ctk.CTkLabel(row, text=f"{entry[1]} | {entry[2]}").pack(side="left", padx=10)
            ctk.CTkButton(row, text="Doldur", width=60, command=lambda e=entry: self.controller.handle_fill(e)).pack(side="right", padx=5)