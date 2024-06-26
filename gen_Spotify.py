import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import time
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

# Set up the SSL certificate verification
import ssl
import certifi

ssl._create_default_https_context = ssl._create_unverified_context

# Import musicBrainzngs
import musicbrainzngs
musicbrainzngs.set_useragent("MyApplication", "0.1", "https://myapplication.com")

class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response_code = self.path.split("?code=")[-1]
        self.wfile.write(f"<html><body><h1>Authorization code received.</h1><p>{response_code}</p></body></html>".encode('utf-8'))
        self.server.auth_code = response_code

def run_server():
    server_address = ('', 8088)
    httpd = HTTPServer(server_address, SpotifyAuthHandler)
    httpd.handle_request()
    return httpd.auth_code

# Declare global variables
sp = None
user=None
username = ""
userid=""
country = ""
profile_picture = ""
num_playlists = 0
num_tracks = 0
num_liked_tracks = 0
top_genres = []
favorite_songs = []


def set_up_Spotify():
    load_dotenv()

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    scope = os.getenv("SPOTIFY_SCOPE", "user-library-read user-read-private playlist-read-private user-top-read")

    sp_oauth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scope)

    try:
        token_info = sp_oauth.get_cached_token()
        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            print("Please visit the following URL to authorize the application:")
            print(auth_url)

            response_code = run_server()
            token_info = sp_oauth.get_access_token(response_code)

        access_token = token_info['access_token']
        global sp
        sp = spotipy.Spotify(auth=access_token)
        return sp

    except spotipy.oauth2.SpotifyOauthError as e:
        print(f"Spotify OAuth Error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_user_data():
    global user, username, userid, country, profile_picture, num_playlists, num_tracks, num_liked_tracks, top_genres
    # Retrieve user profile information
    user = sp.current_user()
    username = user["display_name"]
    userid = user["id"]
    country = user["country"]
    profile_picture = user["images"][0]["url"]

    # Retrieve playlist information
    playlists = sp.current_user_playlists(limit=20)
    num_playlists = playlists["total"]

    # Retrieve track information
    tracks = sp.current_user_saved_tracks()
    num_tracks = tracks["total"]

    # Retrieve liked tracks information
    liked_tracks = sp.current_user_saved_tracks(limit=50)
    num_liked_tracks = liked_tracks["total"]

    # Retrieve top genres information
    top_artists = sp.current_user_top_artists(limit=10, time_range="short_term")
    top_genres = [artist["genres"] for artist in top_artists["items"]]


def get_Spotify_favorite_song():
    # La fonction a pris 1398.334469795227 secondes pour s'exécuter, soit 23.3 minutes
    # A peu près une seconde par chanson


    start_time = time.time()
    # Retrieve liked songs information
    favorite_songs = []

    # Number of songs to retrieve per request
    limit = 50

    # Offset for pagination
    offset = 0

    # While there are remaining liked tracks to retrieve
    while len(favorite_songs) < num_liked_tracks:
        # Retrieve the liked tracks with the current offset and limit
        tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)
        for track in tracks["items"]:
            track_info = track["track"]
            track_name = track_info["name"]
            artist_name = track_info["artists"][0]["name"]
            track_id = track_info["id"]

            # Retrieve the moment when the song was added to the playlist
            added_at = track["added_at"]

            # Retrieve the track information for the track
            track = sp.track(track_id)
            track_duration = track["duration_ms"]

            # Retrieve the album information for the track
            album_id = track_info["album"]["id"]
            album = sp.album(album_id)
            album_name = album["name"]
            release_date = album["release_date"]  # Get the release date of the album

            # Use MusicBrainz to get artist information
            artist_info = musicbrainzngs.search_artists(artist=artist_name, limit=1)

            # Check if the artist information is available
            if artist_info.get("artist-list"):
                artist_country = artist_info["artist-list"][0].get("country", "Unknown")
            else:
                artist_country = "Unknown"

            favorite_songs.append(
                (track_name, artist_name, track_id, album_name, track_duration, release_date, artist_country, added_at))
            print(track_name, artist_name, release_date, " ", artist_country, added_at)

        # Increase the offset by the limit for the next request
        offset += limit

    # Save the retrieved information to a JSON file, unstructured
    data = {
        "username": username,
        "country": country,
        "profile_picture": profile_picture,
        "num_playlists": num_playlists,
        "num_tracks": num_tracks,
        "num_liked_tracks": num_liked_tracks,
        "top_genres": top_genres,
        "favorite_songs": favorite_songs
    }
    with open("./JSON_files/RawDataSpotify.json",
              "w") as file:
        json.dump(data, file)

    # Create a list of song objects with line breaks at the beginning
    formatted_songs = [{"name": f"\n{song[0]} - {song[1]} - {song[2]} - {song[3]} - {song[4]} - {song[5]}"} for song in
                       favorite_songs]

    # Save the retrieved information to a JSON file, structured
    data = {
        "username": username,
        "country": country,
        "profile_picture": profile_picture,
        "num_playlists": num_playlists,
        "num_tracks": num_tracks,
        "num_liked_tracks": num_liked_tracks,
        "top_genres": top_genres,
        "favorite_songs": formatted_songs
    }

    with open("./JSON_files/OrderedDataSpotify.json",
              "w") as file:
        json.dump(data, file, indent=4)

    end_time = time.time()
    execution_time = end_time - start_time

    print("La fonction a pris", execution_time, "secondes pour s'exécuter.")


def load_Spotify_favorite_song():
    # Check if the data file exists
    data_file_path = "./JSON_files/RawDataSpotify.json"
    if os.path.exists(data_file_path):
        # Load the data from the JSON file
        with open(data_file_path, "r") as file:
            data = json.load(file)

        # Set the global variables using the loaded data
        global username, country, profile_picture, num_playlists, num_tracks, num_liked_tracks, top_genres, favorite_songs
        username = data["username"]
        country = data["country"]
        profile_picture = data["profile_picture"]
        num_playlists = data["num_playlists"]
        num_tracks = data["num_tracks"]
        num_liked_tracks = data["num_liked_tracks"]
        top_genres = data["top_genres"]
        favorite_songs = data["favorite_songs"]

        print("Données chargées avec succès")

    else:
        # Perform initialization and save the data to the file
        # initialisationSpotify()
        #print("Initialisation effectuée et données sauvegardées dans le fichier.")
        print("there is no data currently available.")


def printInfos_Spotify(FavoriteTest=False):

    # Print gathered information
    print("Username", username)
    print("User ID:", userid)
    print("Country/Region:", country)
    print("Profile Picture URL:", profile_picture)
    print("Number of Playlists Created:", num_playlists)
    print("Total Number of Tracks in Playlists:", num_tracks)
    print("Number of Liked Tracks:", num_liked_tracks)
    print("Top Genres:", top_genres)
    print("Taille de favorite_songs:", len(favorite_songs))
    if FavoriteTest == True:
        print("Favorite Songs:")
        for song in favorite_songs:
            track_name = song[0]
            artist_name = song[1]
            track_id = song[2]
            album_name = song[3]
            track_duration = song[4]
            artist_country = song[5]

            print("- Name:", track_name)
            print("  Artist:", artist_name)
            print("  ID:", track_id)
            print("  Album:", album_name)
            print("  Duration:", track_duration)
            print("  Artist Country:", artist_country)
            print()

        print("Taille de favorite_songs:", len(favorite_songs))

