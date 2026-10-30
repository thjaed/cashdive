FROM python:3.12-slim

WORKDIR /app

# Install Node.js and Nginx
RUN apt-get update && \
    apt-get install -y curl nginx && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install frontend dependencies
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm ci

# Copy the rest of the project
COPY . .

# Build Next.js
RUN cd frontend && npm run build

# Nginx configuration
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 3000

CMD ["/start.sh"]