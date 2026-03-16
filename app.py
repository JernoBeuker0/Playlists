
from src.spotify_auth import SpotifyAuthClient, SpotifySettings
from src.spotify_client import SpotifyClient
from src.transfer_service import PlaylistTransferService
from src.utils import print_songs
from src.yt_client import YouTubeMusicClient
from src.cli import build_parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    settings = SpotifySettings.from_env()
    auth_client = SpotifyAuthClient(settings)
    spotify_client = SpotifyClient(auth_client)
    yt_client = YouTubeMusicClient()

    if args.print_songs:
        songs = yt_client.get_playlist_tracks(args.playlist_id)
        print("Songs found in YT playlist:")
        print_songs(songs)

    transfer_service = PlaylistTransferService(
        yt_client=yt_client,
        spotify_client=spotify_client,
    )

    result = transfer_service.transfer_playlist(
        yt_playlist_id=args.playlist_id,
        spotify_playlist_name=args.new_playlist_name,
        spotify_playlist_description=args.description,
        public=False,
    )

    print(f"\nCreated Spotify playlist: {result.playlist_id}")
    print(f"Matched: {len(result.matched_songs)}")
    print(f"Missed: {len(result.missed_songs)}")

    if result.missed_songs:
        print("\nSongs not found on Spotify:")
        print_songs(result.missed_songs)


if __name__ == "__main__":
    main()