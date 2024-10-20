from mutagen.easyid3 import EasyID3
import os
import re
excluded_artists = ['Simon & Garfunkel', 'Hall & Oates', 'Crosby, Stills & Nash', 'Crosby, Stills, Nash & Young', 'Earth, Wind & Fire', 'Emerson, Lake & Palmer', 'Ike & Tina Turner', 'Huey, Dewey & Louie', 'Peter, Paul & Mary', 'Chad & Jeremy', 'Ashford & Simpson', 'Derek & The Dominos', 'Peaches & Herb', 'Brooks & Dunn', 'She & Him', 'Big Boi & Dre', 'Sonny & Cher', 'The Captain & Tennille', 'The Mamas & the Papas', 'Gladys Knight & the Pips', 'Yoko & the Plastic Ono Band', 'Marilyn & Billy', 'David Crosby & Graham Nash', 'Loggins & Messina', 'Sam & Dave', 'David & David', 'Macklemore & Ryan Lewis', 'Richard & Linda Thompson', 'Captain Beefheart & His Magic Band', 'James & Bobby Purify', 'Peter, Bjorn & John', 'Pat Travers Band & Carmine Appice', 'Adam & The Ants', 'England Dan & John Ford Coley', 'George & Tammy', 'Boots Randolph & His Combo', 'Louis Prima & Keely Smith', 'Sly & Robbie', 'Sonny Terry & Brownie McGhee', "Booker T. & the MG's", 'Meat Loaf & Stoney', 'Nino Tempo & April Stevens', 'Ruth Brown & Clyde McPhatter', 'The Clark Sisters & Mattie Moss Clark', 'Hank Ballard & the Midnighters', 'El Chicano & Poncho Sanchez', 'Bob Seger & the Silver Bullet Band', 'Adam & The Ants', 'Duke Ellington & His Orchestra', 'Tony Bennett & Lady Gaga', 'Charles Brown & Amos Milburn', 'George Clinton & Parliament-Funkadelic', 'Ike & Tina Turner', 'Dr. Hook & The Medicine Show', 'Lester Flatt & Earl Scruggs', 'Kool & The Gang', 'Fred Astaire & Ginger Rogers', 'Les Paul & Mary Ford', 'Louis Armstrong & His All-Stars', 'Peter & Gordon', 'Mickey & Sylvia', 'Sam & Dave', 'The Mamas & the Papas', 'Meat Loaf & Ellen Foley', 'Xscape & Jermaine Dupri', 'Simon & Garfunkel', 'Crosby, Stills & Nash', 'Crosby, Stills, Nash & Young', 'Earth, Wind & Fire', 'Ashford & Simpson', 'Lionel Hampton & His Orchestra', 'Shirley & Lee', 'LaVern Baker & Jimmy Ricks', 'George Jones & Tammy Wynette', 'Ike & Tina Turner', 'Brooks & Dunn', 'Elvis Costello & the Attractions', 'Martha & The Vandellas', 'Ike & Tina Turner', 'Prince & The Revolution', 'George Michael & Elton John', 'Prince & The New Power Generation', "Booker T. & the MG's", 'Rufus & Chaka Khan', 'Sonny & Cher', "Sergio Mendes & Brasil '66", 'Ziggy Marley & The Melody Makers', 'Robert Plant & Alison Krauss', 'Captain Beefheart & His Magic Band', 'Peaches & Herb', 'Lionel Richie & Diana Ross', 'Dr. Hook & The Medicine Show']

# Directory containing your music files
music_directory = r"E:\Music Not Added Yet"

# Regular expression to match "(feat. Artist)" in song titles, case-insensitive
pattern = re.compile(r"\s*\(f(?:ea)?t(?:\.|uring)? ([^)]+)\)", re.IGNORECASE)

