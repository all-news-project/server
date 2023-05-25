# Use a base Linux image
FROM ubuntu:latest

# Copy the shell bash file to the Docker image
COPY run.sh /app/run.sh

# Set the working directory
WORKDIR /app

# Make the shell bash file executable
RUN chmod +x run.sh

# Run the shell bash file when the container starts
CMD ["./run.sh"]