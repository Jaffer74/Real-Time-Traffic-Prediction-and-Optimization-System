import streamlit as st
import pandas as pd
from pymongo import MongoClient
import datetime

# MongoDB Atlas Connection - Replace <db_password> with your actual password
MONGO_URI = "mongodb+srv://jafferali0741:b4Uk9KZ64sg4f4ar@cluster0.znrk9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["traffic_db"]
collection = db["outputs"]

# Title of the page
st.title("Traffic Prediction Data")

# Fetch data from MongoDB
def fetch_data():
    try:
        # Fetch all data from the predictions collection
        data = list(collection.find({}))
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# Fetch and display data
data = fetch_data()

# Check if there is data
if data:
    # Convert MongoDB data to a Pandas DataFrame for easy manipulation
    df = pd.DataFrame(data)
    
    # Clean up the DataFrame (remove MongoDB-specific fields)
    df.drop(columns=["_id"], inplace=True)  # Drop the _id field
    
    # Display the data in a table format
    st.subheader("Predictions Overview")
    st.dataframe(df)
else:
    st.write("No prediction data available.")
