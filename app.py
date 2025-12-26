import streamlit as st
from pyproj import Transformer

# EPSG:2039 (ITM) and EPSG:4326 (WGS84)
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍")
st.title("📍 MemirHaHaV1")

user_input = st.text_input("Paste Coordinates:", placeholder="31.7, 35.2 or 210000, 650000")

if user_input:
    try:
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(parts) == 2:
            val1, val2 = parts
            
            # 1. IDENTIFY INPUT (GPS is ~30-35, ITM is ~100k-800k)
            is_gps = 28 < val1 < 36
            input_label = "WGS84 (GPS)" if is_gps else "ITM (Israel New Grid)"
            
            # 2. CALCULATE BOTH GRIDS
            if is_gps:
                lat, lon = val1, val2
                itm_x, itm_y = to_itm.transform(lon, lat)
            else:
                itm_x, itm_y = val1, val2
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # 3. UNIFORM DISPLAY (Always looks the same)
            st.info(f"Input Detected: **{input_label}**")
            
            st.subheader("📋 Final Coordinates")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**WGS84 (GPS)**")
                st.code(f"{lat:.6f}, {lon:.6f}")
            with col_b:
                st.markdown("**ITM (New Grid)**")
                st.code(f"{int(itm_x)}, {int(itm_y)}")

            # 4. MARKER-FORCED LINKS
            st.divider()
            st.write("### 🗺️ Open Maps with Markers")
            
            # Israel Hiking: Needs marker in the hash path
            ihm = f"https://israelhiking.osm.org.il/#/?center={lon},{lat}&zoom=15&marker={lat},{lon}"
            
            # Amud Anan: marker=1 is the force-pin flag
            aa = f"https://amudanan.co.il/?lon={lon}&lat={lat}&marker=1"
            
            # GovMap: 'q' triggers the search marker, 'c' centers the camera
            gm = f"https://www.govmap.gov.il/?c={int(itm_x)},{int(itm_y)}&q={int(itm_x)},{int(itm_y)}&z=10"
            
            # Waze: Standard reliable pin
            wz = f"https://waze.com/ul?ll={lat},{lon}&navigate=yes"

            c1, c2 = st.columns(2)
            with c1:
                st.link_button("🇮🇱 Israel Hiking Map", ihm, use_container_width=True)
                st.link_button("☁️ Amud Anan", aa, use_container_width=True)
            with c2:
                st.link_button("🌐 GovMap Israel", gm, use_container_width=True)
                st.link_button("🚗 Waze", wz, use_container_width=True)
                
    except:
        st.error("Invalid numbers. Please try again.")
