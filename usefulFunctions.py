import re

def find_phrases_in_parentheses(title, phrases):
    # Join the phrases into a regex pattern, escaping any special characters
    pattern = re.compile(r"\((" + "|".join([re.escape(phrase) for phrase in phrases]) + r")\)", re.IGNORECASE)
    
    # Find all matches in the title
    matches = pattern.findall(title)
    
    return matches  # Return the list of matched phrases


# Example usage:
phrases_to_check = ['feat.', 'Remix', 'Live', 'Acoustic', 'Demo']

title = "Song Title (feat. Artist) (Live) (Remix)"
found_phrases = find_phrases_in_parentheses(title, phrases_to_check)

if found_phrases:
    print(f"Phrases found in '{title}': {found_phrases}")
else:
    print(f"No target phrases found in '{title}'.")
