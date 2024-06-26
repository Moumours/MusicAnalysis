
from gen_Spotify import *
from graphs import *


if __name__ == "__main__":
    sp = set_up_Spotify()

    if sp:
        load_Spotify_favorite_song()

    else:
        print("Failed to set up Spotify API client.")


