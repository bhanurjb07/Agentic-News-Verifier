# Standard python image
FROM python:3.10

WORKDIR /app

# Copy dependencies first for caching
COPY pyproject.toml . 
# Agar requirements.txt hai toh: COPY requirements.txt .

RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Copy the server folder
COPY . .

# Set the port
EXPOSE 7860

# Command to run the server
CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
