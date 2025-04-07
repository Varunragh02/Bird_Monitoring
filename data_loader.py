import pandas as pd

def load_data(filepath="merged_data_cleaned.csv"):
    df = pd.read_csv(filepath, low_memory=False)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["month_year"] = df["date"].dt.to_period("M").astype(str)

    df["season"] = df["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    }).fillna("Unknown")

    return df
