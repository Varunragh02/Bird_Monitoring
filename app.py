import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Bird Monitoring Dashboard", page_icon="🐦", layout="wide")

# Load data
@st.cache_data

def load_data():
    try:
        df = pd.read_csv("merged_data_cleaned.csv", low_memory=False)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df["Year"] = df["date"].dt.year
            df["Month"] = df["date"].dt.month
            df["month_year"] = df["date"].dt.to_period("M").astype(str)

        if "season" not in df.columns:
            df["Season"] = df["Month"].map({
                12: "Winter", 1: "Winter", 2: "Winter",
                3: "Spring", 4: "Spring", 5: "Spring",
                6: "Summer", 7: "Summer", 8: "Summer",
                9: "Autumn", 10: "Autumn", 11: "Autumn"
            }).fillna("Unknown")

        return df
    except Exception as e:
        st.error(f"❌ Error loading dataset: {e}")
        return None

df = load_data()

# Sidebar
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Select Analysis", [
    "Home", "Temporal Analysis", "Spatial Analysis", "Species Analysis", 
    "Environmental Conditions", "Distance & Behavior", "Observer Trends", "Conservation Insights"])

st.sidebar.title("🔍 Data Filters")

# Filters
if "date" in df.columns:
    start_date = st.sidebar.date_input("Start Date", df["date"].min())
    end_date = st.sidebar.date_input("End Date", df["date"].max())

species_list = df["taxoncode"].dropna().unique() if "taxoncode" in df.columns else []
selected_species = st.sidebar.multiselect("Select Species", species_list)

observer_list = df["observer"].dropna().unique() if "observer" in df.columns else []
selected_observer = st.sidebar.multiselect("Select Observer", observer_list)

# Apply filters
df_filtered = df.copy()
if "date" in df.columns:
    df_filtered = df_filtered[(df_filtered["date"] >= pd.to_datetime(start_date)) &
                              (df_filtered["date"] <= pd.to_datetime(end_date))]
if selected_species:
    df_filtered = df_filtered[df_filtered["taxoncode"].isin(selected_species)]
if selected_observer:
    df_filtered = df_filtered[df_filtered["observer"].isin(selected_observer)]

# Pages
if page == "Home":
    st.title("🐦 Bird Monitoring Dashboard")
    st.write("Explore bird observation trends across different dimensions.")

elif page == "Temporal Analysis":
    st.title("📅 Temporal Analysis")

    if "Season" in df_filtered.columns:
        st.subheader("Observations per Season")
        fig1 = px.histogram(df_filtered, x="Season", color="Season",
                            title="Bird Observations by Season",
                            category_orders={"Season": ["Winter", "Spring", "Summer", "Autumn", "Unknown"]})
        st.plotly_chart(fig1)

    if "month_year" in df_filtered.columns:
        st.subheader("Monthly Observation Trend")
        trend = df_filtered.groupby("month_year").size().reset_index(name="count")
        fig2 = px.line(trend, x="month_year", y="count", title="Monthly Observations Over Time")
        st.plotly_chart(fig2)

elif page == "Spatial Analysis":
    st.title("📍 Spatial Analysis")

    if "location_type" in df_filtered.columns:
        df_filtered["location_type"].fillna("Unknown", inplace=True)
        loc_counts = df_filtered["location_type"].value_counts().reset_index()
        loc_counts.columns = ["Location Type", "Count"]
        fig3 = px.bar(loc_counts, x="Location Type", y="Count", title="Observations by Location Type", color="Location Type")
        st.plotly_chart(fig3)

    if all(col in df_filtered.columns for col in ["latitude", "longitude"]):
        st.subheader("Observation Map")
        fig_map = px.scatter_mapbox(df_filtered, lat="latitude", lon="longitude", hover_name="taxoncode",
                                    color="Season", zoom=3, height=500)
        fig_map.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig_map)

elif page == "Species Analysis":
    st.title("🦜 Species Analysis")

    if "taxoncode" in df_filtered.columns:
        st.subheader("Top Observed Species")
        species_counts = df_filtered["taxoncode"].value_counts().reset_index()
        species_counts.columns = ["Species", "Count"]

        chart_type = st.radio("Choose chart type", ["Bar", "Pie"])
        if chart_type == "Bar":
            fig4 = px.bar(species_counts.head(10), x="Species", y="Count", title="Top 10 Species", color="Species")
            st.plotly_chart(fig4)
        else:
            fig4 = px.pie(species_counts.head(5), names="Species", values="Count", title="Top 5 Species Proportion")
            st.plotly_chart(fig4)

elif page == "Environmental Conditions":
    st.title("🌦️ Environmental Conditions")

    if "temperature" in df_filtered.columns:
        st.subheader("Temperature Distribution")
        fig5 = px.histogram(df_filtered, x="temperature", title="Temperature Histogram", nbins=20)
        st.plotly_chart(fig5)

        if "Season" in df_filtered.columns:
            st.subheader("Temperature by Season")
            fig6 = px.box(df_filtered, x="Season", y="temperature", title="Temperature vs Season")
            st.plotly_chart(fig6)

elif page == "Distance & Behavior":
    st.title("🛫 Distance & Behavior")

    if "distance" in df_filtered.columns:
        st.subheader("Distance Distribution")
        fig7 = px.histogram(df_filtered, x="distance", title="Distance Travelled")
        st.plotly_chart(fig7)

    if "flyover_observed" in df_filtered.columns:
        st.subheader("Flyover Observations")
        flyover_counts = df_filtered["flyover_observed"].value_counts().reset_index()
        flyover_counts.columns = ["Flyover", "Count"]
        fig8 = px.bar(flyover_counts, x="Flyover", y="Count", title="Flyover Frequency", color="Flyover")
        st.plotly_chart(fig8)

elif page == "Observer Trends":
    st.title("🕵️ Observer Trends")

    if "observer" in df_filtered.columns:
        st.subheader("Top 10 Observers")
        observer_counts = df_filtered["observer"].value_counts().head(10).reset_index()
        observer_counts.columns = ["Observer", "Count"]
        fig9 = px.bar(observer_counts, x="Count", y="Observer", orientation="h", title="Top Observers", color="Observer")
        st.plotly_chart(fig9)

elif page == "Conservation Insights":
    st.title("🚨 Conservation Insights")

    if "pif_watchlist_status" in df_filtered.columns:
        st.subheader("Watchlist Species")
        watchlist_counts = df_filtered["pif_watchlist_status"].value_counts().reset_index()
        watchlist_counts.columns = ["Status", "Count"]
        fig10 = px.bar(watchlist_counts, x="Status", y="Count", title="Watchlist Distribution", color="Status")
        st.plotly_chart(fig10)