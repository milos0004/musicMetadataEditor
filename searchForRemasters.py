import os
import re
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

def find_remastered_files(directory_path):
    # Regex patterns for "remaster" and for a year
    remaster_pattern = re.compile(r'remaster(ed)?', re.IGNORECASE)
    year_pattern = re.compile(r'\b(19|20)\d{2}\b')  # Matches years in the 1900s or 2000s

    remastered_files = []
    matching_years = []
    current_year_larger = []

    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Only process MP3 files
            if file_path.lower().endswith('.mp3'):
                try:
                    audio = MP3(file_path, ID3=EasyID3)
                    found_in_fields = []
                    current_year = audio.get("date", ["No current year found"])[0]
                    
                    # Check if "remaster" is found in the file path
                    if remaster_pattern.search(file_path):
                        found_in_fields.append(("path", "No year found", file_path))

                    # Check metadata fields title, album, and comment for "remaster" and "year"
                    for field in ['title', 'album', 'comment']:
                        if field in audio:
                            for val in audio[field]:
                                if remaster_pattern.search(val):
                                    # Find year in the same field, if any
                                    year_match = year_pattern.search(val)
                                    year = year_match.group() if year_match else "No year found"
                                    found_in_fields.append((field, year, val))  # Store the field value too
                                    
                                    # Check if this year matches or is less than the current metadata year
                                    if year != "No year found" and current_year.isdigit():
                                        if year == current_year:
                                            matching_years.append(file_path)
                                        elif int(current_year) > int(year):
                                            current_year_larger.append(file_path)

                    # If "remaster" was found in any field, add to results
                    if found_in_fields:
                        remastered_files.append((file_path, found_in_fields, current_year))
                
                except Exception as e:
                    print(f"Could not read metadata for '{file_path}': {e}")
    
    # Display results
    if remastered_files:
        print("Files containing 'remaster' or 'remastered':")
        for file_path, fields, current_year in remastered_files:
            print(f"File: {file_path}")
            print(f"Current Year: {current_year}")
            for field, year, field_value in fields:
                print(f"Found in: {field}, Year found in field: {year}, Field Value: {field_value}")
            print("-" * 40)
        
        # Summary of files with matching years and where current year is larger
        print(f"\nTotal files with matching years: {len(matching_years)}")
        print("Files with matching years:")
        for file in matching_years:
            print(f" - {file}")

        print(f"\nTotal files where current year is larger than remaster year: {len(current_year_larger)}")
        print("Files where current year is larger than remaster year:")
        for file in current_year_larger:
            print(f" - {file}")
    else:
        print("No files containing 'remaster' or 'remastered' found in the specified directory.")

# Example usage
directory_path = r"E:\Music\Mixtapes"
find_remastered_files(directory_path)

# Pause to keep the window open
input("Press Enter to exit...")
