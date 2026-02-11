# 1. Use a lightweight Python base image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies (needed for some ML libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the project code
COPY . .

# 6. Expose the port FastAPI runs on
EXPOSE 8000

# 7. Command to run the API
CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]