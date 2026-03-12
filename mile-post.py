import streamlit as st
import geopandas as gpd
import tempfile
import os

st.title("Florida Roadway Translator")

uploaded_file = st.file_uploader("Upload ZIP (containing .shp, .shx, .dbf, .prj)", type=["zip"])

if uploaded_file is not None:
    try:
        # 1. Create a temporary file to hold the uploaded ZIP
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        # 2. Use Geopandas to read the temporary file
        # The 'zip://' prefix is the standard way to read zipped shapes
        gdf = gpd.read_file(f"zip://{tmp_path}")

        # 3. Clean up: Delete the temporary file now that it's in memory
        os.remove(tmp_path)

        # 4. Standardize to Lat/Long (WGS84)
        if gdf.crs is not None:
            gdf = gdf.to_crs(epsg=4326)
            st.success("Successfully loaded and translated data!")
        
        # Display Audit Info
        st.write(f"**Feature Count:** {len(gdf)}")
        st.write("**Attribute Preview:**", gdf.head())

        # 5. Export for Mappy App
        geojson = gdf.to_json()
        st.download_button(
            label="Download GeoJSON",
            data=geojson,
            file_name="translated_roadway.geojson",
            mime="application/json"
        )

    except Exception as e:
        st.error(f"Translation Error: {e}")
