import requests
import spotipy
import os
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

date = input("Enter a date (YYYY-MM-DD):")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.find_all("h3", id="title-of-a-story",
                                 class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
song_names = [song.getText() for song in song_names_spans]
print(song_names)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        redirect_uri="https://example.com/callback/",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = int(date.split("-")[0])

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", collaborative=False, public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
