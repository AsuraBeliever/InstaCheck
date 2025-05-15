import instaloader
import os

USERNAME = "alanmnjz"
FOLLOWERS_FILE = "followers.txt"

# Load Instaloader session
L = instaloader.Instaloader()
L.load_session_from_file(USERNAME)

# Get your profile
profile = instaloader.Profile.from_username(L.context, USERNAME)

# Get current followers and followees
current_followers = set(f.username for f in profile.get_followers())
current_followees = set(f.username for f in profile.get_followees())

# ========== CHECK UNFOLLOWERS ==========
if os.path.exists(FOLLOWERS_FILE):
    with open(FOLLOWERS_FILE, "r") as file:
        previous_followers = set(line.strip() for line in file.readlines())

    unfollowers = previous_followers - current_followers

    print("\n📉 People who unfollowed you since last check:")
    if unfollowers:
        for user in sorted(unfollowers):
            print(user)
    else:
        print("No one unfollowed you.")
else:
    print("📄 First run — saving your followers list.")

# Save current followers to file for next time
with open(FOLLOWERS_FILE, "w") as file:
    for user in sorted(current_followers):
        file.write(user + "\n")

# ========== CHECK WHO DOESN'T FOLLOW BACK ==========
not_following_back = current_followees - current_followers

print("\n🙈 People you follow who don't follow you back:")
if not_following_back:
    for user in sorted(not_following_back):
        print(user)
else:
    print("Everyone you follow follows you back!")
