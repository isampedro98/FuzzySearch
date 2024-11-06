
# Duplicate Finder Script

This Python script identifies potential duplicate entries in a dataset of contact information by comparing fields such as first name, last name, email address, and street address. It uses fuzzy matching to determine similarity scores and categorizes matches into High, Mid-high, Mid-low and Low accuracy levels based on configurable thresholds.

## Features
- **Fuzzy Matching**: Utilizes RapidFuzz for optimized string similarity calculations.
- **Batch Processing**: Processes data in batches for memory efficiency.
- **Categorized Outputs**: Saves High, Mid-high, and Low matches into separate CSV files for easy review.

## Requirements

- Python 3.x
- Required Python packages:
  - `pandas` (for data handling)
  - `rapidfuzz` (for optimized fuzzy matching)
  
Install the required packages using:
```bash
pip install pandas rapidfuzz
```

## Usage

1. **Prepare the Data**: Ensure your contact data is in a CSV file format. The file should contain columns for `name`, `name1`, `email`, `address`, and `contactID`.

2. **Run the Script**:
   Execute the script from the command line, passing in the CSV file as an argument. Optionally, specify a `batch_size` to control memory usage.
   ```bash
   python duplicate_finder.py <your_filename.csv> --batch_size 500
   ```
   Example:
   ```bash
   python duplicate_finder.py sample_contacts.csv --batch_size 500
   ```

3. **Arguments**:
   The script has 5 arguments:
   - `filename`: The path to your CSV file.
   - `--batch_size`: (Optional) The number of rows to process at a time. Defaults to 1000.
   - `--high`: (Optional) The threshold score for a "High" match. Defaults to 80.
   - `--mid-high`: (Optional) The threshold score for a "Mid-high" match, should be lower than high. Defaults to 70.
   - `--mid`: (Optional) The threshold score for a "Mid" match, should be lower than mid-high. Defaults to 50.
   - `--mid-low`: (Optional) The threshold score for a "Mid-low" match. Defaults to 35.

4. **Output Files**:
   The script generates three output files:
   - `high_matches.csv`: Contains high-confidence matches.
   - `mid_high_matches.csv`: Contains mid-high confidence matches.
   - `low_matches.csv`: Contains lower confidence matches for further review if needed.

## How It Works

1. **Data Loading**: Loads data from the specified CSV file and fills missing values with empty strings.
2. **Similarity Calculation**: Compares pairs of records based on name, email, and address fields, using fuzzy matching to calculate a similarity score for each field.
3. **Categorizing Matches**: Determines match accuracy based on an overall similarity score:
   - `High`: Scores over the `high` threshold (default 80%)
   - `Mid-high`: Scores between the `--mid-high` and `high` thresholds (default 70%-80%)
   - `Mid`: Scores between the `--mid` and `--mid-high` thresholds (default 50%-70%)
   - `Mid-low`: Scores between the `--mid-low` and `--mid` thresholds (default 35%-50%)
   - `Low`: Scores below the `--mid-low` threshold (default below 35%)
4. **Batch Processing**: Processes data in defined batches to reduce memory and CPU load.
5. **File Output**: Saves matches in separate CSV files based on accuracy categories.

## Example Output

After running the script, you will find three CSV files:
```plaintext
high_matches.csv       # High-confidence matches
mid_high_matches.csv   # Mid-high confidence matches
low_matches.csv        # Lower confidence matches
```

## Customizing the Code

Feel free to adjust the match accuracy thresholds or batch size to meet your specific requirements:
- **Thresholds** can be modified in the command-line arguments `--high`, `--mid-high`, `--mid`, and `--mid-low`.
- **Batch size** can be specified as a command-line argument or adjusted in the code.