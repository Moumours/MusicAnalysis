import matplotlib.pyplot as plt
import random
import math

import pycountry
from collections import defaultdict
from datetime import datetime

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

    def draw_duration_histogram(self):
        # Compter le nombre de chansons par durée
        duration_count = {'<2m00': 0, '2m00-2m15': 0,'2m15-2m30': 0,
                          '2m30-2m45': 0, '2m45-3m00': 0, '3m00-3m15': 0,
                           '3m15-3m30': 0, '3m30-3m45': 0,'3m45-4m00': 0,
                           '4m00-4m15': 0, '4m15-4m30': 0,
                          '4m30-4m45': 0, '4m45-5m00': 0, '>5m00': 0}

        for song in self.spotify_data.user_data['favorite_songs']:
            duration = song[4] / 1000

            if duration < 120:
                duration_count['<2m00'] += 1
            elif 120 <= duration < 135:
                duration_count['2m00-2m15'] += 1
            elif 135 <= duration < 150:
                duration_count['2m15-2m30'] += 1
            elif 150 <= duration < 165:
                duration_count['2m30-2m45'] += 1
            elif 165 <= duration < 180:
                duration_count['2m45-3m00'] += 1
            elif 180 <= duration < 195:
                duration_count['3m00-3m15'] += 1
            elif 195 <= duration < 210:
                duration_count['3m15-3m30'] += 1
            elif 210 <= duration < 225:
                duration_count['3m30-3m45'] += 1
            elif 225 <= duration < 240:
                duration_count['3m45-4m00'] += 1
            elif 240 <= duration < 255:
                duration_count['4m00-4m15'] += 1
            elif 255 <= duration < 270:
                duration_count['4m15-4m30'] += 1
            elif 270 <= duration < 285:
                duration_count['4m30-4m45'] += 1
            elif 285 <= duration < 300:
                duration_count['4m45-5m00'] += 1
            else:
                duration_count['>5m00'] += 1

        # Préparer les étiquettes et les hauteurs des barres
        labels = ['<2m00', '2m00-2m15', '2m15-2m30', '2m30-2m45', '2m45-3m00', '3m00-3m15', '3m15-3m30',
                  '3m30-3m45', '3m45-4m00', '4m00-4m15', '4m15-4m30', '4m30-4m45', '4m45-5m00', '>5m00']
        counts = [duration_count[label] for label in labels]

        # Créer un histogramme
        plt.bar(labels, counts)
        plt.xlabel('Duration')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Number of Songs')
        plt.title('Number of Songs by Duration')

        # Afficher l'histogramme
        plt.show()


    def draw_countries_by_songs(self):
        country_scores = {}

        for song in self.spotify_data.user_data['favorite_songs']:
            artist_country = song[6]
            if artist_country in country_scores:
                country_scores[artist_country] += 1
            else:
                country_scores[artist_country] = 1

        # Sort country scores in descending order (excluding 'Unknown')
        sorted_scores = sorted(country_scores.items(), key=lambda x: x[1], reverse=True)
        sorted_scores = [score for score in sorted_scores if score[0] != 'Unknown']
        sorted_scores.append(('Unknown', country_scores.get('Unknown', 0)))

        labels = [score[0] for score in sorted_scores]
        values = [score[1] for score in sorted_scores]

        # Calculate the total number of songs
        total_songs = sum(values)

        # Create a list to store the legend labels
        legend_labels = []

        # Create a list to store the pie labels
        pie_labels = []

        # Iterate over the sorted scores and check the percentage for each country
        for label, value in zip(labels, values):
            percentage = (value / total_songs) * 100

            # Check if the country name is void
            country = pycountry.countries.get(alpha_2=label)
            if country is not None:
                legend_label = f"{label} ({country.name}) - Songs: {value} - {percentage:.1f}%"
            else:
                legend_label = f"{label} - Songs: {value} - {percentage:.1f}%"

            legend_labels.append(legend_label)

            # Check if the percentage is below 2
            if percentage >= 2:
                pie_labels.append(f"{label}")
            else:
                pie_labels.append('')

        plt.figure(figsize=(8, 6))
        patches, _ = plt.pie(values, labels=pie_labels, startangle=90)
        plt.title("Origins of Favorite Artists (by total number of songs)")
        plt.legend(patches, legend_labels, loc='center right', bbox_to_anchor=(0.01, 0.5))
        plt.tight_layout()
        plt.show()

    def draw_countries_by_unique_artists(self):
        country_scores = {}
        distinct_artist_list = []

        for song in self.spotify_data.user_data['favorite_songs']:
            current_artist=song[1]
            if current_artist not in distinct_artist_list:
                distinct_artist_list.append(current_artist)
                artist_country = song[6]
                if artist_country in country_scores:
                    country_scores[artist_country] += 1
                else:
                    country_scores[artist_country] = 1

        # Sort country scores in descending order (excluding 'Unknown')
        sorted_scores = sorted(country_scores.items(), key=lambda x: x[1], reverse=True)
        sorted_scores = [score for score in sorted_scores if score[0] != 'Unknown']
        sorted_scores.append(('Unknown', country_scores.get('Unknown', 0)))

        labels = [score[0] for score in sorted_scores]
        values = [score[1] for score in sorted_scores]

        # Calculate the total number of artists
        total_artists = len(self.spotify_data.user_data['favorite_songs'])

        # Create a list to store the legend labels
        legend_labels = []

        # Create a list to store the pie labels
        pie_labels = []

        # Iterate over the sorted scores and check the percentage for each country
        for label, value in zip(labels, values):
            percentage = (value / len(distinct_artist_list)) * 100

            # Check if the percentage is below 2
            country = pycountry.countries.get(alpha_2=label)
            if country is not None:
                legend_label = f"{label} ({country.name}) - Artists: {value} - {percentage:.1f}%"
            else:
                legend_label = f"{label} - Artists: {value} - {percentage:.1f}%"

            legend_labels.append(legend_label)

            # Check if the percentage is below 2
            if percentage >= 2:
                pie_labels.append(f"{label}")
            else:
                pie_labels.append('')

        plt.figure(figsize=(8, 6))
        patches, _ = plt.pie(values, labels=pie_labels, startangle=90)
        plt.title("Origins of Favorite Artists (by total number of artists)")
        plt.legend(patches, legend_labels, loc='center right', bbox_to_anchor=(0.01, 0.5))
        plt.tight_layout()
        plt.show()


    def display_artists_by_country(self, country):
        artist_counts = {}

        # Convert the input country name or abbreviation to uppercase
        country = country.upper()

        # Iterate over favorite songs to count the number of songs for each artist
        for song in self.spotify_data.user_data['favorite_songs']:
            artist_country = song[6]
            # Check if the artist's country matches the input country
            if artist_country.upper() == country:
                artist = song[1]
                # Increment the count for the artist
                artist_counts[artist] = artist_counts.get(artist, 0) + 1

        # Sort artists by descending number of songs
        sorted_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)

        # Display the list of artists from the specified country with song counts
        if sorted_artists:
            print(f"Artists from {country}:")
            for artist, count in sorted_artists:
                # Check if the count is 1 and modify the word "song" accordingly
                if count == 1:
                    song_word = "song"
                else:
                    song_word = "songs"
                print(f"{artist} - {count} {song_word}")
        else:
            print(f"No artists found from {country}.")

    def draw_artists_pie_chart_by_country(self, country_abbr):
        country_artists = {}

        # Count the number of songs for each artist from the specified country
        for song in self.spotify_data.user_data['favorite_songs']:
            artist_country = song[6]
            if artist_country == country_abbr:
                artist_name = song[1]
                country_artists[artist_name] = country_artists.get(artist_name, 0) + 1

        # Sort artists by descending number of songs
        sorted_artists = sorted(country_artists.items(), key=lambda x: x[1], reverse=True)

        # Prepare data for the pie chart
        labels = []
        counts = []
        pie_labels = []

        # Create separate lists for labels and counts
        for artist, count in sorted_artists:
            labels.append(artist)
            counts.append(count)
            # Check if the percentage is below 2
            if count >= 2:
                pie_labels.append(f"{artist}")
            else:
                pie_labels.append('')

        # Create a legend with artist names and song counts
        legend_labels = [f"{artist} - {count}" for artist, count in sorted_artists]

        # Draw the pie chart with the artist distribution by country

        plt.figure(figsize=(8, 6))
        patches, _ = plt.pie(counts, labels=pie_labels, startangle=90)
        plt.title(f"Artists Distribution from {country_abbr}")
        plt.legend(patches, legend_labels, loc='center right', bbox_to_anchor=(0.01, 0.2))
        plt.tight_layout()
        plt.show()

