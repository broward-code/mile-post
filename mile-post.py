import streamlit as st
import geopandas as gpd
import fiona
from io import BytesIO
import zipfile

st.title("Desktop Shapefile Translator")

# 1. File Uploader Widget
uploaded_file = st.file_uploader("Upload Roadway/Milepost Data (ZIP format)", type=["zip"])

if uploaded_file is not None:
    try:
        # 2. Read the ZIP file into memory
        with zipfile.ZipFile(uploaded_file) as z:
            # Find the .shp file inside the zip
            shp_files = [f for f in z.namelist() if f.endswith('.shp')]
            
            if not shp_files:
                st.error("No .shp file found in the ZIP!")
            else:
                # 3. Load with Geopandas using the 'zip://' virtual filesystem
                # We wrap the uploaded bytes in a way Geopandas can read
                with fiona.BytesCollection(uploaded_file.read()) as f:
                    gdf = gpd.GeoDataFrame.from_features(f, crs=f.crs)
                
                # 4. Standardize to WGS84 (Web Standard)
                if gdf.crs != "EPSG:4326":
                    gdf = gdf.to_crs(epsg=4326)
                
                st.success(f"Successfully loaded {len(gdf)} features!")
                
                # Display data preview
                st.write("Data Preview:", gdf.head())

                # 5. Download Button (Translate to GeoJSON for your app)
                geojson = gdf.to_json()
                st.download_button(
                    label="Download as GeoJSON",
                    data=geojson,
                    file_name="translated_data.geojson",
                    mime="application/json"
                )

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please zip your .shp, .shx, .dbf, and .prj files together and upload them.")
