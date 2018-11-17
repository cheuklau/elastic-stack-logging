# Official Java 8 image
# Note: To debug
# 1) kubectl describe pods logstash
# 2) Copy docker container ID from step 1 (it should be docker://<container-ID>)
# 3) docker exec -it <container-ID> bash
# 4) vi logstash.conf to change the configuration file
# 5) logstash-6.5.0/bin/logstash -f logstash.conf
# 6) Configuration file is set up to display to stdout, so use that to debug
FROM java:8

# Copy Logstash configuration file
COPY logstash.conf logstash.conf

# Copy Logstash source code
COPY logstash-6.5.0/ logstash-6.5.0/

# Download VI to debug
RUN apt-get update && apt-get -y install vim

# Run sleep command so we have time to debug running container
CMD ["sleep", "1d"]
