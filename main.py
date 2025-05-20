#imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

#set up our app
st.set_page_config(page_title="Data Sweeper", page_icon="🧊", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #e0f7fa;  /* Light cyan background */
            font-family: Arial, sans-serif;
        }
        .stButton>button {
            background-color: #00bcd4;  
            color: white;
            font-weight: bold;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #008c9e;  
        }
        .stCheckbox>label {
            color: #00796b;  
            font-size: 16px;
        }
        .stRadio>label {
            color: #ff5722;  
            font-size: 16px;
        }
        .stTextInput>label {
            color: #d32f2f;  
        }
        .stFileUploader {
            background-color: #c1e5e5;  
            border-radius: 10px;
            padding: 10px;
        }
        .stDataFrame {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stSubheader {
            color: #37474f;  
            font-weight: bold;
        }
        .stWrite {
            color: #333;
        }
        .stDownloadButton>button {
            background-color: #4caf50;  
            color: white;
            border-radius: 5px;
        }
        .stDownloadButton>button:hover {
            background-color: #388e3c;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"File type not supported: {file_ext}")
            continue

        # Display info about the file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Show 5 rows of the data
        st.write("Preview the head of the DataFrame")
        st.dataframe(df.head())

        # Option for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for file {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("<span style='color: green;'>Duplicates removed!</span>", unsafe_allow_html=True)
            with col2:
                if st.button(f"Fill Missing Values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("<span style='color: green;'>Missing values have been filled!</span>", unsafe_allow_html=True)

        # Choose specific columns to display
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create some visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=["number"]))

        # Convert the file -> CSV to Excel
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download button
            st.download_button(
                label=f"Click here to download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
            )
            st.markdown("<span style='color: green;'>All files processed successfull</span>", unsafe_allow_html=True)