import streamlit as st
from pyproj import Transformer
import pandas as pd
import urllib.parse

# הגדרת המרת קואורדינטות
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍")
st.title("📍 MemirHaHaV1")

user_input = st.text_input("הדבק קואורדינטות:", placeholder="31.2839, 34.6754")

if user_input:
    try:
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(parts) == 2:
            v1, v2 = parts
            
            # לוגיקת Auto-Swap
            if 25 < v1 < 40 or 25 < v2 < 40: 
                lat = v1 if 28 < v1 < 35 else v2
                lon = v2 if lat == v1 else v1
                itm_x, itm_y = to_itm.transform(lon, lat)
            else: 
                itm_x = v1 if v1 < 400000 else v2
                itm_y = v2 if itm_x == v1 else v1
                lon, lat = to_wgs.transform(itm_x, itm_y)

            # תצוגה
            st.info(f"מיקום: {lat:.6f}, {lon:.6f}")
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=14)

            st.divider()

            # --- הפתרונות הסופיים לסיכות ---

            # 1. Israel Hiking Map - הפתרון היחיד שעובד כרגע להצגת סיכה הוא קידוד הנקודה ב-URL
            # אנחנו יוצרים "נתיב" (Route) של נקודה אחת
            ihm_url = f"https://israelhiking.osm.org.il/map/15/{lat}/{lon}?s=pt:{lat}:{lon}:Point"

            # 2. Caltopo - שימוש ב-marker בתוך ה-fragment (#)
            # אם marker= לא עובד, נשתמש ב-waypoint
            cal_url = f"https://caltopo.com/map.html#ll={lat},{lon}&z=16&marker={lat},{lon}"

            # 3. Amud Anan - p= (עובד תמיד)
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"

            # 4. Google Maps - להשוואה (עם סיכה בטוחה)
            gm_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            st.write("### פתיחה במפות:")
            col1, col2 = st.columns(2)
            with col1:
                st.link_button("🥾 Israel Hiking (ניסיון סיכה)", ihm_url, use_container_width=True)
                st.link_button("🏔️ Caltopo (סיכה אדומה)", cal_url, use_container_width=True)
            with col2:
                st.link_button("☁️ עמוד ענן", aa_url, use_container_width=True)
                st.link_button("🌐 Google Maps", gm_url, use_container_width=True)

    except:
        st.error("קלט לא תקין")
