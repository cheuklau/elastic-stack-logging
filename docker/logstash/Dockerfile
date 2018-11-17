# Official Elastic Logstash image
FROM docker.elastic.co/logstash/logstash:6.4.2

# Remove default Logstash pipeline file
RUN rm -f /usr/share/logstash/pipeline/logstash.conf

# Add Logstash pipeline file to image
ADD logstash.conf /usr/share/logstash/pipeline/logstash.conf

# Add Logstash configuration file to image
ADD logstash.yml /usr/share/logstash/config/logstash.yml
