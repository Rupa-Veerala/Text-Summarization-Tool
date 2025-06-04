# Use a Python base image
FROM python:3.10-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies including tkinter and X11
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    xauth \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Copy application code
COPY . .

# Command to run the application
CMD ["python3", "text_summarizer.py"]
