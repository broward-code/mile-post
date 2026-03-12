import streamlit as st
import geopandas as gpd
from io import BytesIO

st.title("Desktop Shapefile Translator")

uploaded_file = st.file_uploader("Upload ZIP containing your Shapefile", type=["zip"])

if uploaded_file is not None:
    try:
        # We wrap the uploaded bytes so GeoPandas can treat it like a file
        bytes_data = uploaded_file.getvalue()
        
        # The 'zip://' prefix tells geopandas to look inside the zip archive
        # We pass the bytes directly to read_file
        gdf = gpd.read_file(BytesIO(bytes_data), engine="pyogrio")
        
        if gdf.crs is not None:
            gdf = gdf.to_crs(epsg=4326)
            
        st.success(f"Loaded {len(gdf)} features!")
        st.write(gdf.head())

        # Download as GeoJSON
        geojson = gdf.to_json()
        st.download_button("Download GeoJSON", geojson, "data.geojson", "application/json")

    except Exception as e:
        st.error(f"Error: {e}")
