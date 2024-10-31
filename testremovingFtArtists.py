import unittest
import re

# Sample mock function simulating `remove_featuring_artists` behavior
# Update this section with the actual function from your code
def remove_featuring_artists(title):
    # Patterns from the uploaded file
    pattern1 = re.compile(r"\s*\(f(?:ea)?t(?:\.|uring)? ([^)]+)\)", re.IGNORECASE)
    pattern2 = re.compile(r"\s*f(?:ea)?t(?:\.|uring)?\s+(.+)", re.IGNORECASE)
    
    # Apply patterns to remove featuring artists
    title = pattern1.sub('', title)  # Remove (feat. Artist)
    title = pattern2.sub('', title)  # Remove feat. Artist without brackets
    return title.strip()

# Test cases for edge cases
class TestRemoveFeaturingArtists(unittest.TestCase):
    
    def test_no_featured_artist(self):
        """Test when there is no 'feat.' in title."""
        title = "Song Without Featured Artist"
        self.assertEqual(remove_featuring_artists(title), title)
        
    def test_single_featured_artist_parentheses(self):
        """Test single featured artist with parentheses."""
        title = "Song Title (feat. Artist)"
        expected = "Song Title"
        self.assertEqual(remove_featuring_artists(title), expected)

    def test_single_featured_artist_no_parentheses(self):
        """Test single featured artist without parentheses."""
        title = "Song Title feat. Artist"
        expected = "Song Title"
        self.assertEqual(remove_featuring_artists(title), expected)
        
    def test_multiple_featured_artists(self):
        """Test multiple featured artists."""
        title = "Song Title (feat. Artist1, Artist2)"
        expected = "Song Title"
        self.assertEqual(remove_featuring_artists(title), expected)

    def test_non_standard_variant_featuring(self):
        """Test non-standard 'featuring' format."""
        title = "Song Title featuring Artist"
        expected = "Song Title"
        self.assertEqual(remove_featuring_artists(title), expected)
        
    def test_parentheses_without_feature(self):
        """Test title with parentheses for other reasons."""
        title = "Song Title (Live)"
        expected = "Song Title (Live)"
        self.assertEqual(remove_featuring_artists(title), expected)
        
    def test_excluded_artist(self):
        """Test title with an excluded artist."""
        # Here we mock exclusion by assuming ExcludedArtist should not be removed.
        # In the actual function, you would use the exclusion logic.
        excluded_artist_title = "Song Title feat. ExcludedArtist"
        expected = "Song Title feat. ExcludedArtist"  # Title remains the same
        self.assertEqual(remove_featuring_artists(excluded_artist_title), expected)

# Run the tests
if __name__ == "__main__":
    unittest.main()
