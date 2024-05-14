# frontend/Dockerfile
FROM node:latest
WORKDIR /app

# Copy package.json and possibly package-lock.json
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy the rest of your frontend codebase into the image
COPY . .

# Build the project (if necessary)
RUN npm run build

# Install a server to serve the built files
RUN npm install -g serve

# Command to serve the built application
CMD ["serve", "-s", "dist", "-l", "3000"]
