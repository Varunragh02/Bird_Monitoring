import pandas as pd
from sqlalchemy import create_engine

# 🛠️ Update these values with your own
DB_USER = "root"
DB_PASSWORD = "Selvamk1403#"
DB_HOST = "localhost"
DB_NAME = "bird_monitoring"
CSV_PATH = r"D:\Guvi\Birds_observation\merged_data_cleaned.csv"

# Step 1: Load the cleaned CSV
df = pd.read_csv(CSV_PATH)

# Step 2: Convert 'date' to proper format (optional if already clean)
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

# Step 3: Connect to MySQL
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
df.to_sql("bird_monitoring_data", con=engine, if_exists="replace", index=False)
print("✅ Data successfully inserted into MySQL database!")
# Step 4: Insert into MySQL table
with engine.begin() as conn:
    df.to_sql('bird_monitoring_data', con=conn, if_exists='append', index=False)
    print("✅ Data successfully inserted into 'bird_monitoring_data' table!")
