import pandas as pd
import os

def load_csv(filepath):
    """Load a CSV file and handle potential encoding issues."""
    try:
        return pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(filepath, encoding='ISO-8859-1')

def merge_cofog_files(archive_dir="archive"):
    """Merge all COFOG CSV files from the archive directory."""
    # Load all CSV files
    english_df = load_csv(os.path.join(archive_dir, "cofog_english.csv"))
    french_df = load_csv(os.path.join(archive_dir, "cofog_french.csv"))
    spanish_df = load_csv(os.path.join(archive_dir, "cofog_spanish.csv"))
    notes_df = load_csv(os.path.join(archive_dir, "cofog_extended_notes.csv"))

    # Rename columns to avoid conflicts
    english_df = english_df.rename(columns={'Description': 'Description_EN'})
    french_df = french_df.rename(columns={'Description': 'Description_FR'})
    spanish_df = spanish_df.rename(columns={'Description': 'Description_ES'})

    # Merge all dataframes on 'Code' column
    merged_df = english_df.merge(
        french_df, on='Code', how='outer'
    ).merge(
        spanish_df, on='Code', how='outer'
    ).merge(
        notes_df, on='Code', how='outer'
    )

    # Reorder columns
    column_order = [
        'Code',
        'Description_EN',
        'Description_FR',
        'Description_ES',
        'ExplanatoryNote'
    ]
    merged_df = merged_df[column_order]

    # Sort by Code
    merged_df['SortKey'] = merged_df['Code'].str.extract('(\d+(?:\.\d+)*)', expand=False)
    merged_df['SortKey'] = merged_df['SortKey'].apply(lambda x: [int(n) for n in x.split('.')] if pd.notnull(x) else [])
    merged_df = merged_df.sort_values('SortKey')
    merged_df = merged_df.drop('SortKey', axis=1)

    # Save merged file
    output_path = "data/cofog.csv"
    merged_df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Merged file saved to: {output_path}")
    print(f"Total entries: {len(merged_df)}")
    print("\nFirst few entries:")
    print(merged_df.head().to_string())

if __name__ == "__main__":
    merge_cofog_files()