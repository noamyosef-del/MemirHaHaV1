import streamlit as st
from pyproj import Transformer
import pandas as pd

# הגדרת המרות
to_wgs = Transformer.from_crs("epsg:2039", "epsg:4326", always_xy=True)
to_itm = Transformer.from_crs("epsg:4326", "epsg:2039", always_xy=True)

st.set_page_config(page_title="MemirHaHaV1", page_icon="📍")
st.title("📍 MemirHaHaV1 - Final Fix")

user_input = st.text_input("הדבק קואורדינטות:", placeholder="31.28392, 34.67544")

if user_input:
    try:
        parts = [float(n) for n in user_input.replace(',', ' ').split()]
        if len(parts) == 2:
            v1, v2 = parts
            # לוגיקת Swap
            if 25 < v1 < 40 or 25 < v2 < 40:
                lat, lon = (v1, v2) if v1 < v2 else (v2, v1)
                itm_x, itm_y = to_itm.transform(lon, lat)
            else:
                itm_x, itm_y = (v1, v2) if v1 < v2 else (v2, v1)
                lon, lat = to_wgs.transform(itm_x, itm_y)

            st.write(f"### מיקום: {lat:.6f}, {lon:.6f}")
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=14)

            # --- הפתרונות "מחוץ לקופסה" ---

            # 1. Israel Hiking Map - שימוש בפרמטר r (Route) עם נקודה בודדת
            # זה מכריח את הממשק לצייר עיגול כחול של "תחילת מסלול"
            ihm_url = f"https://israelhiking.osm.org.il/map/16/{lat}/{lon}?s=pt:{lat}:{lon}:Target"

            # 2. Caltopo - שימוש בפרמטר Search
            # כשהוא מקבל חיפוש של קואורדינטות, הוא שם סיכה אדומה של 'Search Result'
            cal_url = f"https://caltopo.com/search?q={lat},{lon}"

            # 3. Amud Anan - נשאר עם p המנצח
            aa_url = f"https://amudanan.co.il/?p={lat},{lon}"
            
            # 4. Google Maps - פורמט חיפוש (הכי אמין לסיכה)
            gm_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            st.divider()
            st.write("### לחץ לבדיקה (PC):")
            c1, c2, c3, c4 = st.columns(4)
            c1.link_button("🥾 IHM", ihm_url, use_container_width=True)
            c2.link_button("🏔️ Caltopo", cal_url, use_container_width=True)
            c3.link_button("☁️ עמוד ענן", aa_url, use_container_width=True)
            c4.link_button("🌐 Google", gm_url, use_container_width=True)

    except:
        st.error("Error")
