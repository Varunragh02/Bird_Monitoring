import pandas as pd

class BirdEDA:
    def __init__(self, file_path=r"D:\Guvi\Birds_observation\merged_data_cleaned.csv"):
        """ Load and preprocess data """
        self.df = self.load_data(file_path)

    def load_data(self, file_path):
        """ Load the dataset and perform basic preprocessing """
        try:
            df = pd.read_csv(file_path)  # Removed parse_dates for debugging
            print("📌 Columns in Dataset:", df.columns)  # Debugging step

            # Fix column names if needed (convert to lowercase)
            df.columns = df.columns.str.lower()

            # Parse 'date' column if it exists
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")

            # Add 'Year' and 'Month' columns
            df["year"] = df["date"].dt.year if "date" in df.columns else None
            df["month"] = df["date"].dt.month if "date" in df.columns else None

            # Manually create 'season' column if missing
            if "season" not in df.columns:
                df["season"] = df["month"].map({
                    12: "Winter", 1: "Winter", 2: "Winter",
                    3: "Spring", 4: "Spring", 5: "Spring",
                    6: "Summer", 7: "Summer", 8: "Summer",
                    9: "Autumn", 10: "Autumn", 11: "Autumn"
                }).fillna("Unknown")

            return df
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return None

    # ------- TEMPORAL ANALYSIS -------
    def temporal_analysis(self):
        """ Returns seasonal and hourly observation counts """
        if self.df is None:
            return "❌ Data not loaded properly"

        if "start_time" in self.df.columns:
            self.df["hour"] = pd.to_datetime(self.df["start_time"], errors="coerce").dt.hour

        seasonal_counts = self.df["season"].value_counts() if "season" in self.df.columns else "❌ 'season' column missing"
        hourly_counts = self.df["hour"].value_counts() if "hour" in self.df.columns else "❌ 'hour' column missing"
        return seasonal_counts, hourly_counts

    # ------- SPATIAL ANALYSIS -------
    def spatial_analysis(self):
        """ Returns observation counts by ecosystem and location data if available """
        if self.df is None:
            return "❌ Data not loaded properly"

        ecosystem_counts = self.df["location_type"].value_counts() if "location_type" in self.df.columns else "❌ 'location_type' column missing"
        location_data = self.df[["latitude", "longitude", "taxoncode"]] if all(col in self.df.columns for col in ["latitude", "longitude", "taxoncode"]) else "❌ Location columns missing"
        return ecosystem_counts, location_data

    # ------- SPECIES ANALYSIS -------
    def species_analysis(self):
        """ Returns most observed species """
        if self.df is None:
            return "❌ Data not loaded properly"

        species_counts = self.df["taxoncode"].value_counts() if "taxoncode" in self.df.columns else "❌ 'taxoncode' column missing"
        return species_counts

    # ------- ENVIRONMENTAL CONDITIONS ANALYSIS -------
    def environmental_analysis(self):
        """ Returns insights on temperature, humidity, and observations """
        if self.df is None:
            return "❌ Data not loaded properly"

        temperature_data = self.df["temperature"].dropna() if "temperature" in self.df.columns else "❌ 'temperature' column missing"
        humidity_data = self.df["humidity"].dropna() if "humidity" in self.df.columns else "❌ 'humidity' column missing"
        return temperature_data, humidity_data

    # ------- DISTANCE & BEHAVIOR ANALYSIS -------
    def distance_behavior_analysis(self):
        """ Returns distance traveled and flyover frequency """
        if self.df is None:
            return "❌ Data not loaded properly"

        distance_data = self.df["distance"].dropna() if "distance" in self.df.columns else "❌ 'distance' column missing"
        flyover_counts = self.df["flyover_observed"].value_counts() if "flyover_observed" in self.df.columns else "❌ 'flyover_observed' column missing"
        return distance_data, flyover_counts

    # ------- OBSERVER TRENDS ANALYSIS -------
    def observer_trends(self):
        """ Returns observer activity insights """
        if self.df is None:
            return "❌ Data not loaded properly"

        observer_counts = self.df["observer"].value_counts() if "observer" in self.df.columns else "❌ 'observer' column missing"
        return observer_counts

    # ------- CONSERVATION INSIGHTS -------
    def conservation_insights(self):
        """ Returns watchlist status counts """
        if self.df is None:
            return "❌ Data not loaded properly"

        watchlist_counts = self.df["pif_watchlist_status"].value_counts() if "pif_watchlist_status" in self.df.columns else "❌ 'pif_watchlist_status' column missing"
        return watchlist_counts


# Example Usage:
if __name__ == "__main__":
    eda = BirdEDA()

    print("\n🔹 Temporal Analysis:", eda.temporal_analysis())
    print("\n🔹 Spatial Analysis:", eda.spatial_analysis())
    print("\n🔹 Species Analysis:", eda.species_analysis())
    print("\n🔹 Environmental Analysis:", eda.environmental_analysis())
    print("\n🔹 Distance & Behavior Analysis:", eda.distance_behavior_analysis())
    print("\n🔹 Observer Trends:", eda.observer_trends())
    print("\n🔹 Conservation Insights:", eda.conservation_insights())