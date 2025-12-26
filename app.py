import streamlit as st
from pyproj import Transformer

# EPSG:2039 (ITM) and EPSG:4326 (WGS84)
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
            
            # --- DETECTION & CONVERSION ---
            if 28 < val1 < 36:  # GPS Input (Lat, Lon)
                lat, lon = val1, val2
                itm_x, itm_y = to_itm.transform(lon, lat)
            else:              # ITM Input (E, N)
                itm_x, itm_y = val1, val2
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # --- DISPLAY RESULTS ---
            st.subheader("📋 Results")
            st.code(f"GPS: {lat:.6f}, {lon:.6f}")
            st.code(f"ITM: {int(itm_x)}, {int(itm_y)}")

            # --- OPTIMIZED MAP LINKS ---
            st.divider()
            c1, c2 = st.columns(2)
            
            with c1:
                # Israel Hiking: Needs /#/?marker=LAT,LON format
                st.link_button("🇮🇱 Israel Hiking Map", f"https://israelhiking.osm.org.il/#/?marker={lat},{lon}&zoom=15")
                
                # Amud Anan: Added marker=1 to highlight the point
                st.link_button("☁️ Amud Anan", f"https://amudanan.co.il/?lon={lon}&lat={lat}&marker=1")
            
            with c2:
                # GovMap: Uses 'c' for coordinates in ITM East,North format
                st.link_button("🌐 GovMap Israel", f"https://www.govmap.gov.il/?c={int(itm_x)},{int(itm_y)}&z=10")
                
                # Waze: Universal format
                st.link_button("🚗 Waze", f"https://waze.com/ul?ll={lat},{lon}&navigate=yes")
                
    except:
        st.error("Invalid input. Please use numbers only.")

st.caption("MemirHaHaV1 | Marker Sync Fixed")
