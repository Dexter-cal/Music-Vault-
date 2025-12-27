import os
from musicvault.vault_manager import VaultManager
from musicvault.sandbox_manager import SandboxManager
from musicvault.view_manager import ViewManager

DB_PATH = "musicvault.db"

def print_help():
    """Prints the available commands."""
    print("\nMusicVault CLI Dashboard")
    print("------------------------")
    print("Available commands:")
    print("  add <filepath>       - Add a new track to the Vault.")
    print("  artists              - List all artists.")
    print("  tracks [artist]      - List tracks, optionally filtered by artist.")
    print("  playlist new <name>  - Create a new playlist.")
    print("  playlist add <p_id> <t_id> - Add a track to a playlist.")
    print("  playlist view <p_id> - View a playlist.")
    print("  help                 - Show this help message.")
    print("  exit                 - Exit the application.")
    print("------------------------")

def main():
    """The main entry point for the MusicVault CLI application."""
    vault_manager = VaultManager(DB_PATH)
    sandbox_manager = SandboxManager(DB_PATH)
    view_manager = ViewManager(DB_PATH)

    print("Welcome to MusicVault!")
    print_help()

    try:
        while True:
            command = input("> ").strip().split()
            if not command:
                continue

            action = command[0].lower()

            if action == "exit":
                break
            elif action == "help":
                print_help()
            elif action == "add" and len(command) > 1:
                filepath = command[1]
                if not os.path.exists(filepath):
                    print(f"Error: File not found at '{filepath}'")
                    continue
                track = vault_manager.add_track(filepath)
                if track:
                    print(f"Added track: '{track.title}' by {track.artist}")
                else:
                    print(f"Error adding track at '{filepath}'.")
            elif action == "artists":
                artists = view_manager.get_distinct_artists()
                print("\nArtists:")
                for artist in artists:
                    print(f"- {artist}")
            elif action == "tracks":
                if len(command) > 1:
                    artist_name = command[1]
                    tracks = view_manager.get_tracks_by_artist(artist_name)
                else:
                    tracks = view_manager.get_all_tracks()
                print("\nTracks:")
                for t in tracks:
                    print(f"  ID: {t.id}, Title: {t.title}, Artist: {t.artist}, Album: {t.album}")
            elif action == "playlist" and len(command) > 2:
                sub_action = command[1].lower()
                if sub_action == "new":
                    playlist_name = " ".join(command[2:])
                    playlist = sandbox_manager.create_playlist(playlist_name)
                    print(f"Created playlist '{playlist.name}' with ID: {playlist.id}")
                elif sub_action == "add" and len(command) == 4:
                    playlist_id, track_id = int(command[2]), int(command[3])
                    sandbox_manager.add_track_to_playlist(playlist_id, track_id)
                    print(f"Added track {track_id} to playlist {playlist_id}.")
                elif sub_action == "view" and len(command) == 3:
                    playlist_id = int(command[2])
                    playlist = sandbox_manager.get_playlist(playlist_id)
                    if playlist:
                        print(f"\nPlaylist: {playlist.name} (ID: {playlist.id})")
                        for t in playlist.tracks:
                            print(f"  - {t.title} by {t.artist}")
                    else:
                        print("Playlist not found.")
            else:
                print("Unknown command. Type 'help' for a list of commands.")

    finally:
        vault_manager.close()
        sandbox_manager.close()
        view_manager.close()
        print("Goodbye!")

if __name__ == "__main__":
    main()
