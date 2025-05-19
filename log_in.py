import instaloader
import tkinter as tk

def login():
    username = username_box.get()
    password = password_box.get()
    try:
        L.load_session_from_file(username)
    except FileNotFoundError:
        try:
            L.login(username, password) # Should prompt for 2FA
            L.save_session_to_file()
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            code = twoFactorAuthCode()
            L.two_factor_login(code)
            L.save_session_to_file()
        
    showSuccessWindow()

def twoFactorAuthCode():
    code = None
    auth_window = tk.Toplevel(login_window)
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

def showSuccessWindow():
    success_window = tk.Toplevel(login_window)
    success_window.title("Success!")
    success_window.geometry("200x200")
    tk.Label(success_window, text="Logged in successfully!").pack()
    tk.Button(success_window, text="Done", command= lambda: [success_window.destroy(), login_window.destroy()]).pack()

login_window = tk.Tk()
login_window.title("Log-in")
login_window.geometry("300x300")
tk.Label(login_window, text="Username").pack()
username_box = tk.Entry(login_window)
username_box.pack()
tk.Label(login_window, text="Password").pack()
password_box = tk.Entry(login_window)
password_box.pack()
tk.Button(login_window, text="Save", command=login).pack()

login_window.mainloop()

L = instaloader.Instaloader()