# Regular expression to match "feat." or "ft." without brackets
pattern2 = re.compile(
    r"(?<!\S)"  # Ensures no non-whitespace before "feat", meaning it requires a space or start of string
    r"(?:f(?:ea)?t(?:\.|uring)?)"  # Matches "feat", "ft.", "ft", "featuring", etc.
    r"(?:[\.\s]+)"  # Ensures "ft" is followed by either a period or a space
    r"([^\s]+(?:[\s,;&]+[^\s]+)*)",  # Captures the artist name after "feat." and accounts for multiple names
    re.IGNORECASE
)

# List of artists to exclude from being added to the artist field

# Initialize a counter for the matching files
match_count = 0

# Helper function to clean and add featured artists to the artist field, keeping the original artist first
def add_featured_artists_to_artist_field(original_artist, featured_artists):
    current_artist_set = {a.strip() for a in original_artist.split(";")}
    featured_artist_set = {artist for artist in featured_artists if artist not in excluded_artists}
    
    # Ensure the original artist is first, then append new featured artists that are not already in the artist field
    updated_artists = [original_artist] + [artist for artist in featured_artist_set if artist not in current_artist_set]
    
    return "; ".join(updated_artists)  # Return the updated artist list with original artist first

# Helper function to split multiple artists correctly by delimiters like ',', '&', 'and'
def split_artists(artist_string):
    # Split by common delimiters like ',', 'and', and '&'
    return re.split(r'\s*,\s*|\s*&\s*|\s+and\s+', artist_string.strip())

# Iterate over all MP3 files in the directory and subdirectories
for root, dirs, files in os.walk(music_directory):
    for filename in files:
        if filename.endswith(".mp3"):
            filepath = os.path.join(root, filename)
            
            try:
                # Load the file's ID3 tags
                audio = EasyID3(filepath)
                
                # Get the current title and artist
                title = audio.get("title", [None])[0]
                artist = audio.get("artist", ["Unknown Artist"])[0]  # Default to "Unknown Artist" if no artist is found
                
                if title:
                    # Find all featured artists from the title using both patterns
                    featured_artists_in_parentheses = pattern.findall(title)
                    featured_artists_without_parentheses = pattern2.findall(title)

                    # Combine all featured artists found, split multiple artists by ',', '&', 'and'
                    all_featured_artists = []
                    if featured_artists_in_parentheses:
                        all_featured_artists.extend(split_artists(featured_artists_in_parentheses[0]))
                    if featured_artists_without_parentheses:
                        all_featured_artists.extend(split_artists(featured_artists_without_parentheses[0]))

                    if all_featured_artists:
                        # Increment the counter
                        match_count += 1

                        # Remove only the "(feat. Artist)" portion from the title, keeping any other parentheses content
                        new_title = pattern.sub("", title)  # Removes "(feat. Artist)"
                        new_title = pattern2.sub("", new_title)  # Removes "feat. Artist" without parentheses
                        new_title = new_title.strip()  # Trim any trailing/leading whitespace

                        # Keep any remaining parentheses content (i.e., not related to featured artists)
                        # by only removing the part of the parentheses that matched the feature pattern
                        if "(" in title and ")" in title:
                            remaining_parentheses_content = title[title.find("("):title.rfind(")")+1]
                            if not pattern.search(remaining_parentheses_content):  # If it's not a "feat." pattern
                                new_title += f" {remaining_parentheses_content}"

                        # Add featured artists to the artist field, ensuring the original artist is listed first
                        updated_artist_field = add_featured_artists_to_artist_field(artist, all_featured_artists)

                        # Update the title and artist in the ID3 tags
                        audio["title"] = new_title.strip()
                        audio["artist"] = updated_artist_field
                        audio.save()

                        # Print the original title, the new title, and the artist
                        print(f"{match_count}. Original: {title} - {artist}")
                        print(f"    Updated: {new_title} - {updated_artist_field}\n")
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Print the total number of matching songs found
print(f"\nTotal matching songs found: {match_count}")
