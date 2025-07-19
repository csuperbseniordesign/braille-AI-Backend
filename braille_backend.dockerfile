# python lightweight image
FROM python:3.13.1-slim

# set working dir in container
WORKDIR /app

# copy & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code base into the container
COPY ./app ./app

# Start the server when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]