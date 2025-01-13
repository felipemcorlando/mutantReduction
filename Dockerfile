# Base Image
FROM python:3.8-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the tests folder
COPY tests/ /app/tests/

# Copy project files into the container
COPY . .

# Add the src directory to the PYTHONPATH
ENV PYTHONPATH="/app/src"
ENV PYTHONPATH="/app/src/featureExtraction/code2vec:/app/src:${PYTHONPATH}"


# Expose port (if needed for debugging or API services)
EXPOSE 8000

# Command to run (can be adjusted later for specific scripts)
CMD ["python", "main.py"]
