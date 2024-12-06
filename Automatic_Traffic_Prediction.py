# import streamlit as st
# import requests
# import folium
# from streamlit_folium import st_folium
# import joblib
# import numpy as np
# from datetime import datetime

# # Load the traffic prediction model and scaler
# model = joblib.load('traffic_prediction_model.pkl')
# scaler = joblib.load('scaler.pkl')

# # Title of the App
# st.title("Route Finder with Weather and Traffic Prediction")

# # Sidebar Input for API Keys
# graphhopper_api_key = st.sidebar.text_input("Enter your GraphHopper API Key", type="password")
# weather_api_key = st.sidebar.text_input("Enter your WeatherAPI Key", type="password")

# # Input for Source and Destination
# source = st.text_input("Enter Source Coordinates (latitude,longitude)", "28.64,77.21")
# destination = st.text_input("Enter Destination Coordinates (latitude,longitude)", "32.71,74.85")

# # Initialize session state for route, weather, and traffic prediction data
# if "route_data" not in st.session_state:
#     st.session_state["route_data"] = None
# if "weather_data" not in st.session_state:
#     st.session_state["weather_data"] = None
# if "traffic_prediction" not in st.session_state:
#     st.session_state["traffic_prediction"] = None

# # Coded day mapping for traffic prediction
# coded_day_mapping = {
#     "Monday": 1,
#     "Tuesday": 2,
#     "Wednesday": 3,
#     "Thursday": 4,
#     "Friday": 5,
#     "Saturday": 6,
#     "Sunday": 7
# }

# # Traffic level mapping
# traffic_mapping = {
#     1: "Light traffic",
#     2: "Moderate traffic",
#     3: "Heavy traffic",
#     4: "Very heavy traffic",
#     5: "Severe congestion"
# }

# # Cache API data to avoid re-fetching
# @st.cache_data(ttl=600)  # Cache for 10 minutes
# def fetch_weather_data(location, api_key):
#     try:
#         response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}")
#         data = response.json()
#         if "error" in data:
#             return None, "Location not found. Please try again."
#         return data, None
#     except Exception as e:
#         return None, f"Error fetching data: {e}"

# def fetch_route(api_key, source, destination):
#     try:
#         # Parse coordinates
#         source_coords = source.split(",")
#         dest_coords = destination.split(",")
#         source_lat, source_lon = float(source_coords[0]), float(source_coords[1])
#         dest_lat, dest_lon = float(dest_coords[0]), float(dest_coords[1])

#         # GraphHopper API Request
#         url = "https://graphhopper.com/api/1/route"
#         params = {
#             "point": [f"{source_lat},{source_lon}", f"{dest_lat},{dest_lon}"],
#             "profile": "car",
#             "locale": "en",
#             "key": api_key,
#             "points_encoded": "false",
#         }
#         response = requests.get(url, params=params)

#         if response.status_code == 200:
#             data = response.json()
#             coordinates = data["paths"][0]["points"]["coordinates"]
#             return coordinates, source_lat, source_lon, dest_lat, dest_lon
#         else:
#             st.error(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
#             return None, None, None, None, None
#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")
#         return None, None, None, None, None

# # # Button to Fetch Route, Weather, and Predict Traffic
# # if st.button("Get Route, Weather, and Predict Traffic"):
# #     if graphhopper_api_key and weather_api_key:
# #         # Fetch Route
# #         coordinates, source_lat, source_lon, dest_lat, dest_lon = fetch_route(graphhopper_api_key, source, destination)
# #         if coordinates:
# #             st.session_state["route_data"] = {
# #                 "coordinates": coordinates,
# #                 "source_lat": source_lat,
# #                 "source_lon": source_lon,
# #                 "dest_lat": dest_lat,
# #                 "dest_lon": dest_lon,
# #             }

# #             # Fetch Weather for Source
# #             source_weather, source_error = fetch_weather_data(f"{source_lat},{source_lon}", weather_api_key)
# #             if source_weather:
# #                 st.session_state["weather_data"] = source_weather

# #                 # Extract weather parameters
# #                 temperature = source_weather['current']['temp_c']
# #                 weather_code = source_weather['current']['condition']['code']
# #                 current_day = datetime.now().strftime("%A")
# #                 coded_day = coded_day_mapping[current_day]

