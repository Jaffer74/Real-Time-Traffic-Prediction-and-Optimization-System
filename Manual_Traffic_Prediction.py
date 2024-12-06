import streamlit as st
import pandas as pd
import joblib
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://jafferali0741:b4Uk9KZ64sg4f4ar@cluster0.znrk9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)  # Use the actual MongoDB connection string here
db = client["traffic_db"]  # Database name (create it if it doesn't exist)
collection = db["outputs"] 

# Load the pre-trained model
model = joblib.load('final_model.pkl')

# Mapping for weekdays and seasons
weekday_map = {
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6
}
season_map = {
    'Spring': 0, 'Summer': 1, 'Fall': 2, 'Winter': 3
}

# Function to predict traffic density
def predict_traffic_density(hour, isholiday, weekday, month, year, season):
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

# Streamlit app layout
st.title("Traffic Density Prediction")

# Get user inputs
hour = st.slider('Hour of the day', 0, 23, 10)  # Default to 10 AM
isholiday = st.selectbox('Is it a holiday?', [True, False], index=1)  # Default to False
weekday = st.selectbox('Select the day of the week', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
month = st.slider('Month of the year', 1, 12, 11)  # Default to November
year = st.number_input('Year', min_value=2000, max_value=2100, value=2023)  # Default to 2023
season = st.selectbox('Select the season', ['Spring', 'Summer', 'Fall', 'Winter'])

# When the user clicks the "Predict" button
if st.button('Predict Traffic Density'):
    try:
        # Make the prediction
        result = predict_traffic_density(hour, isholiday, weekday, month, year, season)
        
        # Display the result
        st.write(f"Predicted Traffic Density: {result}")

        prediction_data = {
            "isholiday": isholiday,
            "hour": hour,
            "weekday": weekday,
            "month": month,
            "year": year,
            "season": season,
            "predicted_traffic_level": result
        }

        # Insert the data into MongoDB
        collection.insert_one(prediction_data)
        st.write("Prediction data has been saved to the database.")
    
    except Exception as e:
        # Handle errors gracefully
        st.error(f"Error: {e}")
