import pandas as pd

# Step 1: Read the Excel file
anketa = pd.read_excel("Downloads/anketa126828-2024-07-20-2.xlsx")

# Step 2: Add a new column to indicate inclusion (1) or exclusion (0)
anketa['included'] = 1

# Social media platforms
social_media = ["Instagram", "TikTok", "FB", "whatsApp", "LinkedIn", "Twitter", "Youtube", "Snapchat", "Threads", "Pinterest", "other"]

# Function to process the data for perception time
i = 51
k = 0
new_columns = {}
while i < 73:
    values_1 = pd.to_numeric(anketa.iloc[:, i], errors='coerce').fillna(0)
    values_2 = pd.to_numeric(anketa.iloc[:, i + 1], errors='coerce').fillna(0)
    values_1[values_1 < 0] = 0
    values_2[values_2 < 0] = 0
    new_column_name = f"{social_media[k]} perception"
    new_columns[new_column_name] = values_1 * 60 + values_2

    k += 1
    i += 2

new_columns_df = pd.DataFrame(new_columns)
df = pd.concat([anketa, new_columns_df], axis=1)

# Function to process the data for actual time
i = 74
k = 0
new_columns = {}
social_media = ["time spend on all social media apps"] + social_media
while i < 99:
    values_3 = pd.to_numeric(df.iloc[:, i], errors='coerce').fillna(0)
    values_4 = pd.to_numeric(df.iloc[:, i + 1], errors='coerce').fillna(0)
    values_3[values_3 < 0] = 0
    values_4[values_4 < 0] = 0
    new_column_name = f"{social_media[k]} actual"
    new_columns[new_column_name] = values_3 * 60 + values_4

    k += 1
    i += 2
    if i == 96:
        i += 1

new_columns_df = pd.DataFrame(new_columns)
df = pd.concat([df, new_columns_df], axis=1)

# Update the 'included' column based on your previous criteria
df['included'] = df.apply(lambda row: 0 if pd.isna(row['Perception of time on all social media']) or pd.isna(row['Other social media']) else 1, axis=1)

# Drop the specified columns
df.drop(columns=df.columns[4:16].tolist() + df.columns[28:49].tolist() + df.columns[51:73].tolist() + df.columns[74:98].tolist(), inplace=True)

# Rename columns
df.rename(columns={df.columns[14]: "Perception of time on all social media", df.columns[15]: "Other social media"}, inplace=True)

# Convert columns to numeric and handle negative values
df.replace({"-1": None, "-2": None}, inplace=True)
df["Perception of time on all social media"] = pd.to_numeric(df["Perception of time on all social media"], errors='coerce') * 60

# Save the updated data to an Excel file
df.to_excel("updated_podatki2.xlsx", index=False)

# Display the summary of the updated data
print(df.describe())