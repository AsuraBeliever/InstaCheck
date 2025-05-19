import instaloader
import tkinter as tk

class InstagramAccount:
    def __init__(self, title : str, resolution : str):
        self.L = instaloader.Instaloader()
        self.login_window = tk.Tk()
        self.login_window.title(title)
        self.login_window.geometry(resolution)
    
    def getUserData(self):
        tk.Label(self.login_window, text="Username").pack()
        username_box = tk.Entry(self.login_window)
        username_box.pack()
        tk.Label(self.login_window, text="Password").pack()
        password_box = tk.Entry(self.login_window)
        password_box.pack()
        tk.Button(self.login_window, text="Save", command=self.login).pack()
        return username_box.get(), password_box.get()

    def login(self):
        username, password = self.getUserData()
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
        tk.Button(success_window, text="Done", command= lambda: [success_window.destroy(), self.login_window.destroy()]).pack()
        self.login_window.mainloop()