# #                 # Zone (optional: you can determine based on your dataset or hardcode a value for testing)
# #                 zone = 1  # Adjust based on your use case

# #                 # Prepare input data for traffic prediction
# #                 input_data = np.array([[coded_day, zone, weather_code, temperature]])
# #                 scaled_data = scaler.transform(input_data)

# #                 # Predict Traffic
# #                 prediction = model.predict(scaled_data)
# #                 traffic_level = int(np.round(prediction).astype(int)[0])
# #                 st.session_state["traffic_prediction"] = traffic_mapping.get(traffic_level, "Unknown traffic level")
# # Button to Fetch Route, Weather, and Predict Traffic
# if st.button("Get Route, Weather, and Predict Traffic"):
#     if graphhopper_api_key and weather_api_key:
#         # Fetch Route
#         coordinates, source_lat, source_lon, dest_lat, dest_lon = fetch_route(graphhopper_api_key, source, destination)
#         if coordinates:
#             st.session_state["route_data"] = {
#                 "coordinates": coordinates,
#                 "source_lat": source_lat,
#                 "source_lon": source_lon,
#                 "dest_lat": dest_lat,
#                 "dest_lon": dest_lon,
#             }

#             # Fetch Weather for Source and Destination
#             source_weather, source_error = fetch_weather_data(f"{source_lat},{source_lon}", weather_api_key)
#             destination_weather, destination_error = fetch_weather_data(f"{dest_lat},{dest_lon}", weather_api_key)

#             if source_weather and destination_weather:
#                 st.session_state["weather_data"] = {
#                     "source": source_weather,
#                     "destination": destination_weather,
#                 }

#                 # Debug: Display fetched weather data
#                 st.write("Debug: Weather data at source", source_weather)
#                 st.write("Debug: Weather data at destination", destination_weather)

#                 # Extract weather parameters for traffic prediction (source)
#                 try:
#                     temperature = source_weather['current']['temp_c']
#                     weather_code = source_weather['current']['condition']['code']
#                     current_day = datetime.now().strftime("%A")
#                     coded_day = coded_day_mapping[current_day]

#                     # Zone (optional: you can determine based on your dataset or hardcode a value for testing)
#                     zone = 1  # Adjust based on your use case

#                     # Prepare input data for traffic prediction
#                     input_data = np.array([[coded_day, zone, weather_code, temperature]])
                    
#                     # Debug: Display input data for model
#                     st.write("Debug: Input data for model", input_data)

#                     scaled_data = scaler.transform(input_data)

#                     # Predict Traffic
#                     prediction = model.predict(scaled_data)
#                     traffic_level = int(np.round(prediction).astype(int)[0])
                    
#                     # Debug: Display model prediction
#                     st.write("Debug: Model prediction output", prediction)

#                     st.session_state["traffic_prediction"] = traffic_mapping.get(traffic_level, "Unknown traffic level")
#                 except Exception as e:
#                     st.error(f"Error during traffic prediction: {e}")
#             else:
#                 st.error("Weather data could not be fetched for source or destination.")
#     else:
#         st.error("Please provide valid API keys for both GraphHopper and WeatherAPI!")

# # Display Traffic Prediction
# # if st.session_state["traffic_prediction"]:
# #     st.subheader("Traffic Prediction")
# #     st.success(f"The predicted traffic level at the source is: {st.session_state['traffic_prediction']}")


# # Display the Route
# if st.session_state["route_data"]:
#     route_data = st.session_state["route_data"]
#     coordinates = route_data["coordinates"]
#     source_lat, source_lon = route_data["source_lat"], route_data["source_lon"]
#     dest_lat, dest_lon = route_data["dest_lat"], route_data["dest_lon"]

#     # Create a Map using Folium
#     st.subheader("Route Map")
#     m = folium.Map(location=[source_lat, source_lon], zoom_start=6)
#     folium.Marker([source_lat, source_lon], popup="Source", icon=folium.Icon(color="green")).add_to(m)
#     folium.Marker([dest_lat, dest_lon], popup="Destination", icon=folium.Icon(color="red")).add_to(m)
#     route = [(coord[1], coord[0]) for coord in coordinates]
#     folium.PolyLine(route, color="blue", weight=5, opacity=0.8).add_to(m)
#     st_folium(m, width=800, height=500)

