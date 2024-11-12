import sqlite3
from collections import defaultdict

def count_songs_per_artist(database_path):
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        
        # Check if the 'Songs' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Songs';")
        if cursor.fetchone() is not None:
            cursor.execute("SELECT Artist, SongTitle, Rating FROM Songs WHERE Rating >= 70;")
            songs = cursor.fetchall()
            
            artist_counts = defaultdict(int)
            for artist, title, rating in songs:
                for individual_artist in artist.split(';'):
                    individual_artist = individual_artist.strip()
                    artist_counts[individual_artist] += 1
            
            top_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:100]
            print("Top 100 Artists with Songs Rated 70 or Higher:")
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
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Songs';")
        if cursor.fetchone() is not None:
            over_70_counts = defaultdict(int)
            total_counts = defaultdict(int)
            
            cursor.execute("SELECT Artist FROM Songs WHERE Rating >= 70;")
            songs_over_70 = cursor.fetchall()
            for row in songs_over_70:
                artists = row[0].split(';')
                for artist in artists:
                    artist = artist.strip()
                    over_70_counts[artist] += 1
            
            cursor.execute("SELECT Artist FROM Songs;")
            all_songs = cursor.fetchall()
            for row in all_songs:
                artists = row[0].split(';')
                for artist in artists:
                    artist = artist.strip()
                    total_counts[artist] += 1
            
            ratios = {}
            for artist in total_counts:
                if total_counts[artist] > 5:
                    if total_counts[artist] > 0:
                        ratio = over_70_counts[artist] / total_counts[artist]
                        ratios[artist] = ratio
            
            top_artists = sorted(ratios.items(), key=lambda x: x[1], reverse=True)[:50]
            print("Top 50 Artists by Ratio of Songs Rated Over 70 to Total Songs (only artists with more than 5 songs):")
            for artist, ratio in top_artists:
                print(f"Artist: {artist}, Ratio: {ratio:.2f}")
        else:
            print("No 'Songs' table found in the database.")
            
    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")
    finally:
        if connection:
            connection.close()


def display_top_artists_by_avg_rating(database_path):
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Songs';")
        if cursor.fetchone() is not None:
            artist_ratings = defaultdict(list)
            
            cursor.execute("SELECT Artist, Rating FROM Songs WHERE Rating != -1;")
            rated_songs = cursor.fetchall()
            
            for row in rated_songs:
                artists = row[0].split(';')
                rating = row[1]
                for artist in artists:
                    artist = artist.strip()
                    artist_ratings[artist].append(rating)
            
            avg_ratings = {}
            for artist, ratings in artist_ratings.items():
                if len(ratings) >= 5:  # Only consider artists with at least 5 rated songs
                    avg_rating = sum(ratings) / len(ratings)
                    avg_ratings[artist] = avg_rating
            
            top_artists = sorted(avg_ratings.items(), key=lambda x: x[1], reverse=True)[:100]
            print("Top 100 Artists by Average Rating (only artists with at least 5 rated songs, ignoring songs with a rating of -1):")
            for artist, avg_rating in top_artists:
                print(f"Artist: {artist}, Average Rating: {avg_rating / 20:.2f} stars")
        else:
            print("No 'Songs' table found in the database.")
            
    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")
    finally:
        if connection:
            connection.close()



def get_song_rating(database_path, title, artist):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        
        # Query to find the song with the specified title and artist
        cursor.execute("""
            SELECT Rating FROM Songs
            WHERE SongTitle = ? AND Artist LIKE ?;
        """, (title, f"%{artist}%"))
        
        # Fetch the rating
        rating = cursor.fetchone()
        
        if rating:
            print(f"The rating for the song '{title}' by {artist} is: {rating[0]}")
        else:
            print(f"No song titled '{title}' by {artist} was found in the database.")
            
    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")
    finally:
        if connection:
            connection.close()

# Path to the MediaMonkey database
database_path = r"E:\Mediamonkey 5\Portable\MM5.DB"

# Run the function to get the rating of the specified song



# Path to the MediaMonkey database
database_path = r"E:\Mediamonkey 5\Portable\MM5.DB"

# Run the functions
count_songs_ratio_per_artist(database_path)
count_songs_per_artist(database_path)
display_top_artists_by_avg_rating(database_path)
get_song_rating(database_path, "Finesse", "Drake")