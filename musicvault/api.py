from flask import Flask, jsonify, request, send_file
from musicvault.device_manager import DeviceManager

DB_PATH = "musicvault.db"
device_manager = DeviceManager(DB_PATH)

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the MusicVault API!"

@app.route('/pair', methods=['POST'])
def pair_device():
    """Pairs a new device and returns a token and QR code URL."""
    device_name = request.json.get('device_name')
    if not device_name:
        return jsonify({"error": "Device name is required."}), 400

    token = device_manager.pair_device(device_name)

    return jsonify({
        "token": token,
        "qr_code_url": f"/qr_code/{token}"
    })

@app.route('/qr_code/<token>', methods=['GET'])
def get_qr_code(token):
    """Generates and serves the QR code image for a given token."""
    if not device_manager.is_token_valid(token):
        return jsonify({"error": "Invalid or expired token."}), 404

    buffer = device_manager.get_pairing_qrcode_in_memory(token)
    return send_file(buffer, mimetype='image/png')


@app.route('/check_connection', methods=['POST'])
def check_connection():
    """Checks if a device's token is valid."""
    token = request.json.get('token')
    if not token:
        return jsonify({"error": "Token is required."}), 400

    if device_manager.is_token_valid(token):
        return jsonify({"status": "ok", "message": "Device is trusted."})
    else:
        return jsonify({"status": "error", "message": "Invalid token."}), 401


def run_api_server(port=5000):
    """Runs the Flask API server."""
    # Note: debug=True is not for production use.
    app.run(host='0.0.0.0', port=port, debug=True)