# if st.session_state["weather_data"] and "source" in st.session_state["weather_data"]:
#     source_weather = st.session_state["weather_data"]["source"]
#     st.subheader("Weather Information at Source")
#     st.write(f"**Location:** {source_weather['location']['name']}, {source_weather['location']['region']}, {source_weather['location']['country']}")
#     st.write(f"**Condition:** {source_weather['current']['condition']['text']}")
#     st.write(f"**Temperature:** {source_weather['current']['temp_c']} °C")
#     st.write(f"**Wind Speed:** {source_weather['current']['wind_kph']} km/h")
#     st.write(f"**Humidity:** {source_weather['current']['humidity']}%")
#     st.write(f"**Pressure:** {source_weather['current']['pressure_mb']} hPa")
#     st.write(f"**Visibility:** {source_weather['current']['vis_km']} km")

# # Display Weather Information for Destination
# if st.session_state["weather_data"] and "destination" in st.session_state["weather_data"]:
#     destination_weather = st.session_state["weather_data"]["destination"]
#     st.subheader("Weather Information at Destination")
#     st.write(f"**Location:** {destination_weather['location']['name']}, {destination_weather['location']['region']}, {destination_weather['location']['country']}")
#     st.write(f"**Condition:** {destination_weather['current']['condition']['text']}")
#     st.write(f"**Temperature:** {destination_weather['current']['temp_c']} °C")
#     st.write(f"**Wind Speed:** {destination_weather['current']['wind_kph']} km/h")
#     st.write(f"**Humidity:** {destination_weather['current']['humidity']}%")
#     st.write(f"**Pressure:** {destination_weather['current']['pressure_mb']} hPa")
#     st.write(f"**Visibility:** {destination_weather['current']['vis_km']} km")

# # Display Traffic Prediction
# if st.session_state["traffic_prediction"]:
#     st.subheader("Traffic Prediction")
#     st.success(f"The predicted traffic level at the source is: {st.session_state['traffic_prediction']}")


# import streamlit as st
# import requests
# import folium
# from streamlit_folium import st_folium
# import joblib
# import numpy as np
# from datetime import datetime
# from geopy.geocoders import Nominatim

# # Load the traffic prediction model and scaler
# model = joblib.load('traffic_prediction_model.pkl')
# scaler = joblib.load('scaler.pkl')

# # Title of the App
# st.title("Route Finder with Weather and Traffic Prediction")

# # Sidebar Input for API Keys
# graphhopper_api_key = st.sidebar.text_input("Enter your GraphHopper API Key", type="password")
# weather_api_key = st.sidebar.text_input("Enter your WeatherAPI Key", type="password")

# # Input for Source and Destination Locations
# source = st.text_input("Enter Source Location:", "New Delhi")
# destination = st.text_input("Enter Destination Location:", "Jammu")

# # Initialize Geolocator
# geolocator = Nominatim(user_agent="streamlit_map_app")

# # Convert location names to latitude and longitude
# try:
#     source_location = geolocator.geocode(source)
#     destination_location = geolocator.geocode(destination)

#     if source_location and destination_location:
#         source_lat, source_lon = source_location.latitude, source_location.longitude
#         dest_lat, dest_lon = destination_location.latitude, destination_location.longitude
#         st.write(f"**Source Coordinates:** {source_lat}, {source_lon}")
#         st.write(f"**Destination Coordinates:** {dest_lat}, {dest_lon}")
#     else:
#         st.error("Could not find one or both locations. Please try again.")
# except Exception as e:
#     st.error(f"Error fetching coordinates: {e}")

# # Initialize session state for route, weather, and traffic prediction data
# if "route_data" not in st.session_state:
#     st.session_state["route_data"] = None
# if "weather_data" not in st.session_state:
#     st.session_state["weather_data"] = None
# if "traffic_prediction" not in st.session_state:
#     st.session_state["traffic_prediction"] = None

# # Coded day mapping for traffic prediction
# coded_day_mapping = {
#     "Monday": 1,
#     "Tuesday": 2,
#     "Wednesday": 3,
#     "Thursday": 4,
#     "Friday": 5,
#     "Saturday": 6,
#     "Sunday": 7
# }

