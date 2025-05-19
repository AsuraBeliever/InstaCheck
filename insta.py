import instaloader
import tkinter as tk
from threading import Thread
from log_in import InstagramAccount
import os

followers_check = tk.Tk()
followers_check.title("Instagram Followers Checker")
followers_check.geometry("500x400")
obj = InstagramAccount("Log-in", "450x300", followers_check)

loading = tk.Label(followers_check, text="Loading followers data.. Please Wait", fg="blue")
loading.pack_forget()

def check_login_status():
    if obj.logged_in_username:
        loading.pack(pady=20)
        followers_check.update()
        # Run in a separate thread to avoid freezing
        Thread(target=run_follower_check, daemon=True).start()
    else:
        followers_check.after(500, check_login_status)

def run_follower_check():
    FOLLOWERS_FILE = "followers.txt"
    try:
        L = obj.L
        profile_name = obj.logged_in_username
        
        # Fetch data (this is the slow part)
        profile = instaloader.Profile.from_username(L.context, profile_name)
        current_followers = set(f.username for f in profile.get_followers())
        current_followees = set(f.username for f in profile.get_followees())

        # Update GUI safely using `after()`
        followers_check.after(0, lambda: [
            loading.pack_forget(),
            update_gui(current_followers, current_followees, FOLLOWERS_FILE)
            ])

    except Exception as e:
        followers_check.after(0, lambda: [
            loading.pack_forget(),
            tk.Label(followers_check, text=f"Error: {str(e)}", fg="red").pack()
            ])

def update_gui(current_followers, current_followees, FOLLOWERS_FILE):
    # ===== CHECK UNFOLLOWERS =====
    tk.Label(followers_check, text="📉 People who unfollowed you since last check:").pack()
    if os.path.exists(FOLLOWERS_FILE):
        with open(FOLLOWERS_FILE, "r") as file:
            previous_followers = set(line.strip() for line in file.readlines())
            unfollowers = previous_followers - current_followers
            if unfollowers:
                for user in sorted(unfollowers):
                    tk.Label(followers_check, text=user).pack()
            else:
                tk.Label(followers_check, text="No one unfollowed you!").pack()
    else:
        tk.Label(followers_check, text="📄 First run — saving followers list.").pack()

    # Save current followers
    with open(FOLLOWERS_FILE, "w") as file:
        for user in sorted(current_followers):
            file.write(user + "\n")

    # ===== CHECK NON-FOLLOWBACKS =====
    tk.Label(followers_check, text="🙈 People not following you back:").pack()
    not_following_back = current_followees - current_followers
    if not_following_back:
        for user in sorted(not_following_back):
            tk.Label(followers_check, text=user).pack()
    else:
        tk.Label(followers_check, text="Everyone follows you back!").pack()

check_login_status()
followers_check.mainloop()