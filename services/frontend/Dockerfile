# ./services/frontend/Dockerfile

# Pull official base image
FROM node:lts-alpine

# Set working directory
WORKDIR /app

# Install Vue CLI globally
RUN npm install -g @vue/cli

# Install dependencies
COPY package*.json ./
RUN npm install


# Copy project files
COPY . .

# Build the app
RUN npm run build

# Expose port
EXPOSE 8080

# Start the app
CMD [ "npm", "run", "serve" ]