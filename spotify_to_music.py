import requests
from dataclasses import dataclass
from ytmusicapi import YTMusic

from config import CLIENT_ID, CLIENT_SECRET

# Constants
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_PLAYLIST_URL = 'https://api.spotify.com/v1/playlists/{}/tracks'
OAUTH_FILE = 'oauth.json'

@dataclass
class APITokenResponse:
    access_token: str
    expires_in: int
    token_type: str

@dataclass
class SpotifyTrack:
    name: str
    album: str
    artists: list[str]

    def __str__(self):
        return f"{self.name} | {self.album} | {self.artists}"

def get_spotify_access_token(client_id: str, client_secret: str) -> str:
    """Retrieve Spotify access token."""
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=data)
    response.raise_for_status()
    token_data = APITokenResponse(**response.json())
    return token_data.access_token

def fetch_spotify_playlist_tracks(access_token: str, playlist_id: str) -> list[dict]:
    """Fetch raw track data from Spotify playlist."""
    headers = {'Authorization': f"Bearer {access_token}"}
    response = requests.get(SPOTIFY_PLAYLIST_URL.format(playlist_id), headers=headers)
    response.raise_for_status()
    return response.json()["items"]

def extract_track_details(raw_tracks: list[dict]) -> list[SpotifyTrack]:
    """Extract track details from raw Spotify track data."""
    return [
        SpotifyTrack(
            track["track"]["name"],
            track["track"]["album"]["name"],
            [artist["name"] for artist in track["track"]["artists"]]
        ) for track in raw_tracks
    ]

def create_ytmusic_playlist_from_spotify_tracks(track_details: list[SpotifyTrack], playlist_name: str, playlist_description: str) -> dict:
    """Create a YouTube Music playlist from Spotify track details."""
    ytmusic = YTMusic(OAUTH_FILE)
    video_ids = [
        ytmusic.search(str(track_detail), filter='songs')[0]["videoId"]
        for track_detail in track_details
    ]
    return ytmusic.create_playlist(playlist_name, playlist_description, video_ids=video_ids, privacy_status='PUBLIC')

if __name__ == "__main__":
    SPOTIFY_PLAYLIST_ID = '0kw7bwWiFHoJe8qXSycKG8'
    NEW_PLAYLIST_TITLE = '30m Run'
    NEW_PLAYLIST_DESCRIPTION = 'Time to run.'

    access_token = get_spotify_access_token(CLIENT_ID, CLIENT_SECRET)
    raw_tracks = fetch_spotify_playlist_tracks(access_token, SPOTIFY_PLAYLIST_ID)
    track_details = extract_track_details(raw_tracks)
    response = create_ytmusic_playlist_from_spotify_tracks(track_details, NEW_PLAYLIST_TITLE, NEW_PLAYLIST_DESCRIPTION)
    print(response)

