# User.py
# Handles login functionality and UI

import customtkinter as ctk
import tkinter.messagebox as tkmb
from DataStorage import DataStorage

class User:
    def __init__(self, storage):
        self.storage = storage
        self.logged_in_user = None

    def login(self):
        email = self.user_entry.get()
        password = self.user_pass.get()

        if self.storage.validate_login(email, password):
            self.logged_in_user = email
            tkmb.showinfo(title="Login Successful",message="You have logged in successfully")
        else:
            tkmb.showerror(title="Login Failed",message="Invalid email and/or password")

    def create_login_ui(self):
        ctk.set_appearance_mode("light")

        app = ctk.CTk()
        app.geometry("400x400")
        app.title("Baddie Health Tracker Login Page")

        label = ctk.CTkLabel(app,text="Baddie Health Tracker",font=ctk.CTkFont(family="Gabriola",size=20,weight="bold"))
        label.pack(pady=20)

        frame = ctk.CTkFrame(master=app,fg_color="#FFD1DC",border_color="FFE3EA")
        frame.pack(pady=20,padx=40,fill="both",expand=True)

        label = ctk.CTkLabel(master=frame,text='Login')
        label.pack(pady=12,padx=10)

        self.user_entry = ctk.CTkEntry(master=frame,placeholder_text="Email")
        self.user_entry.pack(pady=12,padx=10)

        self.user_pass = ctk.CTkEntry(master=frame,placeholder_text="Password",show="*")
        self.user_pass.pack(pady=12,padx=10)

        button = ctk.CTkButton(master=frame,fg_color="#997D84",text='Login',hover=False,command=self.login)
        button.pack(pady=12,padx=10)

        app.mainloop()