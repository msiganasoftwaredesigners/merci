# Use official Python image
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production 
ENV DJANGO_SETTINGS_MODULE=msigana_ecommerce.settings.production


# Set the working directory
WORKDIR /var/www/merci

# Install system dependencies and Node.js 21
RUN apt-get update && \
    apt-get install -y curl gnupg libpq-dev gcc libffi-dev rustc && \
    curl -fsSL https://deb.nodesource.com/setup_21.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Confirm Node.js and npm versions (optional, good for debugging)
RUN node -v && npm -v

# Ensure environment variables from .env are loaded
COPY .env.merci /var/www/merci/.env.merci


# Install Python dependencies
COPY requirements.txt /var/www/merci/
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . /var/www/merci/

RUN chown -R www-data:www-data /var/www/merci

# Install Node.js project dependencies
RUN cd theme && npm install


# Create static folder to avoid warning
RUN mkdir -p /var/www/merci/msigana_ecommerce/static

# Expose port
EXPOSE 8000


# Copy Gunicorn config
COPY gunicorn.conf.py /var/www/merci/

# Run Gunicorn with the config file
CMD ["gunicorn", "--config", "gunicorn.conf.py", "msigana_ecommerce.wsgi:application"]
