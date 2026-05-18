# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Builder - Install dependencies and download models
# =============================================================================
FROM python:3.11-slim AS builder

# Set working directory for dependency installation
WORKDIR /app

# Copy only requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Download and install the scispacy NER model for medical entity extraction
# This bakes the model into the image so it's available at runtime
RUN python -m spacy download en_core_sci_sm

# =============================================================================
# Stage 2: Production - Minimal runtime image
# =============================================================================
FROM python:3.11-slim AS production

# Set working directory for the application
WORKDIR /app

# Copy installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the backend source code into the container
COPY backend/ ./backend/

# Create a non-root user for security isolation
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Switch to non-root user to run the application
USER appuser

# Disable bytecode generation to keep image clean
ENV PYTHONDONTWRITEBYTECODE=1
# Enable unbuffered output for real-time log visibility
ENV PYTHONUNBUFFERED=1

# Expose the FastAPI server port
EXPOSE 8000

# Health check to verify the server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]