# # Traffic level mapping
# traffic_mapping = {
#     1: "Light traffic",
#     2: "Moderate traffic",
#     3: "Heavy traffic",
#     4: "Very heavy traffic",
#     5: "Severe congestion"
# }

# # Cache API data to avoid re-fetching
# @st.cache_data(ttl=600)  # Cache for 10 minutes
# def fetch_weather_data(location, api_key):
#     try:
#         response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}")
#         data = response.json()
#         if "error" in data:
#             return None, "Location not found. Please try again."
#         return data, None
#     except Exception as e:
#         return None, f"Error fetching data: {e}"

# def fetch_route(api_key, source_lat, source_lon, dest_lat, dest_lon):
#     try:
#         # GraphHopper API Request
#         url = "https://graphhopper.com/api/1/route"
#         params = {
#             "point": [f"{source_lat},{source_lon}", f"{dest_lat},{dest_lon}"],
#             "profile": "car",
#             "locale": "en",
#             "key": api_key,
#             "points_encoded": "false",
#         }
#         response = requests.get(url, params=params)

#         if response.status_code == 200:
#             data = response.json()
#             coordinates = data["paths"][0]["points"]["coordinates"]
#             return coordinates
#         else:
#             st.error(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
#             return None
#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")
#         return None

# # Button to Fetch Route, Weather, and Predict Traffic
# if st.button("Get Route, Weather, and Predict Traffic"):
#     if graphhopper_api_key and weather_api_key and source_location and destination_location:
#         # Fetch Route
#         coordinates = fetch_route(graphhopper_api_key, source_lat, source_lon, dest_lat, dest_lon)
#         if coordinates:
#             st.session_state["route_data"] = {
#                 "coordinates": coordinates,
#                 "source_lat": source_lat,
#                 "source_lon": source_lon,
#                 "dest_lat": dest_lat,
#                 "dest_lon": dest_lon,
#             }

#             # Fetch Weather for Source and Destination
#             source_weather, source_error = fetch_weather_data(f"{source_lat},{source_lon}", weather_api_key)
#             destination_weather, destination_error = fetch_weather_data(f"{dest_lat},{dest_lon}", weather_api_key)

#             if source_weather and destination_weather:
#                 st.session_state["weather_data"] = {
#                     "source": source_weather,
#                     "destination": destination_weather,
#                 }

#                 # Extract weather parameters for traffic prediction (source)
#                 temperature = source_weather['current']['temp_c']
#                 weather_code = source_weather['current']['condition']['code']
#                 current_day = datetime.now().strftime("%A")
#                 coded_day = coded_day_mapping[current_day]

#                 # Zone (optional: you can determine based on your dataset or hardcode a value for testing)
#                 zone = 1  # Adjust based on your use case

#                 # Prepare input data for traffic prediction
#                 input_data = np.array([[coded_day, zone, weather_code, temperature]])
#                 scaled_data = scaler.transform(input_data)

#                 # Predict Traffic
#                 prediction = model.predict(scaled_data)
#                 traffic_level = int(np.round(prediction).astype(int)[0])
#                 st.session_state["traffic_prediction"] = traffic_mapping.get(traffic_level, "Unknown traffic level")
#             else:
#                 st.error("Weather data could not be fetched for source or destination.")
#     else:
#         st.error("Please provide valid API keys and location names!")

# # Display the Route
# if st.session_state["route_data"]:
#     route_data = st.session_state["route_data"]
#     coordinates = route_data["coordinates"]
#     source_lat, source_lon = route_data["source_lat"], route_data["source_lon"]
#     dest_lat, dest_lon = route_data["dest_lat"], route_data["dest_lon"]

#     # Create a Map using Folium
#     st.subheader("Route Map")
#     m = folium.Map(location=[source_lat, source_lon], zoom_start=6)
#     folium.Marker([source_lat, source_lon], popup="Source", icon=folium.Icon(color="green")).add_to(m)
#     folium.Marker([dest_lat, dest_lon], popup="Destination", icon=folium.Icon(color="red")).add_to(m)
#     route = [(coord[1], coord[0]) for coord in coordinates]
#     folium.PolyLine(route, color="blue", weight=5, opacity=0.8).add_to(m)
#     st_folium(m, width=800, height=500)

