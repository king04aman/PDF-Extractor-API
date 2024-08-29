# Define the base Python image version
ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1  # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED=1  # Ensure output is not buffered

# Set the working directory inside the container
WORKDIR /app

# Create a non-root user to run the application
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-cache-dir -r requirements.txt

# Switch to the non-root user
USER appuser

# Copy the application code into the container
COPY --chown=appuser:appuser app/ .

# Expose the port the application will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
