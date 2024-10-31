import unittest

# Import excluded_artists from the module where it's defined
from excludedArtists import excluded_artists

class TestExcludedArtistsImport(unittest.TestCase):
    
    def test_excluded_artists_import(self):
        # Check if excluded_artists is imported and is a list
        self.assertIsNotNone(excluded_artists, "excluded_artists should not be None.")
        self.assertIsInstance(excluded_artists, list, "excluded_artists should be a list.")
        
        # Optionally, you can check if the list is not empty if that's expected
        self.assertGreater(len(excluded_artists), 0, "excluded_artists should not be empty.")
        
        # Check if all elements in the list are strings (if that is expected)
        for artist in excluded_artists:
            self.assertIsInstance(artist, str, "Each artist in excluded_artists should be a string.")

if __name__ == '__main__':
    unittest.main()
