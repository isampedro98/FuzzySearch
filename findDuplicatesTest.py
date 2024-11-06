import unittest
import pandas as pd
# Rapid fuzzy string matching in Python and C++ using the Levenshtein Distance
# https://github.com/rapidfuzz/RapidFuzz
from rapidfuzz import fuzz
# combinations, to provide only the non repeated combinations of pairs
from itertools import combinations


def calculate_similarity_score(row1, row2):
    scores = {}

    # Calculate similarity scores only for non-empty fields using RapidFuzz for optimized performance
    scores['first_name'] = fuzz.ratio(str(row1['name']), str(row2['name'])) if row1['name'] and row2['name'] else 0
    scores['last_name'] = fuzz.ratio(str(row1['name1']), str(row2['name1'])) if row1['name1'] and row2['name1'] else 0
    scores['email'] = fuzz.ratio(str(row1['email']), str(row2['email'])) if row1['email'] and row2['email'] else 0
    scores['address'] = fuzz.ratio(str(row1['address']), str(row2['address'])) if row1['address'] and row2['address'] else 0
    scores['postalZip'] = fuzz.ratio(str(row1['postalZip']), str(row2['postalZip'])) if row1['postalZip'] and row2['postalZip'] else 0

    # Compute the overall score as the average of field scores
    overall_score = sum(scores.values()) / len(scores)

    # Determine match accuracy category based on the overall similarity score
    if overall_score > 80:
        match_accuracy = 'High'
    elif 70 <= overall_score <= 80:
        match_accuracy = 'Mid-high'
    elif 50 <= overall_score < 70:
        match_accuracy = 'Mid'
    elif 35 <= overall_score < 50:
        match_accuracy = 'Mid-low'
    else:
        match_accuracy = 'Low'

    # Return a dictionary with detailed match information
    return {
        'ContactID': row1['contactID'],
        'Source ContactID': row2['contactID'],
        'Match Accuracy': match_accuracy,
        'Score': overall_score
    }

class TestDuplicateFinder(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv('testFile.csv').fillna('')

    def test_identical_records(self):
        # Records 1 and 2 are identical
        result = calculate_similarity_score(self.df.iloc[0], self.df.iloc[1])
        self.assertEqual(result['Match Accuracy'], 'High')

    def test_partial_match(self):
        # Records 1 and 3 only partially match
        result = calculate_similarity_score(self.df.iloc[0], self.df.iloc[2])
        self.assertIn(result['Match Accuracy'], ['Mid', 'Mid-low'])

    def test_different_records(self):
        # Records 1 and 4 are completely different
        result = calculate_similarity_score(self.df.iloc[0], self.df.iloc[3])
        self.assertEqual(result['Match Accuracy'], 'Low')

    def test_missing_fields(self):
        # Record 5 has missing values, test for handling of empty fields with Record 2
        result = calculate_similarity_score(self.df.iloc[1], self.df.iloc[4])
        self.assertEqual(result['Match Accuracy'], 'Low')

    def test_high_boundary(self):
        # Records 3 and 4 are similar but have some differences
        result = calculate_similarity_score(self.df.iloc[2], self.df.iloc[3])
        self.assertIn(result['Match Accuracy'], ['Mid-high', 'Mid'])

if __name__ == '__main__':
    unittest.main()