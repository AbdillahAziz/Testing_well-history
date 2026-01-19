import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import json as js
from matplotlib import cm
import streamlit as st
from PIL import Image
import os

#>>>>>>>>>>>> title <<<<<<<<<<<<#
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Well History Data Compilation")
st.image('Logo PGE Panjang.jpg')
st.write("""This page contain the compilation of well history data from various wells in the area. You can filter the data based on Area, Cluster, and Well Name using the sidebar options.""")
#>>>>>>>>>>>> title <<<<<<<<<<<<#

#>>>>>>>>>>>> sidebar <<<<<<<<<<<<#
gambar = Image.open('Logo PGE.png')
st.sidebar.image(gambar)

st.sidebar.title("Pengaturan")
st.sidebar.subheader("Pengaturan konfigurasi tampilan")

#Test

#>>>>>>>>>>>> Load Data <<<<<<<<<<<<#
# Load Excel
folder_path = 'data/Well History'

df_list = []

for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)
        df_raw = pd.read_excel(file_path, header=None)

        well_name = df_raw.iloc[0, 1]
        cluster = df_raw.iloc[1, 1]
        unit = df_raw.iloc[2, 1]
        area = df_raw.iloc[3, 1]

        df = df_raw.iloc[6:].reset_index(drop=True)
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)

        df["Well Name"] = well_name
        df["Cluster"] = cluster
        df["Unit"] = unit
        df["Area"] = area

        df = df[['Well Name', 'Cluster', 'Unit', 'Area','Date','Type','Remarks']]

        df_list.append(df)

final_df = pd.concat(df_list, ignore_index=True)

# Allignment of Date column so it would be "dd Month yyyy"
final_df['Date'] = pd.to_datetime(final_df['Date'], errors='coerce').dt.strftime('%d %B %Y')

# Filter data for sidebar options
areas = final_df['Area'].unique().tolist()
clusters = final_df['Cluster'].unique().tolist()
well_names = final_df['Well Name'].unique().tolist()
types = final_df['Type'].unique().tolist()

# Sidebar options for filtering
selected_area = st.sidebar.multiselect("Select Area", options=areas, default=areas)
selected_cluster = st.sidebar.multiselect("Select Cluster", options=clusters, default=clusters)
selected_well_name = st.sidebar.multiselect("Select Well Name", options=well_names, default=well_names)
selected_type = st.sidebar.multiselect("Select Type", options=types, default=types)

# Apply filters to the DataFrame
filtered_df = final_df[
    (final_df['Area'].isin(selected_area)) &
    (final_df['Cluster'].isin(selected_cluster)) &
    (final_df['Well Name'].isin(selected_well_name)) &
    (final_df['Type'].isin(selected_type))
]

#>>>>>>>>>>>> Showing Data <<<<<<<<<<<<#
st.dataframe(filtered_df)

