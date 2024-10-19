import os
from mutagen.easyid3 import EasyID3

# Directory to scan for music files
music_directory = r"E:\Music Not Added Yet\Deemix"

# List to store artists with "&" or ","
artists_with_special_chars = []

# Iterate over all MP3 files in the directory and subdirectories
for root, dirs, files in os.walk(music_directory):
    for filename in files:
        if filename.endswith(".mp3"):
            filepath = os.path.join(root, filename)
            
            try:
                # Load the file's ID3 tags
                audio = EasyID3(filepath)
                
                # Get the artist field, default to "Unknown Artist" if not available
                artist = audio.get("artist", ["Unknown Artist"])[0]
                
                # Check if the artist contains "&" or ","
                if "&" in artist or "," in artist:
                    # Add to the list if it contains the special characters
                    artists_with_special_chars.append(artist)
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Remove duplicates from the list by converting to a set, then back to a list
artists_with_special_chars = list(set(artists_with_special_chars))

# Output the list of artists with "&" or ","
print("Artists with '&' or ',' in their name:")
for artist in artists_with_special_chars:
    print(artist)
