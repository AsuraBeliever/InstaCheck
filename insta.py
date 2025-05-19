import instaloader
import tkinter as tk
from tkinter import ttk
from threading import Thread
from log_in import InstagramAccount
import os

class AppFollowers(InstagramAccount):
    def __init__(self, title : str, res : str):
        self.followers_check = tk.Tk()
        self.followers_check.title(title)
        self.followers_check.geometry(res)

        super().__init__("Log-in", "450x300", self.followers_check)
        self.loading = tk.Label(self.followers_check, text="Loading followers data.. Please Wait", fg="blue")
        self.loading.pack_forget()
        self.loading_bar = ttk.Progressbar(self.followers_check, orient="horizontal", length=250, mode="determinate")
        self.loading_bar.pack_forget()

    def check_login_status(self):
        if self.logged_in_username:
            self.loading.pack(pady=20)
            self.loading_bar.pack()
            self.followers_check.update()
            # Run in a separate thread to avoid freezing
            Thread(target=self.run_follower_check, daemon=True).start()
        else:
            self.followers_check.after(500, self.check_login_status)

    def run_follower_check(self):
        FOLLOWERS_FILE = "followers.txt"
        try:
            profile_name = self.logged_in_username
            # Fetch data (this is the slow part)
            profile = instaloader.Profile.from_username(self.L.context, profile_name)
            current_followers = set(f.username for f in profile.get_followers())
            current_followees = set(f.username for f in profile.get_followees())

            # Update GUI safely using `after()`
            self.followers_check.after(0, lambda: [
                self.loading.pack_forget(),
                self.loading_bar.pack_forget(),
                self.update_gui(current_followers, current_followees, FOLLOWERS_FILE)
                ])

        except Exception as e:
            self.followers_check.after(0, lambda: [
                self.loading.pack_forget(),
                self.loading_bar.pack_forget(),
                tk.Label(self.followers_check, text=f"Error: {str(e)}", fg="red").pack()
                ])

    def update_gui(self, current_followers, current_followees, FOLLOWERS_FILE):
        # ===== CHECK UNFOLLOWERS =====
        tk.Label(self.followers_check, text="📉 People who unfollowed you since last check:").pack()
        if os.path.exists(FOLLOWERS_FILE):
            with open(FOLLOWERS_FILE, "r") as file:
                previous_followers = set(line.strip() for line in file.readlines())
                unfollowers = previous_followers - current_followers
                if unfollowers:
                    for user in sorted(unfollowers):
                        tk.Label(self.followers_check, text=user).pack()
                else:
                    tk.Label(self.followers_check, text="No one unfollowed you!").pack()
        else:
            tk.Label(self.followers_check, text="📄 First run — saving followers list.").pack()

        # Save current followers
        with open(FOLLOWERS_FILE, "w") as file:
            for user in sorted(current_followers):
                file.write(user + "\n")

        # ===== CHECK NON-FOLLOWBACKS =====
        tk.Label(self.followers_check, text="🙈 People not following you back:").pack()
        not_following_back = current_followees - current_followers
        if not_following_back:
            for user in sorted(not_following_back):
                tk.Label(self.followers_check, text=user).pack()
        else:
            tk.Label(self.followers_check, text="Everyone follows you back!").pack()

obj = AppFollowers("Instagram Followers Checker", "500x400")
obj.check_login_status()
obj.followers_check.mainloop()