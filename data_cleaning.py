import pandas as pd

def merge_and_clean_data(grassland_path, forest_path, output_path):
    """Merges, cleans, and saves bird monitoring data with EDA readiness summary"""

    def load_data(file_path):
        try:
            df = pd.read_excel(file_path)
            print("📂 Loaded:", file_path, "Shape:", df.shape)
            return df
        except Exception as e:
            print("❌ Error loading", file_path, ":", str(e))
            return None

    # Load both datasets
    df1 = load_data(grassland_path)
    df2 = load_data(forest_path)

    # Merge logic
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
    empty_cols = df.columns[df.isnull().all()]
    if not empty_cols.empty:
        print("🧹 Dropping empty columns:", list(empty_cols))
    df.dropna(axis=1, how='all', inplace=True)
    df.drop_duplicates(inplace=True)

    # ✅ Strip whitespace from string columns using a simple loop
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()

    # Convert 'date' to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    if 'date' in df.columns and df['date'].isnull().all():
        print("⚠️ All values in 'date' column are invalid. Removing 'date' and derived columns.")
        df.drop(columns=['date'], inplace=True, errors='ignore')
        df['year'] = None
        df['month'] = None
        df['season'] = None
    else:
        df["year"] = df["date"].dt.year if "date" in df.columns else None
        df["month"] = df["date"].dt.month if "date" in df.columns else None
        df["season"] = df["month"].map({
            12: "Winter", 1: "Winter", 2: "Winter",
            3: "Spring", 4: "Spring", 5: "Spring",
            6: "Summer", 7: "Summer", 8: "Summer"
        }).fillna("Autumn")

    # Check if DataFrame is empty
    if df.empty:
        print("❌ Merged dataset is empty after cleaning. Cannot proceed with EDA summary.")
        return

    # Fill missing categorical values
    categorical_cols = ["ecosystem", "location_type", "pif_watchlist_status", "observer", "flyover", "sky", "wind", "disturbance", "id_method"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Fill missing numeric values
    numeric_cols = ["temperature", "humidity", "interval_length"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median())

    # Clean distance column
    if "distance" in df.columns:
        df["distance"] = df["distance"].astype(str).str.extract(r'(\d+)').astype(float)
        df["distance"] = df["distance"].fillna(df["distance"].median())

    # Fill missing coordinates
    if "latitude" in df.columns and "longitude" in df.columns:
        df["latitude"] = df["latitude"].fillna(df["latitude"].median())
        df["longitude"] = df["longitude"].fillna(df["longitude"].median())

    # Save the cleaned data
    df.to_csv(output_path, index=False)
    print("✅ Cleaned data saved at:", output_path)
    print("✅ Final Dataset Shape:", df.shape)

    # EDA Readiness Summary
    print("\n🔍 EDA Readiness Summary:")
    eda_columns = {
        "Date/Time Features": ["date", "year", "month", "season"],
        "Species Info": ["scientific_name", "common_name", "aou_code"],
        "Location Info": ["location_type", "plot_name", "ecosystem", "latitude", "longitude"],
        "Environmental Conditions": ["temperature", "humidity", "sky", "wind", "disturbance"],
        "Behavioral Metrics": ["distance", "flyover", "interval_length", "id_method"],
        "Observer Info": ["observer", "visit"],
        "Conservation Status": ["pif_watchlist_status", "regional_stewardship_status"],
        "Demographics": ["sex"]
    }

    for category, cols in eda_columns.items():
        available = [col for col in cols if col in df.columns]
        missing = [col for col in cols if col not in df.columns]
        print(f"📌 {category}:")
        print(f"   ✅ Available: {available}")
        print(f"   ❌ Missing  : {missing}\n")

    print("🎉 Data is cleaned and ready for EDA!")

if __name__ == "__main__":
    # 🔁 Replace these with your actual file paths
    grassland_path = "D:/Guvi/Birds_observation/Bird_Monitoring_Data_GRASSLAND.xlsx"
    forest_path = "D:/Guvi/Birds_observation/Bird_Monitoring_Data_FOREST.xlsx"
    output_path = "D:/Guvi/Birds_observation/merged_data_cleaned.csv"

    merge_and_clean_data(grassland_path, forest_path, output_path)