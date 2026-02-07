# Use the official Bun image
FROM oven/bun:1

WORKDIR /app

# Copy package files
COPY package.json bun.lock ./

# Install dependencies using Bun
RUN bun install

# Copy application code
COPY . .

# Expose Port 3000
EXPOSE 3000

# Start Nuxt in Development mode
CMD ["bun", "--bun" ,"run", "dev", "-o"]