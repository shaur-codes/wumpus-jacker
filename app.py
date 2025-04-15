from flask import Flask, render_template, send_from_directory, jsonify
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='w')
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='.')
QR_FOLDER = 'qr_code'

@app.route('/')
def index():
    logger.info("Rendering index.html")
    return render_template('index.html')

@app.route('/qr-image')
def get_qr():
    logger.info("Serving QR image")
    return send_from_directory(QR_FOLDER, 'qr.png')

@app.route('/login-status')
def login_status():
    if os.path.exists('login_success.txt'):
        logger.info("Login success detected")
        return jsonify({'status': 'logged_in'})
    return jsonify({'status': 'waiting'})

if __name__ == '__main__':
    logger.info("Starting Flask app")
    app.run(debug=True, port=5000)
