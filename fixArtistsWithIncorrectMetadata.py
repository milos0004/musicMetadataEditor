import os
from mutagen.easyid3 import EasyID3

# Directory to scan for music files
music_directory = r"E:\Music not added yet\Mixtapes"

# List to store artists with "&" or ","
artists_with_special_chars = []

# List to store all encountered artists
all_artists = []

# List to store songs where artist fields are modified
modified_songs = []

# List to store artists where some but not all parts match
some_match_artists = []

# List of excluded artists (these won't be modified or listed)
excluded_artists = ['Simon & Garfunkel', 'Hall & Oates', 'Crosby, Stills & Nash', 'Crosby, Stills, Nash & Young', 'Earth, Wind & Fire', 'Emerson, Lake & Palmer', 'Ike & Tina Turner', 'Huey, Dewey & Louie', 'Peter, Paul & Mary', 'Chad & Jeremy', 'Ashford & Simpson', 'Derek & The Dominos', 'Peaches & Herb', 'Brooks & Dunn', 'She & Him', 'Big Boi & Dre', 'Sonny & Cher', 'The Captain & Tennille', 'The Mamas & the Papas', 'Gladys Knight & the Pips', 'Yoko & the Plastic Ono Band', 'Marilyn & Billy', 'David Crosby & Graham Nash', 'Loggins & Messina', 'Sam & Dave', 'David & David', 'Macklemore & Ryan Lewis', 'Richard & Linda Thompson', 'Captain Beefheart & His Magic Band', 'James & Bobby Purify', 'Peter, Bjorn & John', 'Pat Travers Band & Carmine Appice', 'Adam & The Ants', 'England Dan & John Ford Coley', 'George & Tammy', 'Boots Randolph & His Combo', 'Louis Prima & Keely Smith', 'Sly & Robbie', 'Sonny Terry & Brownie McGhee', "Booker T. & the MG's", 'Meat Loaf & Stoney', 'Nino Tempo & April Stevens', 'Ruth Brown & Clyde McPhatter', 'The Clark Sisters & Mattie Moss Clark', 'Hank Ballard & the Midnighters', 'El Chicano & Poncho Sanchez', 'Bob Seger & the Silver Bullet Band', 'Adam & The Ants', 'Duke Ellington & His Orchestra', 'Tony Bennett & Lady Gaga', 'Charles Brown & Amos Milburn', 'George Clinton & Parliament-Funkadelic', 'Ike & Tina Turner', 'Dr. Hook & The Medicine Show', 'Lester Flatt & Earl Scruggs', 'Kool & The Gang', 'Fred Astaire & Ginger Rogers', 'Les Paul & Mary Ford', 'Louis Armstrong & His All-Stars', 'Peter & Gordon', 'Mickey & Sylvia', 'Sam & Dave', 'The Mamas & the Papas', 'Meat Loaf & Ellen Foley', 'Xscape & Jermaine Dupri', 'Simon & Garfunkel', 'Crosby, Stills & Nash', 'Crosby, Stills, Nash & Young', 'Earth, Wind & Fire', 'Ashford & Simpson', 'Lionel Hampton & His Orchestra', 'Shirley & Lee', 'LaVern Baker & Jimmy Ricks', 'George Jones & Tammy Wynette', 'Ike & Tina Turner', 'Brooks & Dunn', 'Elvis Costello & the Attractions', 'Martha & The Vandellas', 'Ike & Tina Turner', 'Prince & The Revolution', 'George Michael & Elton John', 'Prince & The New Power Generation', "Booker T. & the MG's", 'Rufus & Chaka Khan', 'Sonny & Cher', "Sergio Mendes & Brasil '66", 'Ziggy Marley & The Melody Makers', 'Robert Plant & Alison Krauss', 'Captain Beefheart & His Magic Band', 'Peaches & Herb', 'Lionel Richie & Diana Ross', 'Dr. Hook & The Medicine Show']

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
                
                # Skip if the artist is in the excluded list
                if artist_field in excluded_artists:
                    continue
                
                # Split artists by ";", then analyze each individual artist
                artists = artist_field.split(";")
                for artist in artists:
                    artist = artist.strip()
                    
                    # Store all artists encountered
                    all_artists.append(artist)
                    
                    # Analyze artist for special characters
                    result = analyze_artist(artist)
                    if result and result not in excluded_artists:  # Skip excluded artists
                        artists_with_special_chars.append(result)
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Remove duplicates from the lists
artists_with_special_chars = list(set(artists_with_special_chars))
all_artists = list(set(all_artists))

# Output the list of artists with "&" or "," in their name, excluding excluded artists
print("Artists with '&' or ',' in their name (excluding excluded artists):")
for artist in sorted(artists_with_special_chars):
    print(f'"{artist}",')

# Split artists_with_special_chars and check if all or some parts match in all_artists
matches_with_splits = []
partial_matches = []

for special_artist in artists_with_special_chars:
    # Split by "&" or ","
    splits = [part.strip() for part in special_artist.replace("&", ",").split(",")]
    
    # Skip excluded artists
    if special_artist in excluded_artists:
        continue

    # Check if all split parts are in the all_artists list
    if all(split in all_artists for split in splits):
        matches_with_splits.append(special_artist)
    elif any(split in all_artists for split in splits):
        # If some (but not all) parts match
        partial_matches.append(special_artist)

# Output the artists where all splits have a match in all_artists
print("\nArtists where all parts match any encountered artist (excluding excluded artists):")
for artist in sorted(matches_with_splits):
    print(f'"{artist}",')

# Output the artists where some (but not all) parts match
print("\nArtists where some parts match any encountered artist (but not all) (excluding excluded artists):")
for artist in sorted(partial_matches):
    print(f'"{artist}",')

# Now, find the songs where these artists (with full matches) appear and modify the artist field
for root, dirs, files in os.walk(music_directory):
    for filename in files:
        if filename.endswith(".mp3"):
            filepath = os.path.join(root, filename)
            
            try:
                # Load the file's ID3 tags
                audio = EasyID3(filepath)
                
                # Get the artist field, default to "Unknown Artist" if not available
                artist_field = audio.get("artist", ["Unknown Artist"])[0]
                
                # If the artist field is in excluded_artists, skip modification
                if artist_field in excluded_artists:
                    continue
                
                # If the artist field matches one of the artists in matches_with_splits
                if artist_field in matches_with_splits:
                    # Store the old artist field
                    old_artist_field = artist_field
                    
                    # Replace "," or "&" with ";"
                    new_artist_field = artist_field.replace("&", ";").replace(",", ";")
                    
                    # Update the artist tag
                    audio["artist"] = new_artist_field
                    audio.save()  # Save the changes to the file
                    
                    # Store the song details for output
                    modified_songs.append({
                        "song_name": filename,
                        "old_artist": old_artist_field,
                        "new_artist": new_artist_field
                    })
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Output the modified songs with old and new artist fields
print("\nModified songs:")
for song in modified_songs:
    print(f'Song: "{song["song_name"]}", Old Artist: "{song["old_artist"]}", New Artist: "{song["new_artist"]}"')

# Output the total number of modified songs
print(f"\nTotal number of modified songs: {len(modified_songs)}")
