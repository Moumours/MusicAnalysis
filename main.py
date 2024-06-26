from gen_Spotify import SpotifyData
from graphs import Graph

if __name__ == "__main__":
    spotify_data = SpotifyData()

    if spotify_data.sp:
        spotify_data.get_user_data()
        spotify_data.load_spotify_favorite_songs()

        graph = Graph(spotify_data)
        # graph.print_data()
        graph.draw_top_artists(30)
        # graph.draw_artist_histogram()
    else:
        print("Failed to set up Spotify API client.")


