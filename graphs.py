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

        # Set the font family to Arial Unicode
        plt.rcParams['font.family'] = 'Arial Unicode MS'

        # Create a bar chart with different colors for each bar and add a grid
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

    def draw_artist_histogram(self):
        # Compter le nombre de chansons par artiste
        artist_count = {}
        for song in self.spotify_data.user_data['favorite_songs']:
            artist_name = song[1]
            if artist_name in artist_count:
                artist_count[artist_name] += 1
            else:
                artist_count[artist_name] = 1

        # Compter le nombre d'artistes par nombre de chansons
        count_artist = {'1': 0, '2': 0, '3': 0,
                        '4': 0, '5': 0, '6': 0,
                        '7': 0, '8': 0, '9': 0, '10+': 0}
        for count in artist_count.values():
            if count == 1:
                count_artist['1'] += 1
            if count == 2:
                count_artist['2'] += 1
            if count == 3:
                count_artist['3'] += 1
            if count == 4:
                count_artist['4'] += 1
            if count == 5:
                count_artist['5'] += 1
            if count == 6:
                count_artist['6'] += 1
            if count == 7:
                count_artist['7'] += 1
            if count == 8:
                count_artist['8'] += 1
            if count == 9:
                count_artist['9'] += 1
            if count >= 10:
                count_artist['10+'] += 1

        # Préparer les étiquettes et les hauteurs des barres
        labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10+']
        counts = [count_artist['1'], count_artist['2'], count_artist['3'],
                  count_artist['4'], count_artist['5'], count_artist['6'],
                  count_artist['7'], count_artist['8'], count_artist['9'],
                  count_artist['10+']]

        # Créer un histogramme
        plt.bar(labels, counts)
        plt.xlabel('Number of Songs')
        plt.ylabel('Number of Artists')
        plt.title('Number of Artists by Song Count')

        # Afficher l'histogramme
        plt.show()
