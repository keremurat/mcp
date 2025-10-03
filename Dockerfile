FROM python:3.12-slim

WORKDIR /app

# Set environment variables for HTTP transport
ENV TRANSPORT=http
ENV PORT=8081
ENV PYTHONUNBUFFERED=1

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 8081

# Run the server
CMD ["python", "server.py"]