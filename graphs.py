import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

import random
import math
import pycountry
import os
import json
from datetime import datetime
from dateutil import parser


def draw_top_artists(selectednumber):
    # Compter le nombre de chansons par artiste
    artist_count = {}
    for song in favorite_songs:
        artist_name = song[1]
        if artist_name in artist_count:
            artist_count[artist_name] += 1
        else:
            artist_count[artist_name] = 1

    # Order the list of artists by ascending music number
    sorted_artists = sorted(artist_count.items(), key=lambda x: x[1],reverse=True)
    sorted_artists = sorted_artists[:selectednumber]

    # Extract artist names and song counts for the selected number of artists
    labels = [artist[0] for artist in sorted_artists]
    counts = [artist[1] for artist in sorted_artists]

    # Create a list of random colors for each bar
    colors = [random.choice(['#'+format(random.randint(0, 16777215), '06x') for _ in range(6)]) for _ in range(selectednumber)]

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
    plt.show()