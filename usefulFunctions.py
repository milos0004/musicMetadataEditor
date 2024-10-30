import re
from excludedArtists import excluded_artists

def find_phrases_in_field(metadata, field_name, phrases_dict):
    """
    Checks for specific phrases in the chosen metadata field (title, artist, album, etc.).
    
    :param metadata: Dictionary containing the metadata fields (e.g., 'title', 'artist', 'album').
    :param field_name: The name of the field to search in (e.g., 'title', 'artist', 'album').
    :param phrases_dict: A dictionary where keys are the field names and values are lists of phrases to check.
    :return: A list of matched phrases in the specified field, or an empty list if none are found.
    """
    
    # Get the value for the chosen field
    field_value = metadata.get(field_name, "")
    
    # If the field has no value or it's not in the metadata, return an empty list
    if not field_value:
        return []

    # Get the phrases for the chosen field
    phrases = phrases_dict.get(field_name, [])

    # Build a regex pattern for the phrases, enclosed in parentheses
    pattern = re.compile(r"\((" + "|".join([re.escape(phrase) for phrase in phrases]) + r")\)", re.IGNORECASE)
    
    # Find all matches in the chosen field
    matches = pattern.findall(field_value)
    
    return matches  # Return the list of matched phrases


# Example usage:
metadata = {
    'title': "Song Title (feat. Artist) (Live) (Remix)",
    'artist': "Main Artist (feat. Someone)",
    'album': "Best Album (Deluxe Edition)"
}

# Phrases to check for each field
phrases_to_check = {
    'title': ['feat.', 'Remix', 'Live', 'Acoustic', 'Demo'],
    'artist': ['feat.', 'and', '&'],
    'album': ['Deluxe Edition', 'Remastered', 'Bonus Track', 'Explicit']
}

# Choose which field to check (title, artist, album)
field_to_check = 'title'  # Can be 'title', 'artist', or 'album'

# Find phrases in the chosen field
found_phrases = find_phrases_in_field(metadata, field_to_check, phrases_to_check)

# Output the result
if found_phrases:
    print(f"Phrases found in {field_to_check}: {found_phrases}")
else:
    print(f"No target phrases found in {field_to_check}.")
