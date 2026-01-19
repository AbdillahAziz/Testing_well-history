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

st.markdown("""
<style>
/* Download button animation */
div.stDownloadButton > button {
    background-color: #2E7D32;
    color: white;
    padding: 0.6em 1.4em;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    animation: pulse 2s infinite;
    transition: transform 0.2s ease-in-out;
}

/* Hover effect */
div.stDownloadButton > button:hover {
    background-color: #1B5E20;
    transform: scale(1.05);
    animation: none;
}

/* Pulse animation */
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(46, 125, 50, 0.6); }
    70% { box-shadow: 0 0 0 10px rgba(46, 125, 50, 0); }
    100% { box-shadow: 0 0 0 0 rgba(46, 125, 50, 0); }
}
</style>
""", unsafe_allow_html=True)

st.title("Well History Data Compilation")
if os.path.exists('Logo PGE Panjang 1.jpg'):
    st.image('Logo PGE Panjang 1.jpg')
st.write("""This page contain the compilation of well history data from various wells in the area. You can filter the data based on Area, Cluster, and Well Name using the sidebar options.""")
#>>>>>>>>>>>> title <<<<<<<<<<<<#

#>>>>>>>>>>>> sidebar <<<<<<<<<<<<#
if os.path.exists('Logo PGE.png'):
    st.sidebar.image(Image.open('Logo PGE.png'))

st.sidebar.title("Pengaturan")
st.sidebar.subheader("Pengaturan konfigurasi tampilan")

#Test

#>>>>>>>>>>>> Load Data <<<<<<<<<<<<#
# Load Excel
folder_path = 'data/Well History'

def load_data(folder_path):
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

            df = df[['Well Name', 'Cluster', 'Unit', 'Area', 'Date', 'Type', 'Remarks']]
            df_list.append(df)

    return pd.concat(df_list, ignore_index=True)

final_df = load_data(folder_path)

# Allignment of Date column so it would be "dd Month yyyy"
final_df['Date_dt'] = pd.to_datetime(final_df['Date'], errors='coerce')
final_df['Date'] = final_df['Date_dt'].dt.strftime('%d %B %Y')

# Filter data for sidebar options
areas = final_df['Area'].unique().tolist()
clusters = final_df['Cluster'].unique().tolist()
well_names = final_df['Well Name'].unique().tolist()
types = final_df['Type'].dropna().unique().tolist()

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

# Removing the temporary Date_dt column
filtered_df = filtered_df.drop(columns=['Date_dt'])

#>>>>>>>>>>>> Showing Data <<<<<<<<<<<<#
st.dataframe(filtered_df)

# Option to download the filtered data as Excel
def convert_df_to_excel(df):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output) as writer:
        df.to_excel(writer, index=False, sheet_name='Filtered Data')
        
    processed_data = output.getvalue()
    return processed_data

excel_data = convert_df_to_excel(filtered_df)

st.markdown("### 📤 Export Filtered Well History Data")

clicked = st.download_button(
    label="📥 Download Excel",
    data=excel_data,
    file_name="filtered_well_history_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

if clicked:
    st.success("✅ Download started successfully!")

st.caption(
    f"📄 {len(filtered_df)} rows exported | "
    f"🕒 Generated on {pd.Timestamp.now().strftime('%d %B %Y %H:%M')}"
)