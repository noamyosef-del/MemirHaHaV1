import streamlit as st
from pyproj import Transformer

# EPSG:2039 is Israel Transverse Mercator (ITM)
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍")

# --- OFFSHORE LIMIT LOGIC ---
# Standard Israel Boundaries + 10km Buffer
ISRAEL_BOUNDS = {
    "lat_min": 29.48, # Near Eilat
    "lat_max": 33.35, # Hermon / North
    "lon_min": 34.15, # ~10km West of shore
    "lon_max": 35.92  # Golan / East
}

st.title("📍 MemirHaHaV1")
user_input = st.text_input("Paste Coordinates:", placeholder="32.123 34.856")

if user_input:
    try:
        nums = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(nums) == 2:
            val1, val2 = nums
            
            # Identify and convert
            if 28 < val1 < 36: # WGS84
                lat, lon = val1, val2
                itm_x, itm_y = to_itm.transform(lon, lat)
            else: # ITM
                itm_x, itm_y = val1, val2
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # --- CHECK 10KM OFFSHORE LIMIT ---
            if not (ISRAEL_BOUNDS["lat_min"] <= lat <= ISRAEL_BOUNDS["lat_max"] and 
                    ISRAEL_BOUNDS["lon_min"] <= lon <= ISRAEL_BOUNDS["lon_max"]):
                st.error("❌ Out of Bounds: Coordinates are more than 10km from Israel/WB borders.")
            else:
                # Swapped Detection
                if lat > 36 or lon < 20: 
                    st.warning("🔄 Swap detected? Check X/Y order.")

                # Results
                st.subheader("📋 Results (Click to Copy)")
                st.text_input("WGS84", f"{lat:.6f}, {lon:.6f}")
                st.text_input("ITM (New)", f"{int(itm_x)}, {int(itm_y)}")

                # Map Links
                st.divider()
                col1, col2 = st.columns(2)
                with col1:
                    st.link_button("🇮🇱 Israel Hiking Map", f"https://israelhiking.osm.org.il/#/?center={lon},{lat}&zoom=15")
                    st.link_button("☁️ Amud Anan", f"https://amudanan.co.il/?lon={lon}&lat={lat}")
                with col2:
                    st.link_button("🌐 GovMap Israel", f"https://www.govmap.gov.il/?q={lat},{lon}&z=10")
                    st.link_button("🚗 Waze", f"https://waze.com/ul?ll={lat},{lon}&navigate=yes")

    except:
        st.error("Invalid input.")
