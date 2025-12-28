import streamlit as st
from pyproj import Transformer
import pandas as pd

# התמרת קואורדינטות
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1 - Pro", page_icon="📍", layout="wide")
st.title("📍 MemirHaHaV1 - Expert Final Build")

user_input = st.text_input("הדבק קואורדינטות:", placeholder="31.28392, 34.67544")

if user_input:
    try:
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(parts) == 2:
            v1, v2 = parts
            # לוגיקת Auto-Swap (מותאמת לישראל)
            if 25 < v1 < 40 or 25 < v2 < 40:
                lat = v1 if 28 < v1 < 35 else v2
                lon = v2 if lat == v1 else v1
            else:
                itm_x = v1 if v1 < 450000 else v2
                itm_y = v2 if itm_x == v1 else v1
                lon, lat = to_wgs.transform(itm_x, itm_y)

            st.success(f"TARGET: {lat:.6f}, {lon:.6f}")
            
            # --- הפיצוחים הטכנולוגיים לסיכה ב-PC ---

            # 1. Israel Hiking Map - פורמט ה-"Points" החדש
            # הוספת /points/ בסוף הנתיב היא הדרך היחידה להזרקת אובייקט ב-PC
            ihm_url = f"https://israelhiking.osm.org.il/map/15/{lat}/{lon}/points/{lat}/{lon}"

            # 2. Caltopo - שימוש ב-Marker בתוך ה-Hash בסדר ספציפי למניעת 404
            # ה-ll חייב להיות ראשון וה-marker חייב להיות זהה לו
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=16&marker={lat},{lon}"

            # 3. עמוד ענן - הוספת פרמטר p ומיקום מרכזי
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"

            # 4. Google Maps - שימוש ב-API הרשמי להצגת Marker
            gm_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            # 5. Waze - פורמט הניווט היציב
            wz_url = f"https://waze.com/ul?ll={lat},{lon}&navigate=yes"

            st.write("### 🚀 קישורים מותאמי PC (עם סיכה):")
            cols = st.columns(5)
            data = [
                ("🥾 IHM", ihm_url),
                ("🏔️ Caltopo", cal_url),
                ("☁️ עמוד ענן", aa_url),
                ("🌐 Google", gm_url),
                ("🚗 Waze", wz_url)
            ]
            
            for i, (label, url) in enumerate(data):
                cols[i].link_button(label, url, use_container_width=True)

            # תצוגה מהירה לווידוא
            st.divider()
            st.write("#### 🗺️ תצוגה מהירה (Preview)")
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=14)

    except Exception as e:
        st.error(f"שגיאה: {e}")

st.caption("MemirHaHaV1 | Expert Panel Final Version | Built for Windows 10")
