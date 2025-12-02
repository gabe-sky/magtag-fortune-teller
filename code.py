# MagTag Fortune Teller
# Displays a daily AI-generated fortune on an Adafruit MagTag e-ink display.
# Fetches a whimsical fortune from OpenAI's GPT-5.1 API, picks a random
# favored zodiac sign, and checks Mercury's retrograde status.
# Updates once every 12 hours via deep sleep for battery efficiency.

import time
import ssl
import socketpool
import wifi
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_magtag.magtag import MagTag
import adafruit_requests
import random

from secrets import secrets

# Display layout constants
SCREEN_WIDTH = 296
SCREEN_HEIGHT = 128
LINE_HEIGHT = 12  # Approximate height of terminalio text lines

# Helper: Word-wrap text at max characters per line
def wrap_text(text, max_chars):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# 🔧 Helper: Convert smart quotes and dashes to plain ASCII
def unsmarten(text):
    return (
        text.replace("“", '"')
            .replace("”", '"')
            .replace("‘", "'")
            .replace("’", "'")
            .replace("—", "-")
            .replace("–", "-")
    )

# Zodiac signs
zodiac_signs = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Connect to Wi-Fi
try:
    print("Connecting to Wi-Fi...")
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("Connected!")
except Exception as e:
    print(f"Wi-Fi connection failed: {e}")
    fortune = "The stars are clouded. Check your connection."
    favored_sign = "Unknown"
    retro_message = "Network unavailable."
    # Skip to display
    magtag = MagTag()
    magtag.graphics.set_background(0xFFFFFF)
    error_label = label.Label(terminalio.FONT, text=fortune, color=0x000000, x=10, y=64)
    magtag.splash.append(error_label)
    magtag.refresh()
    time.sleep(5)
    magtag.exit_and_deep_sleep(43200)

# HTTP session
pool = socketpool.SocketPool(wifi.radio)
session = adafruit_requests.Session(pool, ssl.create_default_context())

# Prompt for OpenAI
prompt = "Give me a short, clever one-sentence fortune in the style of a whimsical fortune cookie."

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {secrets['openai_api_key']}"
}

# ✅ Using updated OpenAI message format
data = {
    "model": "gpt-5.1",
    "messages": [
        {
            "role": "developer",
            "content": "You are a whimsical fortune cookie generator."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
}

# Get fortune from OpenAI with error handling
try:
    print("Requesting fortune from GPT-5.1...")
    response = session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    fortune = response.json()["choices"][0]["message"]["content"].strip()
    fortune = unsmarten(fortune)  # 🧼 Clean smart quotes/dashes
except Exception as e:
    print(f"OpenAI request failed: {e}")
    fortune = "The universe whispers mysteries today."

# Pick random zodiac sign
favored_sign = random.choice(zodiac_signs)

# Get Mercury retrograde status with error handling
try:
    print("Checking Mercury retrograde...")
    retro_response = session.get("https://mercuryretrogradeapi.com")
    retro_json = retro_response.json()

    if retro_json.get("is_retrograde"):
        retro_message = "Mercury is retrograde. Stay flexible."
    else:
        retro_message = "Mercury is direct. Manifest boldly."
except Exception as e:
    print(f"Mercury retrograde check failed: {e}")
    retro_message = "Mercury status unknown."

# Display setup
magtag = MagTag()
magtag.graphics.set_background(0xFFFFFF)  # Clear display

# Wrap and center fortune
wrapped_fortune = wrap_text(fortune, max_chars=35)
fortune_height = len(wrapped_fortune) * LINE_HEIGHT
available_space = SCREEN_HEIGHT - (2 * LINE_HEIGHT + 6)
start_y = (available_space - fortune_height) // 2

fortune_group = displayio.Group()
for i, line in enumerate(wrapped_fortune):
    x = (SCREEN_WIDTH - len(line) * 6) // 2
    y = start_y + i * LINE_HEIGHT
    lbl = label.Label(terminalio.FONT, text=line, color=0x000000, x=x, y=y)
    fortune_group.append(lbl)

# Footer: sign + Mercury status pinned to bottom
footer_lines = [
    f"Today's favored sign: {favored_sign}",
    retro_message
]
footer_group = displayio.Group()
for i, line in enumerate(footer_lines):
    x = (SCREEN_WIDTH - len(line) * 6) // 2
    y = SCREEN_HEIGHT - (2 - i) * LINE_HEIGHT - 2
    lbl = label.Label(terminalio.FONT, text=line, color=0x000000, x=x, y=y)
    footer_group.append(lbl)

# Show everything
magtag.splash.append(fortune_group)
magtag.splash.append(footer_group)
magtag.refresh()

# Sleep for 12 hours
time.sleep(5)
magtag.exit_and_deep_sleep(43200)
