import streamlit as st
from pyproj import Transformer
import pandas as pd

# הגדרת התמרות
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍", layout="wide")
st.title("📍 MemirHaHaV1 - Final Mission")

user_input = st.text_input("הדבק קואורדינטות (WGS84 או ITM):", placeholder="31.28392, 34.67544")

if user_input:
    try:
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(parts) == 2:
            v1, v2 = parts
            # לוגיקת Swap חכמה
            if 25 < v1 < 40 or 25 < v2 < 40:
                lat = v1 if 28 < v1 < 35 else v2
                lon = v2 if lat == v1 else v1
            else:
                itm_x = v1 if v1 < 450000 else v2
                itm_y = v2 if itm_x == v1 else v1
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # תצוגה פנימית
            st.success(f"TARGET: {lat:.6f}, {lon:.6f}")
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=14)

            st.divider()

            # --- הקישורים שעובדים ב-PC (בדיקה ידנית) ---

            # 1. Israel Hiking Map - הפתרון ל-PC: שימוש בפרמטר /points/ בתוך ה-Path
            # זה יוצר שכבה זמנית עם סיכה כחולה
            ihm_url = f"https://israelhiking.osm.org.il/map/16/{lat}/{lon}/points/{lat}/{lon}"

            # 2. Caltopo - הפתרון ל-PC: שימוש ב-Search עם Marker מוצמד
            cal_url = f"https://caltopo.com/search?q={lat},{lon}"

            # 3. Amud Anan - p= (תמיד עובד)
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"
            
            # 4. Google Maps - עם Marker אדום (הפורמט הרשמי)
            gm_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            # 5. Govmap - רשת ישראל הרשמית
            gov_url = f"https://www.govmap.gov.il/?q={lat},{lon}&z=10"

            st.write("### 🚀 קליק אחד לסיכה:")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.link_button("🥾 IHM", ihm_url, use_container_width=True)
            c2.link_button("🏔️ Caltopo", cal_url, use_container_width=True)
            c3.link_button("☁️ עמוד ענן", aa_url, use_container_width=True)
            c4.link_button("🌐 Google", gm_url, use_container_width=True)
            c5.link_button("🇮🇱 GovMap", gov_url, use_container_width=True)

    except:
        st.error("Error")

st.caption("MemirHaHaV1 | PC Compatible | Zero-Step Markers")
