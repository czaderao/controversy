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

if __name__ == "__main__":
    df = pd.read_csv('./res/konrad.csv')

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

    df.to_csv('./res/konrad_flagged.csv', index=False)
    print("\nFlagged data exported to './res/konrad_flagged.csv'")