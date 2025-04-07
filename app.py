import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Load the merged and preprocessed data
df = pd.read_csv("merged_data_cleaned.csv")

# Convert date columns to datetime
df["date"] = pd.to_datetime(df["date"], errors='coerce')
df["year"] = df["date"].dt.year
if "month" not in df.columns:
    df["month"] = df["date"].dt.month

# Filter sidebar
st.sidebar.header("🔍 Filters")

# Location Types Filter 
with st.sidebar.expander("Select Location Types", expanded=False):
    location_types = st.multiselect(
        "Choose Location Types:",
        options=df["location_type"].dropna().unique(),
        default=df["location_type"].dropna().unique()
    )

# Species Filter 
with st.sidebar.expander("Select Species", expanded=False):
    selected_species = st.multiselect(
        "Choose Species:",
        options=df["scientific_name"].dropna().unique(),
        default=df["scientific_name"].dropna().unique()
    )

# Filtered dataframe
df_filtered = df[df["location_type"].isin(location_types) & df["scientific_name"].isin(selected_species)]

# Page selection
page = st.sidebar.selectbox("Select Analysis Page", (
    "Temporal Analysis", "Spatial Analysis", "Species Analysis",
    "Environmental Conditions", "Distance & Behavior", "Observer Trends",
    "Conservation Insights", "Other Insights"
))

# 1. Temporal Analysis
if page == "Temporal Analysis":
    st.title("📅 Temporal Analysis")
    st.subheader("Observations Over Time")
    if "date" in df_filtered.columns:
        df_filtered['season'] = df_filtered['month'] % 12 // 3 + 1
        df_filtered['season'] = df_filtered['season'].map({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})

        col1, col2 = st.columns(2)

        with col1:
            fig_month = px.histogram(df_filtered, x="month", nbins=12, title="Monthly Bird Observations")
            st.plotly_chart(fig_month)

        with col2:
            fig_year = px.histogram(df_filtered, x="year", title="Yearly Bird Observations")
            st.plotly_chart(fig_year)

        st.subheader("Observation Time Range")
        if "start_time" in df_filtered.columns and "end_time" in df_filtered.columns:
            df_filtered["start_hour"] = pd.to_datetime(df_filtered["start_time"], errors='coerce').dt.hour
            df_filtered["end_hour"] = pd.to_datetime(df_filtered["end_time"], errors='coerce').dt.hour
            fig_time = px.histogram(df_filtered, x="start_hour", nbins=24, title="Start Time of Observations")
            st.plotly_chart(fig_time)

# 2. Spatial Analysis
elif page == "Spatial Analysis":
    st.title("📍 Spatial Analysis")

    if "location_type" in df_filtered.columns:
        st.subheader("Species Distribution by Location Type")
        location_species = df_filtered.groupby("location_type")["scientific_name"].nunique().reset_index()
        location_species.columns = ["Location Type", "Unique Species"]
        fig_loc = px.bar(location_species, x="Location Type", y="Unique Species", color="Location Type", title="Unique Species per Location Type")
        st.plotly_chart(fig_loc)

    if "plot_name" in df_filtered.columns:
        st.subheader("Observations by Plot")
        plot_species = df_filtered.groupby("plot_name")["scientific_name"].nunique().reset_index().sort_values(by="scientific_name", ascending=False)
        plot_species.columns = ["Plot Name", "Unique Species"]
        fig_plot = px.bar(plot_species.head(20), x="Plot Name", y="Unique Species", title="Top 20 Plots by Species Count")
        st.plotly_chart(fig_plot)

