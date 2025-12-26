import streamlit as st
from pyproj import Transformer

# EPSG:2039 (ITM) and EPSG:4326 (WGS84)
# always_xy=True means we consistently use (Longitude, Latitude) order for math
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍")
st.title("📍 MemirHaHaV1")

user_input = st.text_input("Paste Coordinates:", placeholder="31.77, 35.21 or 222000, 631000")

if user_input:
    try:
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(parts) == 2:
            val1, val2 = parts
            
            # --- Detection Logic ---
            if 28 < val1 < 36:  # User entered GPS (Lat, Lon)
                lat, lon = val1, val2
                itm_x, itm_y = to_itm.transform(lon, lat)
            else:              # User entered ITM (X, Y)
                itm_x, itm_y = val1, val2
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # --- Results ---
            st.subheader("📋 Results (Click & Copy)")
            st.text_input("WGS84 (GPS)", f"{lat:.6f}, {lon:.6f}")
            st.text_input("ITM (New Grid)", f"{int(itm_x)}, {int(itm_y)}")

            # --- Map Links with Markers ---
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("🇮🇱 Israel Hiking Map", f"https://israelhiking.osm.org.il/#/?center={lon},{lat}&zoom=15&marker={lat},{lon}")
                st.link_button("☁️ Amud Anan", f"https://amudanan.co.il/?lon={lon}&lat={lat}")
            with c2:
                st.link_button("🌐 GovMap Israel", f"https://www.govmap.gov.il/?q={int(itm_x)},{int(itm_y)}&z=10")
                st.link_button("🚗 Waze", f"https://waze.com/ul?ll={lat},{lon}&navigate=yes")
    except:
        st.error("Please enter two numbers.")
