import instaloader

# Create Instaloader instance
L = instaloader.Instaloader()

username = "alanmnjz"
password = "GalletA1812"

# Try to load a saved session first
try:
    L.load_session_from_file(username)
    print("Session loaded successfully.")
except FileNotFoundError:
    # Session not found — login required
    print("No saved session. Logging in...")
    L.login(username, password)  # This will prompt for 2FA automatically
    L.save_session_to_file()
    print("Logged in and session saved.")

# Load your profile
profile = instaloader.Profile.from_username(L.context, username)

# Get followers
print("Fetching followers...")
followers = set(f.username for f in profile.get_followers())

# Get followees (people you follow)
print("Fetching followees...")
followees = set(f.username for f in profile.get_followees())

# Calculate who doesn't follow you back
not_following_back = followees - followers

# Output
print("\nPeople who don't follow you back:")
for user in sorted(not_following_back):
    print(user)