# 3. Species Analysis
elif page == "Species Analysis":
    st.title("🕊️ Species Analysis")

    st.subheader("Species Diversity by Habitat")
    if "location_type" in df_filtered.columns:
        diversity = df_filtered.groupby("location_type")["scientific_name"].nunique().reset_index()
        diversity.columns = ["Location Type", "Unique Species"]
        fig_div = px.bar(diversity, x="Location Type", y="Unique Species", color="Location Type", title="Species Diversity by Location")
        st.plotly_chart(fig_div)

    st.subheader("Common Activities")
    if "interval_length" in df_filtered.columns and "id_method" in df_filtered.columns:
        activity_counts = df_filtered.groupby("id_method")["interval_length"].count().reset_index()
        activity_counts.columns = ["Identification Method", "Count"]
        fig_act = px.pie(activity_counts, names="Identification Method", values="Count", title="Activity Types (via ID Method)")
        st.plotly_chart(fig_act)

    st.subheader("Sex Ratio")
    if "sex" in df_filtered.columns:
        sex_counts = df_filtered["sex"].value_counts().reset_index()
        sex_counts.columns = ["Sex", "Count"]
        fig_sex = px.bar(sex_counts, x="Sex", y="Count", color="Sex", title="Male to Female Observation Ratio")
        st.plotly_chart(fig_sex)

# 4. Environmental Conditions
elif page == "Environmental Conditions":
    st.title("🌦️ Environmental Conditions")

    if "temperature" in df_filtered.columns:
        st.subheader("Temperature Distribution")
        fig_temp = px.histogram(df_filtered, x="temperature", title="Temperature Histogram", nbins=30)
        st.plotly_chart(fig_temp)

        if "season" in df_filtered.columns:
            st.subheader("Temperature by Season")
            fig_temp_season = px.box(df_filtered, x="season", y="temperature", title="Temperature vs Season")
            st.plotly_chart(fig_temp_season)

    if "humidity" in df_filtered.columns:
        st.subheader("Humidity Distribution")
        fig_humidity = px.histogram(df_filtered, x="humidity", title="Humidity Histogram", nbins=30)
        st.plotly_chart(fig_humidity)
        
    if "sky" in df_filtered.columns:
        st.subheader("Sky Conditions")
        sky_counts = df_filtered["sky"].value_counts().reset_index()
        sky_counts.columns = ["sky", "count"]
        fig_sky = px.bar(sky_counts, x="sky", y="count", title="Sky Condition Distribution")
        st.plotly_chart(fig_sky)


    if "wind" in df_filtered.columns:
       st.subheader("Wind Conditions")
       wind_counts = df_filtered["wind"].value_counts().reset_index()
       wind_counts.columns = ["wind", "count"]
       fig_wind = px.bar(wind_counts, x="wind", y="count", title="Wind Condition Distribution")
       st.plotly_chart(fig_wind)

    if "disturbance" in df_filtered.columns:
       st.subheader("Disturbance Effects on Sightings")
       disturbance_counts = df_filtered["disturbance"].value_counts().reset_index()
       disturbance_counts.columns = ["Disturbance Level", "Count"]

       # Plot the bar chart
       fig_disturbance = px.bar(
       disturbance_counts,
       x="Disturbance Level",
       y="Count",
       title="Bird Observations by Disturbance Level",
       labels={"Count": "Number of Observations"}
    )
    st.plotly_chart(fig_disturbance)



# 5. Distance and Behavior
elif page == "Distance & Behavior":
    st.title("🛢️ Distance & Behavior")

    if "distance" in df_filtered.columns:
        st.subheader("Distance Distribution")
        fig_distance = px.histogram(df_filtered, x="distance", title="Bird Distance from Observer", nbins=25)
        st.plotly_chart(fig_distance)

    if "flyover_observed" in df_filtered.columns:
        st.subheader("Flyover Observations")
        df_filtered["flyover_label"] = df_filtered["flyover_observed"].map({
            True: "Flyover Observed", False: "No Flyover", None: "Unknown"
        }).fillna("Unknown")

        flyover_counts = df_filtered["flyover_label"].value_counts().reset_index()
        flyover_counts.columns = ["Flyover Status", "Count"]
        fig_flyover = px.bar(flyover_counts, x="Flyover Status", y="Count", title="Flyover Observation Frequency", color="Flyover Status")
        st.plotly_chart(fig_flyover)

