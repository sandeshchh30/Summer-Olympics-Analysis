import pandas as pd
import streamlit as st

@st.cache_data
def data_preprocessing(df):
    df = df[df['Season'] == 'Summer'].copy()
    df = df.drop_duplicates()

    region_df = pd.read_csv('Data/noc_regions.csv')
    df = df.merge(region_df, on='NOC', how='left')

    df = df[df['Year'] != 1906].copy()

    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)
    df['Total'] = df['Gold'] + df['Silver'] + df['Bronze']

    return df