# # Display Weather Information
# if st.session_state["weather_data"]:
#     st.subheader("Weather Information")
#     source_weather = st.session_state["weather_data"]["source"]
#     destination_weather = st.session_state["weather_data"]["destination"]
#     # st.write(f"**Source Location:** {source_weather['location']['name']}")
#     # st.write(f"**Condition:** {source_weather['current']['condition']['text']}, **Temperature:** {source_weather['current']['temp_c']}°C")
#     # st.write(f"**Destination Location:** {destination_weather['location']['name']}")
#     # st.write(f"**Condition:** {destination_weather['current']['condition']['text']}, **Temperature:** {destination_weather['current']['temp_c']}°C")
#     source_weather = st.session_state["weather_data"]["source"]
#     st.subheader("Weather Information at Source")
#     st.write(f"**Location:** {source_weather['location']['name']}, {source_weather['location']['region']}, {source_weather['location']['country']}")
#     st.write(f"**Condition:** {source_weather['current']['condition']['text']}")
#     st.write(f"**Temperature:** {source_weather['current']['temp_c']} °C")
#     st.write(f"**Wind Speed:** {source_weather['current']['wind_kph']} km/h")
#     st.write(f"**Humidity:** {source_weather['current']['humidity']}%")
#     st.write(f"**Pressure:** {source_weather['current']['pressure_mb']} hPa")
#     st.write(f"**Visibility:** {source_weather['current']['vis_km']} km")

# # Display Weather Information at Destination
#     destination_weather = st.session_state["weather_data"]["destination"]
#     st.subheader("Weather Information at Destination")
#     st.write(f"**Location:** {destination_weather['location']['name']}, {destination_weather['location']['region']}, {destination_weather['location']['country']}")
#     st.write(f"**Condition:** {destination_weather['current']['condition']['text']}")
#     st.write(f"**Temperature:** {destination_weather['current']['temp_c']} °C")
#     st.write(f"**Wind Speed:** {destination_weather['current']['wind_kph']} km/h")
#     st.write(f"**Humidity:** {destination_weather['current']['humidity']}%")
#     st.write(f"**Pressure:** {destination_weather['current']['pressure_mb']} hPa")
#     st.write(f"**Visibility:** {destination_weather['current']['vis_km']} km")

# # Display Traffic Prediction
# if st.session_state["traffic_prediction"]:
#     st.subheader("Traffic Prediction")
#     st.success(f"The predicted traffic level at the source is: {st.session_state['traffic_prediction']}")
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import joblib
import numpy as np
from datetime import datetime
from geopy.geocoders import Nominatim
import holidays
import pandas as pd
from pymongo import MongoClient

# MongoDB Atlas Connection - Replace <db_password> with your actual password
MONGO_URI = "mongodb+srv://jafferali0741:b4Uk9KZ64sg4f4ar@cluster0.znrk9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)  # Use the actual MongoDB connection string here
db = client["automatic_traffic_db"]  # Database name (create it if it doesn't exist)
collection = db["outputs"]  # Collection name (create it if it doesn't exist)

def predict_traffic_density(hour, isholiday, weekday, month, year, season):
    # Load the model
    model = joblib.load('final_model.pkl')
    
    # Map inputs
    weekday_map = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6
    }
    season_map = {
        'Spring': 0, 'Summer': 1, 'Fall': 2, 'Winter': 3
    }
    
    # Convert inputs to numeric
    weekday = weekday_map.get(weekday, -1)
    season = season_map.get(season, -1)
    isholiday = int(isholiday)

    # Check for invalid input
    if weekday == -1 or season == -1:
        raise ValueError("Invalid weekday or season")

    # Create input DataFrame
    input_data = pd.DataFrame([{
        'hour': hour,
        'isholiday': isholiday,
        'weekday': weekday,
        'month': month,
        'year': year,
        'season': season
    }])

    # Predict traffic density
    prediction = model.predict(input_data)
    return prediction[0]

def get_season_for_india(month):
    """Returns the season based on the month, using the available seasons."""
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Summer'
    elif month in [6, 7, 8, 9]:
        return 'Summer'  # Monsoon season fits under Summer
    elif month in [10, 11]:
        return 'Fall'
    else:
        return np.nan

