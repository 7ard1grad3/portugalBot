# README for Appointment Availability Checker

## Overview
This Python script is designed to automate the process of checking for available appointments on a specific website. It uses Selenium WebDriver for browser automation and sends notifications via Telegram when an appointment becomes available or if there are no appointments.

## Features
- Automated browser control using Selenium.
- Checks availability of appointments on a predefined website.
- Sends notifications through Telegram bot.
- Supports headless browser mode for background operation.
- Customizable for specific user ID and appointment date.

## Requirements
- Python 3.x

## Installation
1. Install Python dependencies:
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```
2. Set up environment variables in a `.env` file:
   ```
   PASSPORT_ID=<Your Passport ID>
   PASSPORT_DATE=<Your Date of Birth in DD-MM-YYYY format>
   TELEGRAM_TOKEN=<Your Telegram Bot Token>
   TELEGRAM_GROUP=<Your Telegram Chat ID>
   INFORM_ON_MISSING=<Set to 'True' to receive alerts when no appointments are available>
   ```

## Usage
Run the script:
```bash
python main.py
```
- The script will automatically open a Chrome browser window.
- It navigates to the specified URL and checks for appointment availability.
- If an appointment is available or no appointments are found, it sends a notification through Telegram.

## Function Descriptions
- `start_webdriver(headless)`: Initializes and returns a Chrome WebDriver instance.
- `appointment_is_available(browser)`: Checks if the appointment is available on the website.
- `send_telegram_message(message, token, chat_id)`: Sends a message via Telegram.

## Customization
You can customize the script by changing the `URL` and `SEARCH_TEXT` variables to match the specific requirements of the website you are monitoring.

## Troubleshooting
Ensure that all environment variables are correctly set in the `.env` file. If the script fails, check the log for errors.

## Note
This script is intended for educational purposes and should be used responsibly. Please comply with the terms of service of the website and Telegram.

---

Replace `main.py` with the actual name of your script file. Also, ensure that the users of this script are aware of the legal and ethical implications of using such automated tools on websites.