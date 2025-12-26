import streamlit as st
from pyproj import Transformer

# ITM (2039) to WGS84 (4326)
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
            
            # --- DETECTION ---
            if 28 < val1 < 36:  # GPS Input
                lat, lon = val1, val2
                itm_x, itm_y = to_itm.transform(lon, lat)
            else:              # ITM Input
                itm_x, itm_y = val1, val2
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # --- DISPLAY ---
            st.subheader("📋 Results")
            st.code(f"GPS: {lat:.6f}, {lon:.6f}")
            st.code(f"ITM: {int(itm_x)}, {int(itm_y)}")

            # --- THE SYNCED MAP LINKS ---
            st.divider()
            c1, c2 = st.columns(2)
            
            with c1:
                # FIX: Israel Hiking Map 2025 (Marker needs to be first in the hash)
                st.link_button("🇮🇱 Israel Hiking Map", f"https://israelhiking.osm.org.il/#/?marker={lat},{lon}")
                
                # FIX: Amud Anan (Needs marker=1 AND specific lon/lat)
                st.link_button("☁️ Amud Anan", f"https://amudanan.co.il/?lon={lon}&lat={lat}&marker=1")
            
            with c2:
                # FIX: GovMap (Needs both 'c' for center and 'q' for a search marker)
                st.link_button("🌐 GovMap Israel", f"https://www.govmap.gov.il/?c={int(itm_x)},{int(itm_y)}&q={int(itm_x)},{int(itm_y)}&z=10")
                
                # Waze (Reliable)
                st.link_button("🚗 Waze", f"https://waze.com/ul?ll={lat},{lon}&navigate=yes")
                
    except:
        st.error("Invalid input. Please use numbers only.")

st.caption("MemirHaHaV1 | Fixed Marker Sync 2025")
