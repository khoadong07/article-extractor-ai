import streamlit as st
import requests
import json
import time

# Streamlit interface
st.title("Article Extractor")

# Input for URL
url = st.text_area("Enter the URL")

# Variable to store the state if the request is successful
article_info = None

# Button to send the request to the API
if st.button("Run"):
    if url:
        try:
            # Start measuring time
            start_time = time.time()

            # Send POST request to the FastAPI
            response = requests.post("http://127.0.0.1:8000/api/extract-article", json={"url": url})
            response.raise_for_status()  # Raise an error if the request failed
            article_info = response.json()  # Get the JSON response

            # End measuring time
            end_time = time.time()
            elapsed_time = end_time - start_time  # Calculate the elapsed time

            # Display the processing time
            st.write(f"Processing Time: {elapsed_time:.2f} seconds")

            # Display the extracted article information in JSON format
            st.subheader("Article Information:")
            st.json(article_info)



        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
            article_info = None
    else:
        st.error("Please enter a valid URL.")
