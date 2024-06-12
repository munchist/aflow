import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from cors import CORS, cross_origin
import json

app = CORS(st.wsgi_app)

# Function to create a visualization
def create_visualization(data):
    st.title("Data Visualization")
    
    # Check the type of data received and display accordingly
    if isinstance(data, pd.DataFrame):
        st.write("Data is a DataFrame:")
        st.write(data)

        # Choose appropriate chart based on data type
        if data.shape[1] >= 2:  # At least two columns for a chart
            st.bar_chart(data)
        else:
            st.table(data)
    
    elif isinstance(data, dict):
        st.write("Data is a dictionary:")
        st.json(data)
    
    elif isinstance(data, list):
        st.write("Data is a list:")
        st.write(data)
    
    else:
        st.write("Received unsupported data type.")

# Endpoint to handle data from Node.js server
@app.post("/create-visualization")
@cross_origin()
def create_visualization_endpoint():
    data = st.request.body
    try:
        data = json.loads(data)  # Try to parse as JSON
    except json.JSONDecodeError:
        st.error("Error: Invalid JSON data received.")
        return

    if isinstance(data, str):
        # Attempt to convert to DataFrame if it's a string representation
        try:
            data = pd.read_json(data) 
        except ValueError:
            st.error("Error: Could not convert string to DataFrame.")
            return

    create_visualization(data)

    # Return full visualization URL
    return {"url": st.secrets["url"]} if st.secrets["url"] else {"url": f"{st.get_option('server.baseUrlPath')}/"} 


if __name__ == '__main__':
    st.set_page_config(layout="wide")

    if st.request.method == "POST" and st.request.path == "/create-visualization":
        create_visualization_endpoint() 
    else:
        # Display default visualization
        st.write("Please send POST requests to /create-visualization with data in the body.") 
