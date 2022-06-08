# Website Configuration
PAGE_TITLE = "SkyUtils"
ICON = "https://i.imgur.com/oNGGP6G.png"
OWNER = "280139294327308299"

# Home Page
MAIN_PAGE = "http://localhost/creator"

# Page URL
URL = "http://localhost"

# Streamlit Backend URL
BACKEND_URL = "http://localhost:8501"

# Discord Authentication Data
LOGIN_URL = "http://localhost/login"
LOGOUT_URL = "http://localhost/logout"
REDIRECT_URL = "http://localhost/login/redirect"
AUTH = "https://discord.com/api/oauth2/authorize?client_id=938139939147743233&redirect_uri=http%3A%2F%2Flocalhost%2Flogin%2Fredirect&response_type=code&scope=identify"
CLIENT_ID = "938139939147743233"
CLIENT_SECRET = "CLIENT SECRET FOR DISCORD AUTHENTICATION"

# Database
DB_CONNECTION = "MONGO DB Connetion format for python"

# Cookie Signature
SIGNATURE_KEY = b'COOKIE SIGNATURE KEY LITERALLY CAN BE ANY RANDOMLY GENERATED KEY'

# Page Configuration
page_config = {
    "creator": {
        "display_name": "Item Creator",
        "page_link": "/creator",
        "nav_link": "/?nav=creator",
        "page_file": "item_creator",
        "restricted": False
    },
    "gallery": {
        "display_name": "Hypixel Item Gallery",
        "page_link": "/gallery/home",
        "nav_link": "/?nav=gallery",
        "page_file": "gallery",
        "restricted": False
    },
    "donate": {
        "display_name": "Donate",
        "link": "https://ko-fi.com/poke535",
        "restricted": False
    },
    "atlas_discord": {
        "display_name": "Atlas Discord",
        "link": "https://discord.gg/atlasmc",
        "restricted": False
    },
    "admin": {
        "display_name": "Admin Panel",
        "page_link": "/admin",
        "nav_link": "/?nav=admin",
        "page_file": "admin",
        "restricted": True
    }
}
