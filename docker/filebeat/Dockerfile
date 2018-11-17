# Official Elastic Filebeat image
FROM docker.elastic.co/beats/filebeat:6.4.2

# Copy Filebeat configuration file to image
# Note: Filebeat reads all log files from /logtest/*
#       Filebeat sends data to logstash:5044
COPY filebeat.yml /usr/share/filebeat/filebeat.yml

# Change ownership of configuration file to root user, Filbeat group
USER root
RUN chown root:filebeat /usr/share/filebeat/filebeat.yml

# Switch to Filebeat user
USER filebeat
