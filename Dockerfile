# Use the official Python image as the base image
FROM python:3.10.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install required packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your application
CMD python /app/rng_app.py

# Expose port 2224
EXPOSE 2224


