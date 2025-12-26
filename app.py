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
                input_label = "WGS84 (GPS)"
            else:
                itm_x, itm_y = val1, val2
                lon, lat = to_wgs.transform(itm_x, itm_y)
                input_label = "ITM (Israel New Grid)"

            # Uniform Presentation
            st.info(f"Input: **{input_label}**")
            
            st.subheader("📋 Uniform Results")
            c_a, c_b = st.columns(2)
            with c_a:
                st.markdown("**GPS (Lat, Lon)**")
                st.code(f"{lat:.6f}, {lon:.6f}")
            with c_b:
                st.markdown("**ITM (E, N)**")
                st.code(f"{int(itm_x)}, {int(itm_y)}")

            st.divider()
            st.write("### 🗺️ Map Links (with Markers)")
            
            # --- THE NEW LINK ENGINE ---
            
            # CALTOPO: 'll' for lat/lon, 'z' for zoom, 'marker' for the pin
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=15&marker={lat},{lon}"
            
            # AMUD ANAN: Marker 1 must be present for the blue pin
            aa_url = f"https://amudanan.co.il/?marker=1&lon={lon}&lat={lat}"
            
            # GOVMAP: Using 'q' (Query) to force the red search marker
            gm_url = f"https://www.govmap.gov.il/?q={int(itm_x)},{int(itm_y)}&z=10"
            
            # WAZE: Reliable navigation pin
            wz_url = f"https://waze.com/ul?ll={lat},{lon}&navigate=yes"

            col1, col2 = st.columns(2)
            with col1:
                st.link_button("🏔️ Caltopo", cal_url, use_container_width=True)
                st.link_button("☁️ Amud Anan", aa_url, use_container_width=True)
            with col2:
                st.link_button("🌐 GovMap Israel", gm_url, use_container_width=True)
                st.link_button("🚗 Waze", wz_url, use_container_width=True)
                
    except:
        st.error("Invalid input. Please enter numbers only.")

st.caption("MemirHaHaV1 | Caltopo + Grid Sync")
