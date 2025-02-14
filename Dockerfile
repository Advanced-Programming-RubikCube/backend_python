# Use base image python:3.9-alpine
# Set working directory to /app
# Copy requirements.txt to /app
# Install dependencies from requirements.txt
# Copy all files from current directory to /app
# Expose port 8000
# Run the application using uvicorn
# CMD ["uvicorn", "app.main:app", "--host", "

FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
