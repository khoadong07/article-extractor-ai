# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI is running on
EXPOSE 8000

# Expose the port Streamlit is running on
EXPOSE 8501

# Command to run both FastAPI with Gunicorn (for multiple workers) and Streamlit
CMD ["sh", "-c", "gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app & streamlit run app.py --server.port 8501 --server.enableCORS false"]
