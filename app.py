import streamlit as st
from pyproj import Transformer
import pandas as pd

# הגדרת המרות קואורדינטות
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍", layout="wide")
st.title("📍 MemirHaHaV1 - PC Optimized")

user_input = st.text_input("הדבק קואורדינטות (WGS84 או ITM):", placeholder="31.28392, 34.67544")

if user_input:
    try:
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(parts) == 2:
            v1, v2 = parts
            
            # לוגיקת Auto-Swap משופרת לישראל
            if 25 < v1 < 40 or 25 < v2 < 40:
                lat = v1 if 28 < v1 < 35 else v2
                lon = v2 if lat == v1 else v1
                itm_x, itm_y = to_itm.transform(lon, lat)
            else:
                itm_x = v1 if v1 < 450000 else v2
                itm_y = v2 if itm_x == v1 else v1
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # תצוגה
            st.success(f"מיקום מזוהה: {lat:.6f}, {lon:.6f}")
            
            # מפה פנימית לווידוא
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=14)

            st.divider()

            # --- בניית הקישורים המנצחים ל-PC ---

            # 1. Israel Hiking Map - הפורמט הרשמי לנקודה משותפת (Share)
            # מבנה: /share/Point/lat/lon/Name
            ihm_url = f"https://israelhiking.osm.org.il/share/Point/{lat}/{lon}/Point"

            # 2. Caltopo - שימוש ב-points במקום marker (יותר אמין בדסקטופ)
            # זה יוצר נקודה אדומה עם תווית "Target"
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=16&points={lat},{lon},Target"

            # 3. Amud Anan - p= (עובד מצוין ב-PC)
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"

            # 4. Google Maps - עם נעץ אדום מובנה
            gm_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            st.write("### 🚀 קישורים עם סיכה (נבדק ב-Windows):")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.link_button("🥾 Israel Hiking", ihm_url, use_container_width=True)
            with c2:
                st.link_button("🏔️ Caltopo", cal_url, use_container_width=True)
            with c3:
                st.link_button("☁️ עמוד ענן", aa_url, use_container_width=True)
            with c4:
                st.link_button("🌐 Google Maps", gm_url, use_container_width=True)

    except Exception as e:
        st.error(f"שגיאה בעיבוד הקלט: {e}")

st.caption("MemirHaHaV1 | PC & Desktop Logic | Marker Injection Fix")
