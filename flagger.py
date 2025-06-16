import sys

import pandas as pd
import re

# List of ecclesiastical terms to match (case-insensitive)
institutions = ['bischof', 'erzbischof', 'abt','erzbischöfe', 'bischöfe', 'papst', 'päpste', 'domkapitels', 'domkapitel', 'kloster', 'kapitel']
institution_pattern = re.compile(r'\b(' + '|'.join(institutions) + r')\b', flags=re.IGNORECASE)

def check_ecclesiae_with_matches(charter_summary):
    if pd.isna(charter_summary):
        return False, None
    matches = institution_pattern.findall(charter_summary)
    return (bool(matches), matches if matches else None)

# @args filename - str name of the csv file; processes a single file, adding two columns with flag, if the charter summary contains 'ecclesiastical institutions' and if so, which
def process_csv(filename):
    df = pd.read_csv(f'raw/{filename}.csv')

    # Apply function and unpack results
    results = df['summary'].apply(check_ecclesiae_with_matches)
    df['ecclesiastical_flag'] = results.apply(lambda x: x[0])
    df['ecclesiastical_terms'] = results.apply(lambda x: x[1])

    # Print example rows
    print(df[['fid', 'summary', 'ecclesiastical_flag', 'ecclesiastical_terms']].head())

    # Count True/False
    flag_counts = df['ecclesiastical_flag'].value_counts()
    print("\nCounts:")
    print(f"True (ecclesiastical): {flag_counts.get(True, 0)}")
    print(f"False (non-ecclesiastical): {flag_counts.get(False, 0)}")

    df.to_csv(f'./out/{filename}_flagged.csv', index=False)



if __name__ == "__main__":
    process_csv('konrad')
    process_csv('heinrich')