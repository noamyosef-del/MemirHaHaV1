import streamlit as st
from pyproj import Transformer
import pandas as pd

# התמרת קואורדינטות
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍", layout="wide")
st.title("📍 MemirHaHaV1 - הפיצוח הטכנולוגי")

user_input = st.text_input("הדבק קואורדינטות:", placeholder="31.28392, 34.67544")

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

            st.success(f"TARGET: {lat:.6f}, {lon:.6f}")
            
            # מפה פנימית (עובדת תמיד)
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=14)

            st.divider()

            # --- הפיצוחים החדשים (הזרקת אובייקטים ל-URL) ---

            # 1. Israel Hiking Map - הפורמט היחיד שמכריח סיכה כחולה ב-PC
            ihm_url = f"https://israelhiking.osm.org.il/map/15/{lat}/{lon}?s=pt:{lat}:{lon}"

            # 2. Caltopo - תיקון ה-404: שימוש ב-Marker בתוך ה-Hash (חייב להגיע אחרי ה-ll)
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=16&marker={lat},{lon}"

            # 3. עמוד ענן - שימוש בפרמטר ?p= בלבד (ב-PC לפעמים לוקח לו זמן להיטען)
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"

            # 4. Google Maps - עם סיכה אדומה (הכי אמין)
            gm_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            # 5. Waze - חזר לבקשתך
            wz_url = f"https://waze.com/ul?ll={lat},{lon}&navigate=yes"

            st.write("### 🚀 קישורים לבדיקה (סיכה אחת לכל מפה):")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.link_button("🥾 IHM", ihm_url, use_container_width=True)
            c2.link_button("🏔️ Caltopo", cal_url, use_container_width=True)
            c3.link_button("☁️ עמוד ענן", aa_url, use_container_width=True)
            c4.link_button("🌐 Google", gm_url, use_container_width=True)
            c5.link_button("🚗 Waze", wz_url, use_container_width=True)

    except:
        st.error("Error")

st.info("💡 טיפ למשתמשי PC: אם ב-IHM לא מופיעה סיכה, נסה ללחוץ על הקישור שוב כשהלשונית כבר פתוחה.")
