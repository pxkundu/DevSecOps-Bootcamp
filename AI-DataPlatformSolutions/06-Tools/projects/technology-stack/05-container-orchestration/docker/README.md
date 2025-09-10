# Docker - Container Platform

## 🐳 Overview
Docker is a containerization platform that allows you to package applications and their dependencies into lightweight, portable containers. This section provides practical guides for using Docker in DevSecOps workflows.

## 📁 Directory Structure

```
docker/
├── README.md
├── dockerfiles/
│   ├── nodejs/
│   ├── python/
│   ├── java/
│   └── multi-stage/
├── compose/
│   ├── development/
│   ├── staging/
│   └── production/
├── images/
│   ├── base/
│   ├── application/
│   └── utilities/
└── scripts/
    ├── build.sh
    ├── run.sh
    └── cleanup.sh
```

## 🛠️ Essential Dockerfiles

### 1. Node.js Application
```dockerfile
# dockerfiles/nodejs/Dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build the application
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### 2. Python Application
```dockerfile
# dockerfiles/python/Dockerfile
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### 3. Java Application
```dockerfile
# dockerfiles/java/Dockerfile
FROM openjdk:17-jdk-slim AS base

# Set working directory
WORKDIR /app

# Copy Maven wrapper and pom.xml
COPY .mvn/ .mvn
COPY mvnw pom.xml ./

# Make Maven wrapper executable
RUN chmod +x mvnw

# Download dependencies
RUN ./mvnw dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN ./mvnw clean package -DskipTests

# Production stage
FROM openjdk:17-jre-slim AS production

# Create app user
RUN addgroup --system --gid 1001 appgroup
RUN adduser --system --uid 1001 --gid 1001 appuser

# Set working directory
WORKDIR /app

# Copy the built JAR file
COPY --from=base /app/target/*.jar app.jar

# Change ownership
RUN chown appuser:appgroup app.jar

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### 4. Multi-Stage Build
```dockerfile
# dockerfiles/multi-stage/Dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine AS production

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy SSL certificates
COPY ssl/ /etc/nginx/ssl/

# Expose ports
EXPOSE 80 443

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

## 🐙 Docker Compose Configurations

### 1. Development Environment
```yaml
# compose/development/docker-compose.yml
version: '3.8'

services:
  web:
    build:
      context: ../../
      dockerfile: dockerfiles/nodejs/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    volumes:
      - ../../:/app
      - /app/node_modules
    depends_on:
      - db
      - redis
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

### 2. Production Environment
```yaml
# compose/production/docker-compose.yml
version: '3.8'

services:
  web:
    image: myapp:latest
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - db
      - redis
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

## 🚀 Deployment Scripts

### 1. Build Script
```bash
#!/bin/bash
# scripts/build.sh

set -e

# Configuration
IMAGE_NAME=${1:-myapp}
TAG=${2:-latest}
DOCKERFILE=${3:-dockerfiles/nodejs/Dockerfile}
BUILD_CONTEXT=${4:-.}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Building Docker image: $IMAGE_NAME:$TAG${NC}"

# Build the image
docker build \
    -f "$DOCKERFILE" \
    -t "$IMAGE_NAME:$TAG" \
    -t "$IMAGE_NAME:latest" \
    "$BUILD_CONTEXT"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Image built successfully${NC}"
    
    # Show image details
    echo "Image details:"
    docker images "$IMAGE_NAME"
else
    echo -e "${RED}Image build failed${NC}"
    exit 1
fi

# Optional: Push to registry
if [ "$PUSH_TO_REGISTRY" = "true" ]; then
    echo "Pushing image to registry..."
    docker push "$IMAGE_NAME:$TAG"
    docker push "$IMAGE_NAME:latest"
fi
```