# 6. Observer Trends
elif page == "Observer Trends":
    st.title("🧍 Observer Trends")

    if "observer" in df_filtered.columns:
        st.subheader("Observations by Observer")
        observer_counts = df_filtered["observer"].value_counts().reset_index()
        observer_counts.columns = ["Observer", "Count"]
        fig_obs = px.bar(observer_counts.head(20), x="Observer", y="Count", title="Top Observers")
        st.plotly_chart(fig_obs)

    if "visit" in df_filtered.columns:
        st.subheader("Visit Patterns")
        visit_species = df_filtered.groupby("visit")["scientific_name"].nunique().reset_index()
        visit_species.columns = ["Visit", "Unique Species"]
        fig_visit = px.line(visit_species, x="Visit", y="Unique Species", title="Species Count Over Visits")
        st.plotly_chart(fig_visit)

# 7. Conservation Insights
elif page == "Conservation Insights":
    st.title("🚨 Conservation Insights")

    if "pif_watchlist_status" in df_filtered.columns:
        st.subheader("PIF Watchlist Species")
        df_filtered["watchlist_label"] = df_filtered["pif_watchlist_status"].map({
            True: "Watchlist Species", False: "Non-Watchlist", None: "Unknown"
        }).fillna("Unknown")

        watchlist_counts = df_filtered["watchlist_label"].value_counts().reset_index()
        watchlist_counts.columns = ["Watchlist Status", "Count"]
        fig_watchlist = px.bar(watchlist_counts, x="Watchlist Status", y="Count", title="Birds by Watchlist Status", color="Watchlist Status")
        st.plotly_chart(fig_watchlist)

    if "regional_stewardship_status" in df_filtered.columns:
        st.subheader("Regional Stewardship Species")
        df_filtered["stewardship_label"] = df_filtered["regional_stewardship_status"].map({
            True: "Stewardship Species", False: "Non-Stewardship", None: "Unknown"
        }).fillna("Unknown")

        stewardship_counts = df_filtered["stewardship_label"].value_counts().reset_index()
        stewardship_counts.columns = ["Stewardship Status", "Count"]
        fig_stewardship = px.bar(stewardship_counts, x="Stewardship Status", y="Count", title="Birds by Stewardship Status", color="Stewardship Status")
        st.plotly_chart(fig_stewardship)

    if "aou_code" in df_filtered.columns:
        st.subheader("Species Count by AOU Code")
        aou_counts = df_filtered["aou_code"].value_counts().reset_index()
        aou_counts.columns = ["AOU Code", "Count"]
        fig_aou = px.bar(aou_counts.head(20), x="AOU Code", y="Count", title="Top 20 AOU Code Species", color="AOU Code")
        st.plotly_chart(fig_aou)

# 8. Other Insights
elif page == "Other Insights":
    st.title("📌 Other Insights")

    st.subheader("Seasonal Hotspots")
    if "season" in df_filtered.columns and "scientific_name" in df_filtered.columns:
        seasonal_hotspot = df_filtered.groupby(["season", "scientific_name"]).size().reset_index(name="count")
        fig_hot = px.scatter(seasonal_hotspot, x="season", y="scientific_name", size="count", color="season", title="Species Activity Across Seasons")
        st.plotly_chart(fig_hot)

    st.subheader("Environmental Influence on Behavior")
    if "temperature" in df_filtered.columns and "interval_length" in df_filtered.columns:
        df_behavior = df_filtered.dropna(subset=["temperature", "interval_length"])

        if df_behavior["temperature"].dropna().empty or df_behavior["interval_length"].dropna().empty:
            st.warning("Not enough valid data for plotting temperature vs activity length.")
        else:
            fig_env = px.scatter(
                df_behavior,
                x="temperature",
                y="interval_length",
                trendline="ols",
                title="Effect of Temperature on Activity Length"
            )
            st.plotly_chart(fig_env)

    st.subheader("Conservation Focus: Species at Risk")
    if "scientific_name" in df_filtered.columns and "pif_watchlist_status" in df_filtered.columns:
        risk_species = df_filtered[df_filtered["pif_watchlist_status"] == True]

        if not risk_species.empty:
            risk_counts = risk_species["scientific_name"].value_counts().reset_index()
            risk_counts.columns = ["Scientific Name", "Observations"]
            fig_risk = px.bar(risk_counts.head(10), x="Scientific Name", y="Observations",
                              color="Scientific Name", title="Top Watchlist Species")
            st.plotly_chart(fig_risk)
        else:
            st.warning("No PIF Watchlist species found in the selected data.")
