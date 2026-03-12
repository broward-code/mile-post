import streamlit as st
import geopandas as gpd
from shapely.ops import nearest_points
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mile Post Locator", layout="wide")

# 1. Load Data (Cached for performance)
@st.cache_data
def load_data():
    # Loading from your uploaded shapefiles
    roads = gpd.read_file("data/roadways.shp").to_crs(epsg=4326)
    mps = gpd.read_file("data/mileposts.shp").to_crs(epsg=4326)
    return roads, mps

roads, mps = load_data()

st.title("Florida Roadway Mile Post Finder")

# 2. Get User Location (Simulation or Text Input for now)
# Note: Streamlit doesn't have a native 'GPS' button yet, 
# so we use a map click or coordinate input.
st.sidebar.header("Your Location")
lat = st.sidebar.number_input("Latitude", value=26.1224) # Default Ft. Lauderdale
lon = st.sidebar.number_input("Longitude", value=-80.1373)

user_point = gpd.points_from_xy([lon], [lat])[0]

# 3. Calculation Logic
if st.button("Find Nearest Mile Post"):
    # Calculate distance to all points
    mps['dist'] = mps.geometry.distance(user_point)
    nearest_mp = mps.loc[mps['dist'].idxmin()]
    
    st.success(f"Closest Mile Post: **{nearest_mp['MP_VALUE']}**")
    st.info(f"Roadway ID: {nearest_mp['ROAD_ID']}")

# 4. Visualization
m = folium.Map(location=[lat, lon], zoom_start=15)
folium.Marker([lat, lon], tooltip="You are here", icon=folium.Icon(color='red')).add_to(m)

# Add nearest mile post to map
st_folium(m, width=700)