# Load the traffic prediction model and scaler
model = joblib.load('traffic_prediction_model.pkl')
scaler = joblib.load('scaler.pkl')

# Title of the App
st.title("Route Finder with Weather and Traffic Prediction")

# Sidebar Input for API Keys
graphhopper_api_key = st.sidebar.text_input("Enter your GraphHopper API Key", type="password")
weather_api_key = st.sidebar.text_input("Enter your WeatherAPI Key", type="password")

# Input for Source and Destination Locations
source = st.text_input("Enter Source Location:", "New Delhi")
destination = st.text_input("Enter Destination Location:", "Jammu")

# Initialize Geolocator
geolocator = Nominatim(user_agent="streamlit_map_app")

# Convert location names to latitude and longitude
try:
    source_location = geolocator.geocode(source)
    destination_location = geolocator.geocode(destination)

    if source_location and destination_location:
        source_lat, source_lon = source_location.latitude, source_location.longitude
        dest_lat, dest_lon = destination_location.latitude, destination_location.longitude
        st.write(f"**Source Coordinates:** {source_lat}, {source_lon}")
        st.write(f"**Destination Coordinates:** {dest_lat}, {dest_lon}")
    else:
        st.error("Could not find one or both locations. Please try again.")
except Exception as e:
    st.error(f"Error fetching coordinates: {e}")

# Initialize session state for route, weather, and traffic prediction data
if "route_data" not in st.session_state:
    st.session_state["route_data"] = None
if "weather_data" not in st.session_state:
    st.session_state["weather_data"] = None
if "traffic_prediction" not in st.session_state:
    st.session_state["traffic_prediction"] = None

# Coded day mapping for traffic prediction
coded_day_mapping = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}

# Traffic level mapping
traffic_mapping = {
    1: "Light traffic",
    2: "Moderate traffic",
    3: "Heavy traffic",
    4: "Very heavy traffic",
    5: "Severe congestion"
}

# Cache API data to avoid re-fetching
@st.cache_data(ttl=600)  # Cache for 10 minutes
def fetch_weather_data(location, api_key):
    try:
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}")
        data = response.json()
        if "error" in data:
            return None, "Location not found. Please try again."
        return data, None
    except Exception as e:
        return None, f"Error fetching data: {e}"

