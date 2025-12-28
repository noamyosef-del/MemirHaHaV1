import streamlit as st
from pyproj import Transformer
import pandas as pd

# הגדרת המרות
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍", layout="wide")
st.title("📍 MemirHaHaV1")

user_input = st.text_input("הדבק קואורדינטות:", placeholder="31.28392, 34.67544")

if user_input:
    try:
        # ניקוי ופירוק קלט
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(parts) == 2:
            v1, v2 = parts
            # לוגיקת Swap חכמה לישראל (כולל יו"ש והים)
            if 25 < v1 < 40 or 25 < v2 < 40:
                lat = v1 if 28 < v1 < 35 else v2
                lon = v2 if lat == v1 else v1
                itm_x, itm_y = to_itm.transform(lon, lat)
            else:
                itm_x = v1 if v1 < 450000 else v2
                itm_y = v2 if itm_x == v1 else v1
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # תצוגת נתונים
            st.write(f"### 📍 מיקום: `{lat:.6f}, {lon:.6f}`")
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=14)

            st.divider()

            # --- בניית קישורי "קליק אחד וסיכה" (One-Click Marker) ---

            # 1. Israel Hiking Map - שימוש בקידוד סיכה ישיר
            # הפורמט הזה יוצר נקודה ב-Side Panel וסיכה כחולה במפה
            ihm_url = f"https://israelhiking.osm.org.il/map/15/{lat}/{lon}?s=pt:{lat}:{lon}:Target"

            # 2. Caltopo - שימוש בפורמט Marker אגרסיבי
            # הוספת ה-z=16 לפני ה-Marker עוזרת ל-PC לרנדר את הסיכה
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=16&marker={lat},{lon}"

            # 3. Amud Anan - ה-p הקלאסי
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"
            
            # 4. Google Maps - עם סיכה אדומה מובנית
            gm_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            # 5. Waze - ניווט
            wz_url = f"https://waze.com/ul?ll={lat},{lon}&navigate=yes"

            st.write("### 🚀 פתח במפה (עם סיכה):")
            rows = st.columns(5)
            labels = ["🥾 IHM", "🏔️ Caltopo", "☁️ עמוד ענן", "🌐 Google", "🚗 Waze"]
            urls = [ihm_url, cal_url, aa_url, gm_url, wz_url]
            
            for i, col in enumerate(rows):
                col.link_button(labels[i], urls[i], use_container_width=True)

    except:
        st.error("קלט לא תקין. נא להזין זוג מספרים.")

st.caption("MemirHaHaV1 | Marker Sync Engine | No extra steps required")
