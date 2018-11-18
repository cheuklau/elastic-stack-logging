# Elastic Stack Logging

## Overview 

This repository will test the Elastic Stack for centralized logging. The components are:

* Microservice
    + Generates three different types:
        1. `INFO` - single line log
        2. `WARN` - multi-line stack trace
        3. `ERROR` - multi-line stack trace
    + User specifies the following parameters in `k8s/microservice-filebeat/deployment.yaml`
        1. `WAIT_TIME` - time between logs in seconds
        2. `PER_ERR` - percent chance log is an ERROR
        3. `PER_WARN` - percent chance log is a WARN
2. Filebeat
    + Monitors the logfile written by the microservice and sends the data to Logstash
    + This will be monitored as a sidecar to the microservice container
    + Filebeat will monitor `/logtest/logfile` which is within a shared volume
    + Filebeat is configured to handle multi-line events i.e., Java stack traces
3. Logstash
    + Ingests the log data from Filebeat
    + Parses out the event status i.e., `INFO`, `WARN` or `ERROR`
    + Send the data as JSON format to Elasticsearch for indexing
4. Elasticsearch
    + Indexes the data from Logstash
5. Kibana
    + Visualizes the data from Elasticsearch
    + Open `localhost:30000` in any browser to view Kibana UI
    + Go to `Timelion` tab and enter `.es(index="elk-info*").label(INFO), .es(index="elk-warn*").label(WARN), .es(index="elk-error-*").label(ERROR)`

![Fig 1: Kibana UI showing rate of log messages by status](/images/logmessages.png)

## Build Instructions

The Docker images should be up to date in `cheuklau/` Docker Hub. To build simply go to each direction in `/k8s` and execute:

```
kubectl create -f deployment.yaml
kubectl create -f service.yaml
```

## Debug Instructions

To debug Logstash parsing go to `/k8s/logstash_debug` and execute:

```
kubectl delete deployment logstash
kubectl create -f deployment.yaml
kubectl create -f service.yaml
```

Get the Docker container ID by:

```
kubectl describe pod logstash (then copy the Docker container ID)
docker exec -it <Docker-container-ID> bash
```

Change the configuration file `logstash.conf` as necessary then run Logstash:

```
Logstash-*/bin/logstash -f logstash.conf
```

The configuration file has output directed as `stdout`.