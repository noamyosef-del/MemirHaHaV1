import streamlit as st
from pyproj import Transformer
import pandas as pd

# המרת קואורדינטות
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1 - Fix", layout="wide")
st.title("📍 תיקון מערכתי - MemirHaHaV1")

user_input = st.text_input("הדבק קואורדינטות:", placeholder="31.28392, 34.67544")

if user_input:
    try:
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(parts) == 2:
            v1, v2 = parts
            if 25 < v1 < 40 or 25 < v2 < 40:
                lat, lon = (v1, v2) if v1 < v2 else (v2, v1)
            else:
                itm_x, itm_y = (v1, v2) if v1 < v2 else (v2, v1)
                lon, lat = to_wgs.transform(itm_x, itm_y)

            st.success(f"TARGET: {lat:.6f}, {lon:.6f}")

            # --- בנייה מחדש של הקישורים (פרוטוקול Deep-Link) ---

            # 1. Google Maps - פורמט חיפוש (סיכה בטוחה)
            gm_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            # 2. Waze - רק מיקום (בלי ניווט אוטומטי כדי לראות את הסיכה)
            wz_url = f"https://waze.com/ul?ll={lat},{lon}&zoom=16"

            # 3. Israel Hiking (IHM) - פורמט הזרקת נקודה (מכריח סיכה כחולה)
            ihm_url = f"https://israelhiking.osm.org.il/map/15/{lat}/{lon}/points/{lat}/{lon}"

            # 4. Caltopo - פורמט Marker יציב
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=16&marker={lat},{lon}"

            # 5. עמוד ענן - תיקון פורמט למובייל ולדסקטופ
            # שימוש בפרמטרים מופרדים כדי להכריח את האפליקציה להסתנכרן
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}&lat={lat}&lon={lon}"

            st.write("### 🚀 בדיקה מחודשת (מובייל ו-PC):")
            c = st.columns(5)
            c[0].link_button("🌐 Google", gm_url, use_container_width=True)
            c[1].link_button("🚗 Waze", wz_url, use_container_width=True)
            c[2].link_button("🥾 IHM", ihm_url, use_container_width=True)
            c[3].link_button("🏔️ Caltopo", cal_url, use_container_width=True)
            c[4].link_button("☁️ עמוד ענן", aa_url, use_container_width=True)

            st.divider()
            st.code(f"{lat:.6f}, {lon:.6f}")
            st.caption("העתקה לגיבוי לחיפוש ידני אם האפליקציה חוסמת.")

    except:
        st.error("קלט לא תקין")
