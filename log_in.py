import instaloader
from instaloader.instaloader import _get_config_dir
import tkinter as tk
import os

class InstagramAccount:
    def __init__(self, title : str, resolution : str, tkinterApp : tk.Tk):
        self.L = instaloader.Instaloader()
        self.login_window = tk.Toplevel(tkinterApp)
        self.login_window.title(title)
        self.login_window.geometry(resolution)
        self.logged_in_username = None
        self.followers_check = tkinterApp
        self.followers_check.withdraw()

        session_dir = instaloader.instaloader._get_config_dir()
        usernames = []
        for f in os.listdir(session_dir):
            username = f[len("session-"):]
            usernames.append(username)

        #Interfaz
        if usernames:
            for username in usernames:
                tk.Label(self.login_window, text=username).pack()
                tk.Button(self.login_window, text="Login", command= lambda u=username: self.login(u)).pack()
        else:
            tk.Label(self.login_window, text="Username").pack()
            self.username_box = tk.Entry(self.login_window)
            self.username_box.pack()
            tk.Label(self.login_window, text="Password").pack()
            self.password_box = tk.Entry(self.login_window, show="*")
            self.password_box.pack()
            tk.Button(self.login_window, text="Save", command=self.login).pack()
    
    def getUserData(self):
        return self.username_box.get(), self.password_box.get()

    def login(self, username):
        try:
            username, password = self.getUserData()
        except:
            username = username

        try:
            self.L.load_session_from_file(username)
        except FileNotFoundError:
            try:
                self.L.login(username, password) # Should prompt for 2FA
                self.L.save_session_to_file()
            except instaloader.exceptions.TwoFactorAuthRequiredException:
                code = self.twoFactorAuthCode()
                self.L.two_factor_login(code)
                self.L.save_session_to_file()

        self.logged_in_username = username
        self.showSuccessWindow()

    def twoFactorAuthCode(self):
        code = None
        auth_window = tk.Toplevel(self.login_window)
        auth_window.title("Two Factor Authentication")
        auth_window.geometry("250x300")
        tk.Label(auth_window, text="Enter code").pack()
        code_box = tk.Entry(auth_window)
        code_box.pack()
        def getCode():
            nonlocal code
            code = code_box.get()
            auth_window.destroy()
        
        tk.Button(auth_window, text="Send", command=getCode).pack()
        auth_window.wait_window()
        return code

    def showSuccessWindow(self):
        success_window = tk.Toplevel(self.login_window)
        success_window.title("Success!")
        success_window.geometry("200x200")
        tk.Label(success_window, text="Logged in successfully!").pack()
        tk.Button(success_window, text="Done", command= lambda: [success_window.destroy(), self.login_window.destroy(), self.followers_check.deiconify()]).pack()
