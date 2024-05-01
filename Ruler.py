import pandas as pd
import re

INPUT_FILE_PATH = "Data/USA/Input/Historical/FY2023_archived_opportunities_(Sample,_Trimmed).csv"
OUTPUT_FILE_PATH = "Data/USA/Output/Historical/FY_2023_(Sample).csv"


def clean_title(title):
    # Remove numerical prefixes that may include dashes or other separators
    title = re.sub(r"^\d+\s*[-–—]\s*", "", title)

    # Remove fiscal year mentions, often denoted as "FY" followed by digits
    title = re.sub(r"\bFY\d+\b", "", title)

    # Remove any standalone numbers and common terms like "Buy#", "Project" followed by numbers
    title = re.sub(r"\b(Buy#|Project)\s*\d+\b", "", title)

    # General clean-up for common contractual terms or codes
    title = re.sub(r"\bQ\d+\b|\bSFB\b|Contract\s*\#\d+", "", title)

    # Remove UEI codes and anything following them
    title = re.sub(r"\s+\[UEI:.*\]", "", title)

    # Remove zip codes and anything that follows
    title = re.sub(r"\s+\d{5}(?:[-\s]\d{4})?.*$", "", title)

    # Remove any content after a comma, often geographic or organizational details
    title = re.sub(r",.*", "", title)

    # Clean up trailing periods and extra spaces
    title = re.sub(r'\\.?\s*$', '', title)

    # Attempt to strip out common location patterns and trailing geographic details
    title = re.sub(r"-\s*[A-Za-z\s]*$", "", title)

    # Remove any remaining numeric prefixes or suffixes
    title = re.sub(r"^\d+\s*|--\s*\d+", "", title)

    # Remove any remaining references to quarters (Q1, Q2, etc.)
    title = re.sub(r"\bQ\d\b", "", title)

    # Removes trailing locations after a dash
    # Clean up extra spaces and dashes leftover from removals
    title = re.sub(r"\s{2,}", " ", title)  # Collapse multiple spaces into one
    title = re.sub(
        r"\s*-\s*", " - ", title
    )  # Standardize spacing around dashes
    title = title.strip()

    return title


# Load your data with the correct encoding
data = pd.read_csv(INPUT_FILE_PATH, encoding='utf-8')

# Apply cleaning function to the necessarycolumns
data['Cleaned Department/Ind.Agency'] = (
    data['Department/Ind.Agency'].astype(str).apply(clean_title)
)
data['Cleaned Sub-Tier'] = data['Sub-Tier'].astype(str).apply(clean_title)
data['Cleaned Awardee'] = data['Awardee'].astype(str).apply(clean_title)

# Save the cleaned data to a new CSV file
data.to_csv(OUTPUT_FILE_PATH, index=False)
