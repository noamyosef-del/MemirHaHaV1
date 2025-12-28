import streamlit as st
from pyproj import Transformer
import pandas as pd

# המרת קואורדינטות
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1 - Mobile Fix", layout="wide")
st.title("📍 MemirHaHaV1 - גרסת האפליקציות")

user_input = st.text_input("הדבק קואורדינטות (GPS/רשת ישראל):")

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

            st.success(f"מיקום: {lat:.6f}, {lon:.6f}")

            # --- בניית קישורים עמוקים (Deep Links) למובייל ---

            # 1. עמוד ענן - שימוש בפורמט amudanan:// (מכריח פתיחת אפליקציה)
            # אם זה לא עובד במכשיר ספציפי, משתמשים בפורמט ה-Web המשופר
            aa_app_url = f"amudanan://map?lat={lat}&lon={lon}"
            aa_web_url = f"https://amudanan.co.il/?p={lat},{lon}"

            # 2. Israel Hiking (IHM) - פורמט שמפעיל את האפליקציה בסיכה
            ihm_url = f"https://israelhiking.osm.org.il/share/Point/{lat}/{lon}/Target"

            # 3. Caltopo - שימוש בפורמט ה-Marker היציב ביותר
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=16&marker={lat},{lon}"

            # 4. Google Maps - API רשמי (היחיד עם סיכה בטוחה)
            gm_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            # 5. Waze - ללא ניווט אוטומטי (כדי לראות סיכה)
            wz_url = f"waze://?ll={lat},{lon}&z=10"

            st.write("### 🚀 פתיחה (תעדיף את הכפתורים עם האייקון):")
            
            # שורה 1: גוגל ו-ווייז
            col1, col2 = st.columns(2)
            col1.link_button("🌐 Google Maps (סיכה)", gm_url, use_container_width=True)
            col2.link_button("🚗 Waze (סיכה)", wz_url, use_container_width=True)

            # שורה 2: אפליקציות שטח
            st.divider()
            st.write("#### אפליקציות שטח (מובייל):")
            c1, c2, c3 = st.columns(3)
            # עמוד ענן עם ניסיון כפול
            c1.link_button("☁️ עמוד ענן", aa_app_url, use_container_width=True)
            c2.link_button("🥾 Israel Hiking", ihm_url, use_container_width=True)
            c3.link_button("🏔️ Caltopo", cal_url, use_container_width=True)

            # גיבוי לעמוד ענן אם האפליקציה לא מגיבה
            st.caption("אם 'עמוד ענן' לא נפתח, נסה את הקישור הישיר:")
            st.write(aa_web_url)

    except:
        st.error("Error")
