# MagTag Fortune Teller

A whimsical daily fortune display for the Adafruit MagTag e-ink device. Each day, your MagTag will show you an AI-generated fortune cookie message, a randomly selected favored zodiac sign, and the current Mercury retrograde status.

**Note:** This project requires an OpenAI API key to generate fortunes. You'll need to [sign up for an OpenAI account](https://platform.openai.com/signup) and [create an API key](https://platform.openai.com/api-keys) before using this project. I'm happy to supply the code, but footing the bill for the AI is up to you.

## Features

- **AI-Generated Fortunes**: Fetches unique, whimsical fortunes from OpenAI's GPT-5.1 API
- **Zodiac Sign**: Randomly selects a "favored sign" each day
- **Mercury Retrograde Status**: Checks whether Mercury is in retrograde using the Mercury Retrograde API
- **Energy Efficient**: Uses deep sleep mode to update every 12 hours for extended battery life
- **Error Handling**: Displays fallback messages if network or API requests fail

## Hardware Requirements

- Adafruit MagTag (ESP32-S2 with 2.9" e-ink display)
- Wi-Fi network access
- USB cable for initial setup

## Setup

1. **Install CircuitPython** on your MagTag if you haven't already (follow [Adafruit's guide](https://learn.adafruit.com/adafruit-magtag))

2. **Install Required Libraries**: Copy the following libraries to your MagTag's `lib` folder:
   - `adafruit_magtag`
   - `adafruit_requests`
   - `adafruit_display_text`

3. **Configure Your Secrets**:
   ```bash
   cp secrets.py.sample secrets.py
   ```

   Edit `secrets.py` and add your own values:
   - `ssid`: Your Wi-Fi network name
   - `password`: Your Wi-Fi password
   - `openai_api_key`: Your OpenAI API key ([get one here](https://platform.openai.com/api-keys))

4. **Deploy**: Copy `code.py` and `secrets.py` to your MagTag's root directory. The device will automatically reset and run the code.

## How It Works

When the MagTag powers on or wakes from deep sleep:
1. Connects to your Wi-Fi network
2. Requests a fortune from the OpenAI API
3. Selects a random zodiac sign
4. Checks Mercury's retrograde status
5. Displays everything on the e-ink screen
6. Enters deep sleep for 12 hours

If any network request fails, the device displays appropriate fallback messages so you always get a fortune display.

## Customization

- **Fortune Style**: Edit the prompt on line 77 of `code.py` to change the fortune generation style
- **Sleep Duration**: Modify the deep sleep duration (currently 43200 seconds / 12 hours) on line 162
- **Display Layout**: Adjust `SCREEN_WIDTH`, `SCREEN_HEIGHT`, and `LINE_HEIGHT` constants for different text layouts

## License

This project is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) (Creative Commons Attribution-NonCommercial 4.0 International). You are free to share and adapt this work for non-commercial purposes, provided you give appropriate credit.
