import os
from mutagen.easyid3 import EasyID3

# Directory to scan for music files
music_directory = r"E:\Music\Mixtapes"

# List to store artists with "&" or ","
artists_with_special_chars = []

# List to store all encountered artists
all_artists = []

# Helper function to analyze individual artists
def analyze_artist(artist):
    # Check if the artist contains "&" or ","
    if "&" in artist or "," in artist:
        return artist.strip()
    return None

# Iterate over all MP3 files in the directory and subdirectories
for root, dirs, files in os.walk(music_directory):
    for filename in files:
        if filename.endswith(".mp3"):
            filepath = os.path.join(root, filename)
            
            try:
                # Load the file's ID3 tags
                audio = EasyID3(filepath)
                
                # Get the artist field, default to "Unknown Artist" if not available
                artist_field = audio.get("artist", ["Unknown Artist"])[0]
                
                # Split artists by ";", then analyze each individual artist
                artists = artist_field.split(";")
                for artist in artists:
                    # Store all artists encountered
                    all_artists.append(artist.strip())
                    
                    # Analyze artist for special characters
                    result = analyze_artist(artist)
                    if result:
                        artists_with_special_chars.append(result)
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Remove duplicates from the lists
artists_with_special_chars = list(set(artists_with_special_chars))
all_artists = list(set(all_artists))

# Output the list of artists with "&" or "," in their name
print("Artists with '&' or ',' in their name:")
for artist in sorted(artists_with_special_chars):
    print(f'"{artist}",')

# Split artists_with_special_chars and check if each split has a match in all_artists
matches_with_splits = []

for special_artist in artists_with_special_chars:
    # Split by "&" or ","
    splits = [part.strip() for part in special_artist.replace("&", ",").split(",")]
    
    # Check if all split parts are in the all_artists list
    if all(split in all_artists for split in splits):
        matches_with_splits.append(special_artist)

# Output the artists where all splits have a match in all_artists
print("\nArtists where all parts match any encountered artist:")
for artist in sorted(matches_with_splits):
    print(f'"{artist}",')

# Print the total number of such artists
print(f"\nTotal number of artists where all parts match: {len(matches_with_splits)}")
