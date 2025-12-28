import streamlit as st
from pyproj import Transformer
import pandas as pd

# הגדרת המרת קואורדינטות - רשת ישראל החדשה ל-WGS84 ולהפך
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍", layout="centered")

# כותרת האפליקציה
st.title("📍 MemirHaHaV1")
st.markdown("### ממיר קואורדינטות וסנכרון מפות חכם")

# קלט מהמשתמש
user_input = st.text_input("הדבק קואורדינטות (GPS או רשת ישראל):", placeholder="למשל: 31.2839, 34.6754")

if user_input:
    try:
        # ניקוי תווים מיותרים והפיכה לרשימת מספרים
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        
        if len(parts) == 2:
            v1, v2 = parts
            
            # --- לוגיקת זיהוי והחלפה אוטומטית (Auto-Swap) ---
            # בישראל: Lat (קו רוחב) הוא תמיד סביב 29-33, Lon (קו אורך) סביב 34-36
            if 25 < v1 < 40 or 25 < v2 < 40: 
                grid_name = "WGS84 (GPS)"
                lat = v1 if 28 < v1 < 35 else v2
                lon = v2 if lat == v1 else v1
                itm_x, itm_y = to_itm.transform(lon, lat)
            else: 
                # ברשת ישראל: הצפון (Y) תמיד גדול משמעותית מהמזרח (X)
                grid_name = "ITM (Israel New Grid)"
                itm_x = v1 if v1 < 400000 else v2
                itm_y = v2 if itm_x == v1 else v1
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # הצגת נתונים מספריים
            st.info(f"הקלט זוהה כ: **{grid_name}**")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("GPS (Lat, Lon)", f"{lat:.6f}, {lon:.6f}")
            with col_b:
                st.metric("ITM (E, N)", f"{int(itm_x)}, {int(itm_y)}")

            # --- תצוגת מפה פנימית (Preview) ---
            st.write("#### 🗺️ תצוגה מהירה:")
            preview_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
            st.map(preview_data, zoom=14)

            st.divider()
            st.write("#### 🚀 פתיחה באתרים חיצוניים (עם סיכה):")

            # --- בניית קישורים עם סיכות (Markers) עובדות ---
            
            # Israel Hiking Map - שימוש בנתיב /points/ הייעודי להצגת סיכה
            ihm_url = f"https://israelhiking.osm.org.il/map/15/{lat}/{lon}/points/{lat}/{lon}"
            
            # Caltopo - שימוש בפרמטר marker (ביחיד) שמציג סמן בולט
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=15&marker={lat},{lon}"
            
            # Amud Anan - פרמטר p= הוא הסטנדרט לנקודה משותפת
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"
            
            # Waze - ניווט ישיר לנקודה
            wz_url = f"https://waze.com/ul?ll={lat},{lon}&navigate=yes"

            # כפתורי קישור
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("🥾 Israel Hiking (סיכה)", ihm_url, use_container_width=True)
                st.link_button("☁️ עמוד ענן", aa_url, use_container_width=True)
            with c2:
                st.link_button("🏔️ Caltopo (סיכה)", cal_url, use_container_width=True)
                st.link_button("🚗 Waze", wz_url, use_container_width=True)
                
    except Exception:
        st.error("שגיאה: הקלט אינו תקין. נא להזין זוג מספרים בלבד.")

st.caption("MemirHaHaV1 | Marker Sync Engine | 2025 Optimized")
