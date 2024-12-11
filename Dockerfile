# Use the official Python image as the base
FROM python:3.12-slim-bullseye as base

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=true \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    QR_CODE_DIR=/myapp/qr_codes

# Set the working directory
WORKDIR /myapp

# Install dependencies only when needed
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install the dependencies
COPY ./requirements.txt /myapp/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Create a non-root user and switch to it for better security
RUN useradd -m myuser
USER myuser

# Copy the application code with the correct permissions
COPY --chown=myuser:myuser . /myapp

# Expose the application port
EXPOSE 8000

# EntryPoint: Launch FastAPI with uvicorn
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
