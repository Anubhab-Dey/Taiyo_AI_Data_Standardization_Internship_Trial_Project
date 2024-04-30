import pandas as pd
import re

INPUT_FILE_PATH = "Data/USA/Input/Historical/FY2023_archived_opportunities_(Sample,_Trimmed).csv"
OUTPUT_FILE_PATH = "Data/USA/Output/Historical/FY_2023_(Sample).csv"


def clean_name(name):
    # Regular expressions to clean the names
    cleaned = re.sub(
        r"\s+\[UEI:.*\]", "", name
    )  # Remove UEI and following characters
    cleaned = re.sub(
        r"\s+\d{5}(?:[-\s]\d{4})?.*$", "", cleaned
    )  # Remove zip code and everything after
    cleaned = re.sub(
        r",.*", "", cleaned
    )  # Remove anything after a comma (like city, state)
    cleaned = re.sub(r'\.\s*$', '', cleaned)  # Remove trailing periods if any
    cleaned = cleaned.strip()  # Remove leading/trailing whitespace
    return cleaned


# Load your data with the correct encoding
data = pd.read_csv(INPUT_FILE_PATH, encoding='windows-1252')

# Apply cleaning function to the necessarycolumns
data['Cleaned Department/Ind.Agency'] = (
    data['Department/Ind.Agency'].astype(str).apply(clean_name)
)
data['Cleaned Sub-Tier'] = data['Sub-Tier'].astype(str).apply(clean_name)
data['Cleaned Awardee'] = data['Awardee'].astype(str).apply(clean_name)

# Save the cleaned data to a new CSV file
data.to_csv(OUTPUT_FILE_PATH, index=False)
