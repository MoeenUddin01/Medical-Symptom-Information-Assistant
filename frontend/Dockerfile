# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Builder - Build the React application
# =============================================================================
FROM node:20-alpine AS builder

# Set working directory for the application build
WORKDIR /app

# Copy package files first for better Docker layer caching
COPY package.json package-lock.json ./

# Install dependencies using npm ci for reproducible, exact versions
RUN npm ci

# Copy the rest of the frontend source code
COPY . .

# Accept the backend URL as a build argument for Vite to embed at build time
ARG VITE_BACKEND_URL=http://localhost:8000
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL

# Build the production-ready React application
RUN npm run build

# =============================================================================
# Stage 2: Production - Serve with Nginx
# =============================================================================
FROM nginx:alpine AS production

# Copy the built React application files into Nginx web root
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration for SPA routing
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for HTTP traffic
EXPOSE 80

# Health check to verify Nginx is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Run Nginx in the foreground (no daemon mode)
CMD ["nginx", "-g", "daemon off;"]