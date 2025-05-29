import os
import pandas as pd
import glob

# Ensure the output directory exists
os.makedirs('output', exist_ok=True)

# Load all CSV files in the data folder
file_paths = glob.glob(os.path.join('data', '*.csv'))

processed_data = []

for file in file_paths:
    df = pd.read_csv(file)
    df = df[df['product'] == 'pink morsel']
    df['sales'] = df['quantity'] * df['price']
    df = df[['sales', 'date', 'region']]
    processed_data.append(df)

# Combine all data into one DataFrame
final_df = pd.concat(processed_data, ignore_index=True)

# Save to CSV inside the output directory
final_df.to_csv(os.path.join('output', 'pink_morsel_sales.csv'), index=False)

print("✅ File saved successfully to output/pink_morsel_sales.csv")
