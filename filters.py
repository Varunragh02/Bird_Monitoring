import streamlit as st
import pandas as pd

def apply_filters(df):
    st.sidebar.title("🔍 Filters")

    if "date" in df.columns:
        start = st.sidebar.date_input("Start Date", df["date"].min())
        end = st.sidebar.date_input("End Date", df["date"].max())
        df = df[(df["date"] >= pd.to_datetime(start)) & (df["date"] <= pd.to_datetime(end))]

    if "taxoncode" in df.columns:
        species = st.sidebar.multiselect("Species", df["taxoncode"].dropna().unique())
        if species:
            df = df[df["taxoncode"].isin(species)]

    if "observer" in df.columns:
        observers = st.sidebar.multiselect("Observer", df["observer"].dropna().unique())
        if observers:
            df = df[df["observer"].isin(observers)]

    return df
