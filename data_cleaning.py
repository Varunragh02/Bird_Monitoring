import pandas as pd

def merge_and_clean_data(grassland_path, forest_path, output_path):
    """ Merges, cleans, and saves bird monitoring data """

    def load_data(file_path):
        try:
            df = pd.read_excel(file_path)
            print("📂 Loaded:", file_path, "Shape:", df.shape)
            return df
        except Exception as e:
            print("❌ Error loading", file_path, ":", str(e))
            return None

    df1 = load_data(grassland_path)
    df2 = load_data(forest_path)

    if df1 is None and df2 is None:
        print("❌ Both datasets are missing. Cannot proceed.")
        return
    elif df1 is None:
        df = df2
    elif df2 is None:
        df = df1
    else:
        df = pd.concat([df1, df2], ignore_index=True)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Drop completely empty rows and columns
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    df.drop_duplicates(inplace=True)

    # Convert 'date' column to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Extract Year and Month
    df["year"] = df["date"].dt.year if "date" in df.columns else None
    df["month"] = df["date"].dt.month if "date" in df.columns else None

    # Categorize months into seasons
    df["season"] = df["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer"
    }).fillna("Autumn")

    # Fill missing categorical values (Updated for Pandas 3.0)
    categorical_cols = ["ecosystem", "location_type", "pif_watchlist_status", "observer", "flyover"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Fill missing numeric values with median
    numeric_cols = ["temperature", "humidity"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # Convert 'distance' column from text to numeric bins
    if "distance" in df.columns:
        df["distance"] = df["distance"].astype(str).str.extract(r'(\d+)').astype(float)
        df["distance"] = df["distance"].fillna(df["distance"].median())

    # Fill missing location data
    if "latitude" in df.columns and "longitude" in df.columns:
        df["latitude"] = df["latitude"].fillna(df["latitude"].median())
        df["longitude"] = df["longitude"].fillna(df["longitude"].median())

    # Save cleaned dataset
    df.to_csv(output_path, index=False)
    print("✅ Cleaned data saved at:", output_path)
    print("✅ Final Dataset Shape:", df.shape)

# Example Usage
if __name__ == "__main__":
    merge_and_clean_data(
        r"D:\Guvi\Birds_observation\Bird_Monitoring_Data_GRASSLAND.XLSX",
        r"D:\Guvi\Birds_observation\Bird_Monitoring_Data_FOREST.XLSX",
        r"D:\Guvi\Birds_observation\merged_data_cleaned.csv"
    )
