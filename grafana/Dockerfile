# Builder to install the MongoDB datasource plugin (free and open-source)
FROM alpine:latest AS builder

RUN apk add --no-cache wget unzip

RUN wget https://github.com/haohanyang/mongodb-datasource/releases/download/v0.3.1/haohanyang-mongodb-datasource-0.3.1.zip -O /tmp/mongodb-datasource.zip && \
    unzip /tmp/mongodb-datasource.zip -d /tmp/mongodb-datasource

# Grafana
FROM grafana/grafana:latest

# Copy the unzipped plugin from the builder stage
COPY --from=builder /tmp/mongodb-datasource/haohanyang-mongodb-datasource /var/lib/grafana/plugins/haohanyang-mongodb-datasource

# Set environment variable to allow loading unsigned plugins
ENV GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS=haohanyang-mongodb-datasource

# Make port 3000 available to the world outside this container
EXPOSE 3000