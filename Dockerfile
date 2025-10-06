# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies (though none are required for this project)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY capture_server.py .
COPY job-tracker.md .

# Create a directory for the data files
RUN mkdir -p /app/data

# Expose the port the server will run on
EXPOSE 8766

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the server
CMD ["python", "capture_server.py"]
