# Setup

1. Install the necessary requirements.
`$ python -m pip install -r requirements.txt`
2. Run `setup_oauth.py` to setup headers for `ytmusicapi` in a file named `oauth.json`.
`$ python setup_oauth.py`
3. Edit the variables in `SpotifyToMusic.py` as desired.
    ```
    SPOTIFY_PLAYLIST_ID = '<SPOTIFY PLAYLIST ID>'
    NEW_PLAYLIST_TITLE = '<YOUTUBE MUSIC PLAYLIST NAME>'
    NEW_PLAYLIST_DESCRIPTION = '<YOUTUBE MUSIC PLAYLIST DESCRIPTION>'
    ```
4. Create a file named `config.py` and add in Spotify Client ID & Secret
    ```
    CLIENT_ID = '<SPOTIFY CLIENT ID>'
    CLIENT_SECRET = '<SPOTIFY CLIENT SECRET>'
    ```
5. Run `spotify_to_music.py` to start playing music.
`$ python spotify_to_music.py`

## How to get Spotify Client ID & Secret?
[See the instructions here.](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)