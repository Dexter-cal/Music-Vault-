from flask import Flask, jsonify
from threading import Thread
from waitress import serve

from musicvault.view_manager import ViewManager

DB_PATH = "musicvault.db"

def create_api_server():
    """Creates and configures the Flask application for the local API."""
    app = Flask(__name__)

    def get_view_manager():
        """Creates a new ViewManager instance for each request."""
        return ViewManager(DB_PATH)

    @app.route('/api/tracks', methods=['GET'])
    def get_all_tracks():
        with get_view_manager() as view_manager:
            tracks = view_manager.get_all_tracks()
            return jsonify([track.__dict__ for track in tracks])

    @app.route('/api/artists', methods=['GET'])
    def get_artists():
        with get_view_manager() as view_manager:
            artists = view_manager.get_distinct_artists()
            return jsonify(artists)

    @app.route('/api/tracks/artist/<string:artist_name>', methods=['GET'])
    def get_tracks_by_artist(artist_name):
        with get_view_manager() as view_manager:
            tracks = view_manager.get_tracks_by_artist(artist_name)
            return jsonify([track.__dict__ for track in tracks])

    return app

def run_server(app, host='0.0.0.0', port=5000):
    """Runs the Flask server using waitress."""
    print(f"Starting API server on http://{host}:{port}")
    serve(app, host=host, port=port)

class ServerThread(Thread):
    """A thread that runs the Flask API server."""
    def __init__(self, app):
        super().__init__()
        self.app = app

    def run(self):
        run_server(self.app)
