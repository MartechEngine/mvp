# --- Stage 1: Dependency Installation ---
FROM node:18-alpine AS deps
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm ci

# --- Stage 2: Builder ---
# This stage builds the Next.js application.
FROM node:18-alpine AS builder
WORKDIR /usr/src/app
COPY --from=deps /usr/src/app/node_modules ./node_modules
COPY . .

# Build the Next.js application for production
RUN npm run build

# --- Stage 3: Final Production Image ---
FROM node:18-alpine
WORKDIR /usr/src/app

# Create a dedicated, non-root user for security
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy only the necessary production artifacts from the builder stage
COPY --from=builder /usr/src/app/public ./public
COPY --from=builder --chown=nextjs:nodejs /usr/src/app/.next ./.next
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app/package.json ./package.json

# Switch to the non-root user
USER nextjs

# Expose the port the application will run on
EXPOSE 3000
ENV PORT 3000

# The default command to run the application in a production environment.
# This will be used in production. Docker Compose will override this for local development.
CMD ["npm", "start"]
