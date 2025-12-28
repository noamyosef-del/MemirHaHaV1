import streamlit as st
from pyproj import Transformer
import pandas as pd

# התמרת קואורדינטות - רשת ישראל החדשה ל-WGS84 ולהפך
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍", layout="wide")

st.title("📍 MemirHaHaV1")
st.markdown("### מערכת המרה וסנכרון מפות (גרסת מומחים יציבה)")

user_input = st.text_input("הדבק קואורדינטות (GPS או רשת ישראל):", placeholder="למשל: 31.28392, 34.67544")

if user_input:
    try:
        # ניקוי ופירוק הקלט
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        
        if len(parts) == 2:
            v1, v2 = parts
            
            # לוגיקת זיהוי והחלפה אוטומטית (Swap)
            if 25 < v1 < 40 or 25 < v2 < 40:
                # GPS (WGS84)
                lat = v1 if 28 < v1 < 35 else v2
                lon = v2 if lat == v1 else v1
                itm_x, itm_y = to_itm.transform(lon, lat)
            else:
                # ITM (Israel New Grid)
                itm_x = v1 if v1 < 450000 else v2
                itm_y = v2 if itm_x == v1 else v1
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # --- הצגת נתונים מספריים וצילום מצב ---
            st.success(f"**מיקום זוהה:** {lat:.6f}, {lon:.6f}")
            
            # מנוע העתקה - הפתרון היחיד לסיכה בטוחה ב-PC ב-IHM/Caltopo
            st.write("#### 📋 1. העתק לחיפוש (לסיכה ב-IHM/קלטופו)")
            st.code(f"{lat:.6f}, {lon:.6f}")
            
            st.divider()

            # --- בניית קישורי המפות ---
            # גוגל ווייז - סיכה מובנית
            gm_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            wz_url = f"https://waze.com/ul?ll={lat},{lon}&navigate=yes"
            
            # אתרים מקצועיים - פתיחה במיקום (דורש הדבקה לסיכה)
            ihm_url = f"https://israelhiking.osm.org.il/map/16/{lat}/{lon}"
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=16"
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"

            st.write("#### 🚀 2. פתח מפה")
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1: st.link_button("🌐 Google", gm_url, use_container_width=True, type="primary")
            with c2: st.link_button("🚗 Waze", wz_url, use_container_width=True)
            with c3: st.link_button("🥾 IHM", ihm_url, use_container_width=True)
            with c4: st.link_button("🏔️ Caltopo", cal_url, use_container_width=True)
            with c5: st.link_button("☁️ עמוד ענן", aa_url, use_container_width=True)

            # תצוגה פנימית מהירה
            st.divider()
            st.write("#### 🗺️ תצוגה מהירה (Preview)")
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=14)

    except Exception as e:
        st.error(f"שגיאה בעיבוד הקלט: {e}")

st.caption("MemirHaHaV1 | Operational Stability Mode | 2025")
