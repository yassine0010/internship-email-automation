import pandas as pd
import os

input_file = '/Users/yassinebenayed/Desktop/cleaning/Export.csv'
output_file = '/Users/yassinebenayed/Desktop/cleaning/Export_cleaned.csv'

# Read the CSV with error handling for malformed data
df = pd.read_csv(input_file, sep=';', on_bad_lines='skip', engine='python')

print(f"Original data: {len(df)} rows")
print(f"Columns: {list(df.columns)}\n")

# Standardize emails: lower case and remove extra spaces
if 'Email entreprise' in df.columns:
    df['Email entreprise'] = df['Email entreprise'].astype(str).str.strip().str.lower()
    
    # Remove rows where email is empty, 'nan', or clearly invalid (missing @)
    df = df[
        ~df['Email entreprise'].isin(['', 'nan', 'none', 'null']) &
        df['Email entreprise'].str.contains('@', na=False)
    ]

# Remove duplicates based on email (primary key)
# Keep first occurrence of each unique email
df_cleaned = df.drop_duplicates(subset=['Email entreprise'], keep='first')

print(f"After removing duplicates by email: {len(df_cleaned)} rows")
print(f"Removed {len(df) - len(df_cleaned)} duplicate entries\n")

# Optional: Clean up common data issues
# Replace invalid phone/fax numbers with empty string
phone_columns = ['Téléphone', 'Fax']
for col in phone_columns:
    if col in df_cleaned.columns:
        df_cleaned[col] = df_cleaned[col].astype(str).replace(
            ['X', '.', 'N/A', '//', '00000000', '0000000', '0000', '-------', 'Non disponible', '-'], 
            ''
        )

# Save the cleaned data
df_cleaned.to_csv(output_file, sep=';', index=False, quoting=1)

print(f"✓ Cleaned data saved to: {output_file}")
print(f"\nSummary:")
print(f"- Original records: {len(df)}")
print(f"- Cleaned records: {len(df_cleaned)}")
print(f"- Duplicates removed: {len(df) - len(df_cleaned)}")

# Show some statistics
print(f"\n--- Data Quality Report ---")
missing_emails = (df_cleaned['Email entreprise'].isna().sum() + 
                  (df_cleaned['Email entreprise'].astype(str).str.strip() == '').sum())
print(f"Missing/empty emails: {missing_emails}")
