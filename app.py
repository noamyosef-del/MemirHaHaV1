import streamlit as st
from pyproj import Transformer
import pandas as pd

# התמרת קואורדינטות
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍", layout="centered")

st.title("📍 MemirHaHaV1 - Pro")

user_input = st.text_input("הדבק קואורדינטות (GPS או רשת ישראל):", placeholder="31.28392, 34.67544")

if user_input:
    try:
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(parts) == 2:
            v1, v2 = parts
            # לוגיקת Swap חכמה
            if 25 < v1 < 40 or 25 < v2 < 40:
                lat, lon = (v1, v2) if v1 < v2 else (v2, v1)
            else:
                itm_x, itm_y = (v1, v2) if v1 < v2 else (v2, v1)
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # --- מנוע העתקה אוטומטי ---
            st.markdown("### 📋 שלב 1: העתק לסיכה בטוחה")
            search_string = f"{lat:.6f}, {lon:.6f}"
            st.code(search_string)
            st.caption("לחץ על האייקון מימין למעלה כדי להעתיק. לאחר מכן הדבק בחיפוש באתר המפה.")

            st.divider()

            # --- שלב 2: פתיחת אתרים ---
            st.markdown("### 🚀 שלב 2: פתח מפה")
            
            # בניית קישורים
            ihm_url = f"https://israelhiking.osm.org.il/map/16/{lat}/{lon}"
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=16"
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"
            gm_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            wz_url = f"https://waze.com/ul?ll={lat},{lon}&navigate=yes"

            col1, col2, col3 = st.columns(3)
            with col1:
                st.link_button("🥾 Israel Hiking", ihm_url, use_container_width=True)
            with col2:
                st.link_button("🏔️ Caltopo", cal_url, use_container_width=True)
            with col3:
                st.link_button("☁️ עמוד ענן", aa_url, use_container_width=True)
            
            st.write("") # מרווח
            
            col4, col5 = st.columns(2)
            with col4:
                st.link_button("🌐 Google (סיכה מובנית)", gm_url, use_container_width=True)
            with col5:
                st.link_button("🚗 Waze (סיכה מובנית)", wz_url, use_container_width=True)

            # תצוגה פנימית לווידוא
            st.divider()
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=14)

    except:
        st.error("Error")

st.caption("MemirHaHaV1 | Operational Protocol: Copy -> Open -> Paste")
