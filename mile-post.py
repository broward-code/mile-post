import streamlit as st
import geopandas as gpd
import zipfile
from io import BytesIO

st.title("Florida Roadway Translator")

uploaded_file = st.file_uploader("Upload ZIP (containing .shp, .shx, .dbf, .prj)", type=["zip"])

if uploaded_file is not None:
    try:
        # 1. Open the zip in memory to find the .shp filename
        with zipfile.ZipFile(uploaded_file) as z:
            # Look for the filename ending in .shp
            shp_filenames = [f for f in z.namelist() if f.endswith('.shp')]
            
            if not shp_filenames:
                st.error("Could not find a .shp file inside the ZIP.")
            else:
                # 2. Pick the first .shp found
                target_shp = shp_filenames[0]
                
                # 3. Use the 'zip://' prefix with the uploaded file 
                # and point it specifically to the internal .shp
                # We reset the pointer to the start of the uploaded file first
                uploaded_file.seek(0)
                gdf = gpd.read_file(uploaded_file, engine="pyogrio", layer=target_shp.replace('.shp', ''))

                # 4. Standardize to Lat/Long
                if gdf.crs is not None:
                    gdf = gdf.to_crs(epsg=4326)
                    st.success(f"Successfully translated {target_shp}")
                
                st.write("Data Preview:", gdf.head())

                # 5. Download Button
                geojson = gdf.to_json()
                st.download_button("Download GeoJSON", geojson, "roadway_data.geojson", "application/json")

    except Exception as e:
        st.error(f"Error: {e}")
