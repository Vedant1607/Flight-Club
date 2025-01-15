
# Flight Price Alert System

A Python-based application that monitors flight prices and sends notifications when a price drop occurs. It integrates with external APIs such as Amadeus for flight search and Sheety for storing user and destination data. The system sends alerts via SMS, WhatsApp, and Email.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Search and compare flight prices to various destinations.
- Send notifications to users when the price of a flight drops below a specific threshold.
- Supports SMS, WhatsApp, and Email notifications.
- Integrates with Google Sheets using Sheety API to store destinations and user data.
- Fetches flight details from Amadeus API.

## Tech Stack

- **Python 3.x**: Backend logic.
- **Requests**: HTTP requests to interact with external APIs.
- **Twilio API**: For SMS and WhatsApp notifications.
- **SMTP**: For email notifications.
- **Amadeus API**: Flight search data provider.
- **Sheety API**: For storing and managing user and destination data in Google Sheets.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Vedant1607/flight-price-alert.git
cd flight-price-alert
```

### 2. Set up the environment variables

Create a `.env` file in the root directory and add the following configuration values:

```dotenv
SHEETY_USERNAME=your_sheety_username
SHEET_PASSWORD=your_sheety_password
SHEETY_PRICES_ENDPOINT=your_sheety_prices_endpoint
SHEETY_USERS_ENDPOINT=your_sheety_users_endpoint
AMADEUS_API_KEY=your_amadeus_api_key
AMADEUS_API_SECRET=your_amadeus_api_secret
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
TWILIO_TO=your_twilio_to_phone_number
TWILIO_WP_NUMBER=your_twilio_wp_number
EMAIL_PROVIDER_SMTP_ADDRESS=your_email_provider_smtp_address
MY_EMAIL=your_email
MY_EMAIL_PASSWORD=your_email_password
```

### 3. Set up the external APIs

- **Amadeus API**: Get your API key and secret from [Amadeus](https://developers.amadeus.com/).
- **Twilio**: Create an account on [Twilio](https://www.twilio.com/) to get your account SID, auth token, and phone number for SMS/WhatsApp notifications.
- **Sheety**: Set up your [Sheety account](https://sheety.co/) to link a Google Sheet for destination and user data.

## Usage

1. **Run the Application**: Once the setup is complete, you can start the flight alert system by running:

   ```bash
   python main.py
   ```

2. **Functionality**:
   - The script will fetch destination data from Sheety.
   - It will then search for flight prices using the Amadeus API.
   - If a flight price drops below the set threshold, the system will send notifications to users via SMS, WhatsApp, and Email.

3. **Viewing Alerts**: You will receive SMS and WhatsApp messages, and your email will be notified if there is a price drop for a flight.

## Configuration

Make sure to update the following values in your `.env` file:
- **SHEETY_PRICES_ENDPOINT**: The endpoint where flight price data is stored.
- **SHEETY_USERS_ENDPOINT**: The endpoint where user email data is stored.
- **AMADEUS_API_KEY** and **AMADEUS_API_SECRET**: Your Amadeus API credentials for flight search.
- **TWILIO_ACCOUNT_SID**, **TWILIO_AUTH_TOKEN**, and **TWILIO_PHONE_NUMBER**: Your Twilio credentials for sending messages.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request. Bug fixes, feature requests, and enhancements are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Acknowledgments

- [Amadeus API](https://developers.amadeus.com/) for flight search capabilities.
- [Twilio](https://www.twilio.com/) for SMS and WhatsApp messaging.
- [Sheety](https://sheety.co/) for managing Google Sheets as a database.
