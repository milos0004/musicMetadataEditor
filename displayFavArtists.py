import sqlite3
from collections import defaultdict

import sqlite3
from collections import defaultdict

def count_songs_per_artist(database_path):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        
        # Check if the 'Songs' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Songs';")
        if cursor.fetchone() is not None:
            # Query to retrieve song titles, artists, and ratings
            cursor.execute("SELECT Artist, SongTitle, Rating FROM Songs WHERE Rating >= 70;")
            songs = cursor.fetchall()
            
            # Dictionary to count songs per artist
            artist_counts = defaultdict(int)
            
            # Count songs for each artist
            for artist, title, rating in songs:
                # Split artists by ';' and count each individually
                for individual_artist in artist.split(';'):
                    individual_artist = individual_artist.strip()  # Clean up whitespace
                    artist_counts[individual_artist] += 1
            
            # Sort artists by the number of songs and get the top 100
            top_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:100]
            
            # Display the results
            print("Top 100 Artists with Songs Rated 60 or Higher:")
            for artist, count in top_artists:
                print(f"Artist: {artist}, Song Count: {count}")
        else:
            print("No 'Songs' table found in the database.")
            
    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")
    finally:
        if connection:
            connection.close()



def count_songs_ratio_per_artist(database_path):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        
        # Check if the 'Songs' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Songs';")
        if cursor.fetchone() is not None:
            # Dictionary to count songs rated over 60 and total songs
            over_60_counts = defaultdict(int)
            total_counts = defaultdict(int)
            
            # Query to count songs rated over 60
            cursor.execute("SELECT Artist FROM Songs WHERE Rating >= 70;")
            songs_over_60 = cursor.fetchall()
            for row in songs_over_60:
                artists = row[0].split(';')  # Split artists by ';'
                for artist in artists:
                    artist = artist.strip()  # Remove any leading/trailing whitespace
                    over_60_counts[artist] += 1
            
            # Query to count all songs per artist
            cursor.execute("SELECT Artist FROM Songs;")
            all_songs = cursor.fetchall()
            for row in all_songs:
                artists = row[0].split(';')  # Split artists by ';'
                for artist in artists:
                    artist = artist.strip()  # Remove any leading/trailing whitespace
                    total_counts[artist] += 1
            
            # Calculate ratios and prepare for sorting
            ratios = {}
            for artist in total_counts:
                if total_counts[artist] > 5:  # Only consider artists with more than 5 songs
                    if total_counts[artist] > 0:  # Avoid division by zero
                        ratio = over_60_counts[artist] / total_counts[artist]
                        ratios[artist] = ratio
            
            # Sort artists by ratio and get the top 100
            top_artists = sorted(ratios.items(), key=lambda x: x[1], reverse=True)[:50]
            
            # Display the results
            print("Top 100 Artists by Ratio of Songs Rated Over 60 to Total Songs (only artists with more than 5 songs):")
            for artist, ratio in top_artists:
                print(f"Artist: {artist}, Ratio: {ratio:.2f}")
        else:
            print("No 'Songs' table found in the database.")
            
    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")
    finally:
        if connection:
            connection.close()

# Path to the MediaMonkey database
database_path = r"E:\Mediamonkey 5\Portable\MM5.DB"

# Run the function to count songs ratio per artist
count_songs_ratio_per_artist(database_path)
count_songs_per_artist(database_path)