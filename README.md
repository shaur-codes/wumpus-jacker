# wumpus-jacker

*wumpus-jacker* is a project that showcases how to use **Selenium** and **Flask** to automate the Discord login process via a QR code. It grabs the QR code from the Discord login page using Selenium, displays it through a Flask web app, and redirects the user to Discord once the QR code is scanned with the Discord mobile app.

*Note*: This project is **strictly for educational purposes** and *must not* be used for malicious activities like unauthorized access to Discord accounts.

## Installation

### Prerequisites
- *Python 3.x*
- *Google Chrome browser*
- *ChromeDriver* (must match your Chrome version)
- Required Python libraries: `selenium`, `flask`, `opencv-python`, `numpy`

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wumpus-jacker.git
   cd wumpus-jacker
2. Install the required libraries:
   ```pip install -r requirements.txt```
   Make sure ChromeDriver is installed and in your system's PATH
## Usage
* Run the Selenium script:
* Launch the script to open Discord's login page and capture the QR code:
  ```python run.py```
* Access the Flask app:
 Open your browser and go to http://localhost:5000.
 You’ll see the Discord QR code on the page.
* you can use ```ngrok```, ```cloudflared``` or ```srv.us``` to make it accessible over internet.
* Scan the QR code:
  Use the Discord mobile app to scan the QR code shown in the Flask app.
* Once scanned, the Selenium-controlled browser logs into Discord.

## How It Works
Selenium: Opens Chrome, visits the Discord login page, and uses OpenCV to detect and capture the QR code (the largest square contour).

Flask: Runs a webpage that shows the captured QR code and checks for login status.

Login Detection: When the QR code is scanned, Selenium notices the page change (QR code vanishes), writes a file (login_success.txt), and Flask redirects to Discord when it sees this file.

# Disclaimers and Notes
Educational Purpose: This project teaches web automation and session management techniques.

Security: The login session stays in the Selenium-controlled browser and isn’t passed to your browser due to security limits. This doesn’t bypass Discord’s security.

Usage Caution: Do not use this for unauthorized access or any harmful actions.

## Credits
Discord login Page: https://github.com/Ayanprogrammer11