def fetch_route(api_key, source_lat, source_lon, dest_lat, dest_lon):
    try:
        # GraphHopper API Request
        url = "https://graphhopper.com/api/1/route"
        params = {
            "point": [f"{source_lat},{source_lon}", f"{dest_lat},{dest_lon}"],
            "profile": "car",
            "locale": "en",
            "key": api_key,
            "points_encoded": "false",
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            coordinates = data["paths"][0]["points"]["coordinates"]
            return coordinates
        else:
            st.error(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Button to Fetch Route, Weather, and Predict Traffic
if st.button("Get Route, Weather, and Predict Traffic"):
    if graphhopper_api_key and weather_api_key and source_location and destination_location:
        # Fetch Route
        coordinates = fetch_route(graphhopper_api_key, source_lat, source_lon, dest_lat, dest_lon)
        if coordinates:
            st.session_state["route_data"] = {
                "coordinates": coordinates,
                "source_lat": source_lat,
                "source_lon": source_lon,
                "dest_lat": dest_lat,
                "dest_lon": dest_lon,
            }

            # Fetch Weather for Source and Destination
            source_weather, source_error = fetch_weather_data(f"{source_lat},{source_lon}", weather_api_key)
            destination_weather, destination_error = fetch_weather_data(f"{dest_lat},{dest_lon}", weather_api_key)

            if source_weather and destination_weather:
                st.session_state["weather_data"] = {
                    "source": source_weather,
                    "destination": destination_weather,
                }

                # Extract weather parameters for traffic prediction (source)
                date = datetime.strptime(source_weather['location']['localtime'], '%Y-%m-%d %H:%M')
                hour = date.hour
                in_holidays = holidays.IN()  # You can change this to your country, e.g., holidays.UK(), holidays.CA(), etc.
                is_holiday = date.date() in in_holidays
                weekday = date.strftime('%A')
                month = date.month
                year = date.year
                season = get_season_for_india(month)
                temperature = source_weather['current']['temp_c']
                weather_code = source_weather['current']['condition']['code']
                current_day = datetime.now().strftime("%A")
                coded_day = coded_day_mapping[current_day]

                # Zone (optional: you can determine based on your dataset or hardcode a value for testing)
                zone = 1  # Adjust based on your use case

                # Prepare input data for traffic prediction
                input_data = np.array([[coded_day, zone, weather_code, temperature]])
                scaled_data = scaler.transform(input_data)

                # Predict Traffic
                prediction = model.predict(scaled_data)
                new_input = {
                    "hour": hour,
                    "isholiday": is_holiday,
                    "weekday": weekday,
                    "month": month,
                    "year": year,
                    "season": season
                }
                prediction = predict_traffic_density(isholiday=is_holiday, hour=hour, weekday=weekday, month=month, year=year, season=season)

                # Save to MongoDB
                traffic_data = {
                    "source": source,
                    "destination": destination,
                    "hour": hour,
                    "isholiday": is_holiday,
                    "weekday": weekday,
                    "month": month,
                    "year": year,
                    "season": season,
                    "traffic_prediction": prediction,
                    "coordinates": coordinates,
                    "weather": source_weather
                }

                collection.insert_one(traffic_data)  # Insert into MongoDB

                st.session_state["traffic_prediction"] = prediction
                st.write(prediction)
            else:
                st.error("Weather data could not be fetched for source or destination.")
    else:
        st.error("Please provide valid API keys and location names!")

# Display the Route
if st.session_state["route_data"]:
    route_data = st.session_state["route_data"]
    coordinates = route_data["coordinates"]
    source_lat, source_lon = route_data["source_lat"], route_data["source_lon"]
    dest_lat, dest_lon = route_data["dest_lat"], route_data["dest_lon"]

    # Create a Map using Folium
    st.subheader("Route Map")
    m = folium.Map(location=[source_lat, source_lon], zoom_start=6)
    folium.Marker([source_lat, source_lon], popup="Source", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker([dest_lat, dest_lon], popup="Destination", icon=folium.Icon(color="red")).add_to(m)
    route = [(coord[1], coord[0]) for coord in coordinates]
    folium.PolyLine(route, color="blue", weight=5, opacity=0.8).add_to(m)
    st_folium(m, width=800, height=500)

# Display Weather Information
if st.session_state["weather_data"]:
    st.subheader("Weather Information")
    source_weather = st.session_state["weather_data"]["source"]
    destination_weather = st.session_state["weather_data"]["destination"]
    st.subheader("Weather Information at Source")
    
    st.write(f"**Location:** {source_weather['location']['name']}, {source_weather['location']['region']}, {source_weather['location']['country']}")
    st.write(f"**Condition:** {source_weather['current']['condition']['text']}")
    st.write(f"**Temperature:** {source_weather['current']['temp_c']} °C")
    st.write(f"**Wind Speed:** {source_weather['current']['wind_kph']} km/h")
    st.write(f"**Humidity:** {source_weather['current']['humidity']}%")
    st.write(f"**Pressure:** {source_weather['current']['pressure_mb']} hPa")
    st.write(f"**Visibility:** {source_weather['current']['vis_km']} km")

# Display Weather Information at Destination
    st.subheader("Weather Information at Destination")
    st.write(f"**Location:** {destination_weather['location']['name']}, {destination_weather['location']['region']}, {destination_weather['location']['country']}")
    st.write(f"**Condition:** {destination_weather['current']['condition']['text']}")
    st.write(f"**Temperature:** {destination_weather['current']['temp_c']} °C")
    st.write(f"**Wind Speed:** {destination_weather['current']['wind_kph']} km/h")
    st.write(f"**Humidity:** {destination_weather['current']['humidity']}%")
    st.write(f"**Pressure:** {destination_weather['current']['pressure_mb']} hPa")
    st.write(f"**Visibility:** {destination_weather['current']['vis_km']} km")

# Display Traffic Prediction
if st.session_state["traffic_prediction"]:
    st.subheader("Traffic Prediction")
    st.success(f"The predicted traffic level at the source is: {st.session_state['traffic_prediction']}")
