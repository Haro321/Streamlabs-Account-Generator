# StreamLabs Signup Bot

A Python automation bot that signs up for a StreamLabs account by filling out the signup form and verifying the email address using a temporary email service. The bot uses a headless browser driver (powered by botasaurus_driveror a similar package) along with TempMail for email verification. It also supports the use of proxies and multithreading for concurrent signups.

## Features

- **Automated Signup Process:** Opens the signup page, fills in email and password fields, and submits the form.
- **Email Verification:** Automatically retrieves the verification code from a temporary email inbox and submits it.
- **Password Generation:** Generates a strong random password containing uppercase, lowercase, digits, and special characters.
- **Proxy Support:** Configure a proxy for the browser driver if needed.
- **Multithreading:** Supports running multiple signup processes concurrently.
- **Logging:** Logs all steps and errors to both a file (`streamlabs_signup.log`) and the console.

## Requirements

- Python 3.7+
- botasaurus_driver
- TempMail
- python-dotenv

## Installation
   ```bash
   git clone https://github.com/your-username/streamlabs-signup-bot.git
   cd streamlabs-signup-bot