import streamlit as st
from pyproj import Transformer

# Professional coordinate transformation
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
            is_gps = 28 < val1 < 36
            
            if is_gps:
                lat, lon = val1, val2
                itm_x, itm_y = to_itm.transform(lon, lat)
                grid_name = "WGS84 (GPS)"
            else:
                itm_x, itm_y = val1, val2
                lon, lat = to_wgs.transform(itm_x, itm_y)
                grid_name = "ITM (Israel New Grid)"

            # Uniform Display
            st.info(f"Input Detected: **{grid_name}**")
            
            st.subheader("📋 Uniform Results")
            c_a, c_b = st.columns(2)
            with c_a:
                st.markdown("**GPS (Lat, Lon)**")
                st.code(f"{lat:.6f}, {lon:.6f}")
            with c_b:
                st.markdown("**ITM (E, N)**")
                st.code(f"{int(itm_x)}, {int(itm_y)}")

            st.divider()
            st.write("### 🗺️ Open Maps")
            
            # --- THE "FORCE" PARAMETERS ---
            # Caltopo: 'point' creates a temporary red dot that is harder to ignore than 'marker'
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=15&point={lat},{lon}"
            
            # Amud Anan: The 'p' parameter is the official "shared point" trigger
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"
            
            # Waze: Always works with markers
            wz_url = f"https://waze.com/ul?ll={lat},{lon}&navigate=yes"

            col1, col2, col3 = st.columns(3)
            with col1:
                st.link_button("🏔️ Caltopo", cal_url, use_container_width=True)
            with col2:
                st.link_button("☁️ Amud Anan", aa_url, use_container_width=True)
            with col3:
                st.link_button("🚗 Waze", wz_url, use_container_width=True)
                
    except:
        st.error("Invalid input. Please enter numbers only.")

st.caption("MemirHaHaV1 | Marker Sync Engine")
