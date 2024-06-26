import matplotlib.pyplot as plt
import random
import math

class Graph:
    def __init__(self, spotify_data):
        self.spotify_data = spotify_data

    def print_data(self, song_names=False):
        print(f"Username: {self.spotify_data.user_data.get('username', 'N/A')}")
        print(f"User ID: {self.spotify_data.user_data.get('userid', 'N/A')}")
        print(f"Country/Region: {self.spotify_data.user_data.get('country', 'N/A')}")
        print(f"Profile Picture URL: {self.spotify_data.user_data.get('profile_picture', 'N/A')}")
        print(f"Number of Playlists Created: {self.spotify_data.user_data.get('num_playlists', 0)}")
        print(f"Total Number of Tracks in Playlists: {self.spotify_data.user_data.get('num_tracks', 0)}")
        print(f"Number of Liked Tracks: {self.spotify_data.user_data.get('num_liked_tracks', 0)}")
        print(f"Top Genres: {self.spotify_data.user_data.get('top_genres', [])}")
        print(f"Number of Favorite Songs: {len(self.spotify_data.user_data.get('favorite_songs', []))}")
        if song_names:
            for song in self.spotify_data.user_data.get('favorite_songs', []):
                print(f"- {song[0]} by {song[1]}, added on {song[7]}")

    def draw_top_artists(self, selectednumber):
        # Count the number of songs per artist
        artist_count = {}
        for song in self.spotify_data.user_data['favorite_songs']:
            artist_name = song[1]
            if artist_name in artist_count:
                artist_count[artist_name] += 1
            else:
                artist_count[artist_name] = 1

        # Order the list of artists by descending song count
        sorted_artists = sorted(artist_count.items(), key=lambda x: x[1], reverse=True)
        sorted_artists = sorted_artists[:selectednumber]

        # Extract artist names and song counts for the selected number of artists
        labels = [artist[0] for artist in sorted_artists]
        counts = [artist[1] for artist in sorted_artists]

        # Create a list of random colors for each bar
        colors = [random.choice(['#' + format(random.randint(0, 16777215), '06x') for _ in range(6)]) for _ in
                  range(selectednumber)]

        # Create a bar chart with different colors for each bar
        plt.bar(labels, counts, color=colors)
        plt.xlabel('Artist')
        plt.ylabel('Number of Songs')
        plt.title(f'Top {selectednumber} Artists by Song Count')

        # Set the y-axis tick locations as integer values
        plt.yticks(range(math.ceil(max(counts)) + 1))

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Display the histogram
        plt.tight_layout()
        plt.show()
