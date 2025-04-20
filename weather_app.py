

import streamlit as st
import requests
from datetime import date, timedelta
from opencage.geocoder import OpenCageGeocode


WEATHER_API_KEY = 'a2de6ce2ff3642459a852619251104'  
GEOCODE_API_KEY = 'd3909e5e477c46ba94a67f92e41d411f'           
BASE_URL = 'https://api.weatherapi.com/v1'
geocoder = OpenCageGeocode(GEOCODE_API_KEY)

st.set_page_config(page_title="India Weather App", layout="centered")
st.title("🌦️ Weather Forecast ")



def get_city_from_input(location_input: str):
    if not location_input:
        return None

    if location_input.strip().isdigit():
        results = geocoder.geocode(location_input + ", India")
        if results:
            components = results[0]['components']
            return components.get('city') or components.get('town') or components.get('village')
        else:
            return None
    else:
        # Assume it's a valid city
        return location_input.strip()

# ========== INPUT ==========
location_input = st.text_input("Enter Indian Pincode or City", placeholder="e.g. 110001 or Delhi")

# ========== CURRENT WEATHER ==========
if st.button("Get Current Weather") and location_input:
    city = get_city_from_input(location_input)
    if not city:
        st.error("❌ Could not determine a valid city from your input.")
    else:
        try:
            res = requests.get(f"{BASE_URL}/current.json?key={WEATHER_API_KEY}&q={city}")
            data = res.json()

            if "error" in data:
                st.error(data["error"]["message"])
            else:
                current = data["current"]
                location = data["location"]

                st.subheader(f"Weather in {location['name']}, {location['country']}")
                st.image("https:" + current["condition"]["icon"])
                st.markdown(f"**Condition**: {current['condition']['text']}")
                st.markdown(f"🌡️ **Temperature**: {current['temp_c']} °C")
                st.markdown(f"💧 **Humidity**: {current['humidity']}%")
                st.markdown(f"🌬️ **Wind Speed**: {current['wind_kph']} km/h")

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ========== FORECAST ==========
st.markdown("---")
st.subheader("🔮 Forecast (Up to 3 Days Ahead)")

forecast_date = st.date_input(
    "Select Date",
    min_value=date.today(),
    max_value=date.today() + timedelta(days=3)
)

if st.button("Get Forecast") and location_input:
    city = get_city_from_input(location_input)
    if not city:
        st.error("❌ Could not determine a valid city from your input.")
    else:
        try:
            res = requests.get(f"{BASE_URL}/forecast.json?key={WEATHER_API_KEY}&q={city}&dt={forecast_date}")
            data = res.json()

            if "error" in data:
                st.error(data["error"]["message"])
            else:
                forecast = data["forecast"]["forecastday"][0]["day"]

                st.subheader(f"Forecast for {forecast_date}")
                st.image("https:" + forecast["condition"]["icon"])
                st.markdown(f"**Condition**: {forecast['condition']['text']}")
                st.markdown(f"🌡️ **Avg Temperature**: {forecast['avgtemp_c']} °C")
                st.markdown(f"💧 **Avg Humidity**: {forecast['avghumidity']}%")
                st.markdown(f"🌬️ **Max Wind**: {forecast['maxwind_kph']} km/h")

        except Exception as e:
            st.error(f"Error: {str(e)}")
