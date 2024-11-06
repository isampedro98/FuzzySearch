import pandas as pd
# Rapid fuzzy string matching in Python and C++ using the Levenshtein Distance
# https://github.com/rapidfuzz/RapidFuzz
from rapidfuzz import fuzz

# combinations, to provide only the non repeated combinations of pairs
from itertools import combinations
import argparse

# Set up argument parsing to accept various parameters from the command line
parser = argparse.ArgumentParser(description="Duplicate Finder Script")
parser.add_argument("filename", type=str, help="The CSV file to process")
parser.add_argument("--batch_size", type=int, default=1000, help="Batch size for processing (default: 1000)")
parser.add_argument("--high", type=int, default=80, help="High match score (default: 80)")
parser.add_argument("--mid-high", type=int, default=70, help="Mid-high match score (default: 70; must be lower than high)")
parser.add_argument("--mid", type=int, default=50, help="Mid match score (default: 50; must be lower than mid-high)")
parser.add_argument("--mid-low", type=int, default=35, help="Mid-low match score (default: 35)")
args = parser.parse_args()

# Load data from the provided filename, filling NaN values with empty strings for consistent processing
df = pd.read_csv(args.filename).fillna('')

# Function to calculate similarity scores across fields and assign match accuracy
# Compares two rows of data on specific fields using fuzzy matching and computes an overall similarity score.
# Categorizes match accuracy based on provided thresholds.
def calculate_similarity_score(row1, row2):
    scores = {}

    # Calculate similarity scores only for non-empty fields using RapidFuzz for optimized performance
    scores['first_name'] = fuzz.ratio(str(row1['name']), str(row2['name'])) if row1['name'] and row2['name'] else 0
    scores['last_name'] = fuzz.ratio(str(row1['name1']), str(row2['name1'])) if row1['name1'] and row2['name1'] else 0
    scores['email'] = fuzz.ratio(str(row1['email']), str(row2['email'])) if row1['email'] and row2['email'] else 0

    # These last ones can be commented out, as though it provides the exact duplicate, but taking into account
    # that the mistake in the address and postalzip can be ignored. If first name, last name and email are the same, then we should be already talking about the same person/contact
    scores['postalZip'] = fuzz.ratio(str(row1['postalZip']), str(row2['postalZip'])) if row1['postalZip'] and row2['postalZip'] else 0
    scores['address'] = fuzz.ratio(str(row1['address']), str(row2['address'])) if row1['address'] and row2['address'] else 0

    # Compute the overall score as the average of field scores
    overall_score = sum(scores.values()) / len(scores)

    # Determine match accuracy category based on the overall similarity score
    if overall_score > args.high:
        match_accuracy = 'High'
    elif args.mid_high <= overall_score <= args.high:
        match_accuracy = 'Mid-high'
    elif args.mid <= overall_score < args.mid_high:
        match_accuracy = 'Mid'
    elif args.mid_low <= overall_score < args.mid:
        match_accuracy = 'Mid-low'
    else:
        match_accuracy = 'Low'

    # Return a dictionary with detailed match information
    return {
        'ContactID': row1['contactID'],
        'Source ContactID': row2['contactID'],
        'Match Accuracy': match_accuracy,
    }

# Initialize lists to store matches categorized by accuracy
high_matches = []
mid_high_matches = []
low_matches = []

# Define batch size to control memory usage for processing large datasets
batch_size = args.batch_size

# Process records in manageable batches to reduce memory and CPU usage
# Batch processing trades accuracy for speed if the dataset is divided into small parts.
# To maximize accuracy, you can set batch_size equal to the total dataset size
for start in range(0, len(df), batch_size):
    end = min(start + batch_size, len(df))
    batch = df.iloc[start:end]

    # Generate unique pairs within the batch and calculate similarity scores
    for i, j in combinations(batch.index, 2):
        result = calculate_similarity_score(df.loc[i], df.loc[j])

        # Categorize the match into High, Mid-high, or Low based on accuracy
        if result['Match Accuracy'] == 'High':
            high_matches.append(result)
        elif result['Match Accuracy'] == 'Mid-high':
            mid_high_matches.append(result)
        else:
            low_matches.append(result)

# Save each category of matches to separate CSV files for easy review
pd.DataFrame(high_matches).to_csv('high_matches.csv', index=False)
pd.DataFrame(mid_high_matches).to_csv('mid_high_matches.csv', index=False)
pd.DataFrame(low_matches).to_csv('low_matches.csv', index=False)

# Notify the user about the created output files
print("Files created: 'high_matches.csv', 'mid_high_matches.csv', 'low_matches.csv'")
