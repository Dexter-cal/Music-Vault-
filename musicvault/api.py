import sqlite3
from flask import Flask, jsonify, request, send_file
from functools import wraps
from musicvault.device_manager import DeviceManager
from musicvault.view_manager import ViewManager
from musicvault.vault_manager import VaultManager

def create_app(db_path="musicvault.db"):
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    device_manager = DeviceManager(db_path)
    view_manager = ViewManager(db_path)
    vault_manager = VaultManager(db_path)

    def token_required(f):
        """Decorator to protect routes with token-based authentication."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    return jsonify({"error": "Malformed token header."}), 401

            if not token:
                return jsonify({"error": "Token is missing."}), 401

            try:
                if not device_manager.is_token_valid(token):
                    return jsonify({"error": "Token is invalid or expired."}), 401
            except sqlite3.Error as e:
                return jsonify({"error": "Database error", "message": str(e)}), 500

            return f(*args, **kwargs)
        return decorated_function

    @app.route('/')
    def index():
        return "Welcome to the MusicVault API!"

    @app.route('/pair', methods=['POST'])
    def pair_device():
        """Pairs a new device and returns a token and QR code URL."""
        device_name = request.json.get('device_name')
        if not device_name:
            return jsonify({"error": "Device name is required."}), 400

        try:
            token = device_manager.pair_device(device_name)
        except sqlite3.Error as e:
            return jsonify({"error": "Database error", "message": str(e)}), 500

        return jsonify({
            "token": token,
            "qr_code_url": f"/qr_code/{token}"
        })

    @app.route('/qr_code/<token>', methods=['GET'])
    def get_qr_code(token):
        """Generates and serves the QR code image for a given token."""
        try:
            if not device_manager.is_token_valid(token):
                return jsonify({"error": "Invalid or expired token."}), 404
        except sqlite3.Error as e:
            return jsonify({"error": "Database error", "message": str(e)}), 500

        buffer = device_manager.get_pairing_qrcode_in_memory(token)
        return send_file(buffer, mimetype='image/png')


    @app.route('/check_connection', methods=['POST'])
    def check_connection():
        """Checks if a device's token is valid."""
        token = request.json.get('token')
        if not token:
            return jsonify({"error": "Token is required."}), 400

        try:
            if device_manager.is_token_valid(token):
                return jsonify({"status": "ok", "message": "Device is trusted."})
            else:
                return jsonify({"status": "error", "message": "Invalid token."}), 401
        except sqlite3.Error as e:
            return jsonify({"error": "Database error", "message": str(e)}), 500

    # Library Endpoints
    @app.route('/library/tracks', methods=['GET'])
    @token_required
    def get_tracks():
        """Returns all tracks or tracks filtered by artist, album, or genre."""
        try:
            artist = request.args.get('artist')
            album = request.args.get('album')
            genre = request.args.get('genre')

            if artist:
                tracks = view_manager.get_tracks_by_artist(artist)
            elif album:
                tracks = view_manager.get_tracks_by_album(album)
            elif genre:
                tracks = view_manager.get_tracks_by_genre(genre)
            else:
                tracks = view_manager.get_all_tracks()

            return jsonify([track.to_dict() for track in tracks])
        except sqlite3.Error as e:
            return jsonify({"error": "Database error", "message": str(e)}), 500

    @app.route('/library/artists', methods=['GET'])
    @token_required
    def get_artists():
        """Returns a list of all distinct artists."""
        try:
            artists = view_manager.get_distinct_artists()
            return jsonify(artists)
        except sqlite3.Error as e:
            return jsonify({"error": "Database error", "message": str(e)}), 500

    @app.route('/library/albums', methods=['GET'])
    @token_required
    def get_albums():
        """Returns a list of all distinct albums."""
        try:
            albums = view_manager.get_distinct_albums()
            return jsonify(albums)
        except sqlite3.Error as e:
            return jsonify({"error": "Database error", "message": str(e)}), 500

    @app.route('/library/genres', methods=['GET'])
    @token_required
    def get_genres():
        """Returns a list of all distinct genres."""
        try:
            genres = view_manager.get_distinct_genres()
            return jsonify(genres)
        except sqlite3.Error as e:
            return jsonify({"error": "Database error", "message": str(e)}), 500

    @app.route('/stream/<int:track_id>', methods=['GET'])
    @token_required
    def stream_track(track_id):
        """Streams an audio file for a given track ID."""
        try:
            tracks = view_manager.get_track_by_id(track_id)
            if not tracks:
                return jsonify({"error": "Track not found"}), 404

            track = tracks[0]
            return send_file(track.filepath, mimetype='audio/mpeg')
        except sqlite3.Error as e:
            return jsonify({"error": "Database error", "message": str(e)}), 500
        except FileNotFoundError:
            return jsonify({"error": "File not found on server"}), 404

    return app

def run_api_server(app, port=5000):
    """Runs the Flask API server."""
    # Note: debug=True is not for production use.
    # Use the self-signed certificate and key to enable HTTPS.
    app.run(host='0.0.0.0', port=port, debug=True, ssl_context=('certs/cert.pem', 'certs/key.pem'))