### 2. Run Script
```bash
#!/bin/bash
# scripts/run.sh

set -e

# Configuration
IMAGE_NAME=${1:-myapp}
TAG=${2:-latest}
CONTAINER_NAME=${3:-myapp-container}
PORT=${4:-3000}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running Docker container: $CONTAINER_NAME${NC}"

# Stop and remove existing container if it exists
if docker ps -a --format 'table {{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    echo "Stopping existing container..."
    docker stop "$CONTAINER_NAME"
    docker rm "$CONTAINER_NAME"
fi

# Run the container
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$PORT:3000" \
    -e NODE_ENV=production \
    "$IMAGE_NAME:$TAG"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Container started successfully${NC}"
    echo "Container ID: $(docker ps -q --filter name=$CONTAINER_NAME)"
    echo "Access the application at: http://localhost:$PORT"
else
    echo -e "${RED}Container start failed${NC}"
    exit 1
fi

# Show container logs
echo "Container logs:"
docker logs "$CONTAINER_NAME"
```

### 3. Cleanup Script
```bash
#!/bin/bash
# scripts/cleanup.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Cleaning up Docker resources${NC}"

# Stop and remove all containers
echo "Stopping and removing containers..."
docker stop $(docker ps -aq) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

# Remove unused images
echo "Removing unused images..."
docker image prune -f

# Remove unused volumes
echo "Removing unused volumes..."
docker volume prune -f

# Remove unused networks
echo "Removing unused networks..."
docker network prune -f

# System cleanup
echo "Performing system cleanup..."
docker system prune -f

echo -e "${GREEN}Cleanup completed${NC}"

# Show remaining resources
echo "Remaining resources:"
echo "Containers: $(docker ps -aq | wc -l)"
echo "Images: $(docker images -q | wc -l)"
echo "Volumes: $(docker volume ls -q | wc -l)"
echo "Networks: $(docker network ls -q | wc -l)"
```

## 📋 Best Practices

### 1. Dockerfile Best Practices
- Use multi-stage builds to reduce image size
- Use specific base image tags, not `latest`
- Minimize the number of layers
- Use `.dockerignore` to exclude unnecessary files
- Run containers as non-root user
- Use health checks
- Optimize layer caching

### 2. Security Best Practices
- Use minimal base images
- Scan images for vulnerabilities
- Keep base images updated
- Use secrets management
- Implement least privilege access
- Regular security audits

### 3. Performance Best Practices
- Use appropriate base images
- Optimize layer caching
- Use multi-stage builds
- Minimize image size
- Use appropriate resource limits
- Monitor container performance

### 4. Development Best Practices
- Use Docker Compose for local development
- Implement hot reloading
- Use volume mounts for development
- Separate development and production configurations
- Use environment variables for configuration

## 🧪 Hands-On Examples

### Example 1: Build and Run Node.js Application
```bash
# Build the image
./scripts/build.sh myapp latest dockerfiles/nodejs/Dockerfile

# Run the container
./scripts/run.sh myapp latest myapp-container 3000

# Check container status
docker ps

# View logs
docker logs myapp-container

# Stop container
docker stop myapp-container
```

### Example 2: Multi-Service Development Environment
```bash
# Start development environment
cd compose/development
docker-compose up -d

# View logs
docker-compose logs -f

# Scale services
docker-compose up -d --scale web=3

# Stop services
docker-compose down
```

### Example 3: Production Deployment
```bash
# Build production image
./scripts/build.sh myapp v1.0.0 dockerfiles/nodejs/Dockerfile

# Deploy to production
cd compose/production
docker-compose up -d

# Monitor services
docker-compose ps
docker-compose logs -f
```

## 📚 Learning Resources

### Official Documentation
- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### Community Resources
- [Docker Hub](https://hub.docker.com/)
- [Docker Samples](https://github.com/docker/awesome-compose)
- [Stack Overflow Docker](https://stackoverflow.com/questions/tagged/docker)

---

**Ready to master Docker?** Start with the basic Node.js Dockerfile and work your way up to complex multi-service applications!
