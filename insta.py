import instaloader
import tkinter as tk
import os

followers_check = tk.Tk()
followers_check.title("Instagram Followers Checker")
followers_check.geometry("500x400")

USERNAME = "alanmnjz"
FOLLOWERS_FILE = "followers.txt"

# Get your profile
L = instaloader.Instaloader()
profile = instaloader.Profile.from_username(L.context, USERNAME)

# Get current followers and followees
current_followers = set(f.username for f in profile.get_followers())
current_followees = set(f.username for f in profile.get_followees())

# ========== CHECK UNFOLLOWERS ==========
if os.path.exists(FOLLOWERS_FILE):
    with open(FOLLOWERS_FILE, "r") as file:
        previous_followers = set(line.strip() for line in file.readlines())

    unfollowers = previous_followers - current_followers

    # print("\n📉 People who unfollowed you since last check:")
    tk.Label(followers_check, text="📉 People who unfollowed you since last check:").pack()

    if unfollowers:
        for user in sorted(unfollowers):
            # print(user)
            tk.Label(followers_check, text=user).pack()
    else:
        # print("No one unfollowed you.")
        tk.Label(followers_check, text="No one unfolled you.").pack()
else:
    # print("📄 First run — saving your followers list.")
    tk.Label(followers_check, text="📄 First run — saving your followers list.").pack()

# Save current followers to file for next time
with open(FOLLOWERS_FILE, "w") as file:
    for user in sorted(current_followers):
        file.write(user + "\n")

# ========== CHECK WHO DOESN'T FOLLOW BACK ==========
not_following_back = current_followees - current_followers

# print("\n🙈 People you follow who don't follow you back:")
tk.Label(followers_check, text="🙈 People you follow who don't follow you back:").pack()
if not_following_back:
    for user in sorted(not_following_back):
        # print(user)
        tk.Label(followers_check, text=user).pack()
else:
    # print("Everyone you follow follows you back!")
    tk.Label(followers_check, text="Everyone you follow follows you back!").pack()


followers_check.mainloop()