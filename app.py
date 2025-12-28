import streamlit as st
from pyproj import Transformer
import pandas as pd

# הגדרת התמרות קואורדינטות
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍")
st.title("📍 MemirHaHaV1")

user_input = st.text_input("הדבק קואורדינטות (GPS או ITM):", placeholder="למשל: 31.28, 34.67")

if user_input:
    try:
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(parts) == 2:
            v1, v2 = parts
            
            # לוגיקה חכמה לזיהוי והחלפת סדר (Auto-Swap)
            if 25 < v1 < 40 or 25 < v2 < 40:  # זיהוי GPS (ישראל בין 29 ל-33 מעלות רוחב)
                grid_name = "WGS84 (GPS)"
                lat = v1 if 28 < v1 < 35 else v2
                lon = v2 if lat == v1 else v1
                itm_x, itm_y = to_itm.transform(lon, lat)
            else:  # זיהוי רשת ישראל (ITM)
                grid_name = "ITM (Israel New Grid)"
                itm_x = v1 if v1 < 400000 else v2
                itm_y = v2 if itm_x == v1 else v1
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # הצגת הנתונים
            st.success(f"זיהוי: **{grid_name}**")
            col_res1, col_res2 = st.columns(2)
            col_res1.metric("GPS (Lat, Lon)", f"{lat:.6f}, {lon:.6f}")
            col_res2.metric("ITM (E, N)", f"{int(itm_x)}, {int(itm_y)}")

            # --- מפה מובנית (Preview) ---
            st.write("### 🗺️ תצוגה מהירה")
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=14)

            st.divider()
            
            # --- בניית קישורים עם סימון מיקום (Markers) ---
            # IHM עם פרמטר marker
            ihm_url = f"https://israelhiking.osm.org.il/map/{lat}/{lon}?marker={lat},{lon}"
            # Caltopo עם פרמטר markers
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=15&markers={lat},{lon}"
            # Amud Anan עם פרמטר p
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"
            # Waze
            wz_url = f"https://waze.com/ul?ll={lat},{lon}&navigate=yes"

            st.write("### 🚀 פתח באפליקציות (עם סיכה)")
            c1, c2, c3, c4 = st.columns(4)
            c1.link_button("🥾 IHM", ihm_url, use_container_width=True)
            c2.link_button("🏔️ Caltopo", cal_url, use_container_width=True)
            c3.link_button("☁️ עמוד ענן", aa_url, use_container_width=True)
            c4.link_button("🚗 Waze", wz_url, use_container_width=True)

    except Exception as e:
        st.error("שגיאה: וודא שהזנת מספרים בלבד המייצגים קואורדינטות בישראל.")

st.caption("MemirHaHaV1 | Fixed Marker URLs for IHM & Caltopo")
