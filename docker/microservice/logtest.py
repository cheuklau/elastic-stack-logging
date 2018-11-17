import time
import os
import datetime
from random import randint


def logger(log_dir, wait_time, per_warn, per_err):
    ''' Write INFO, WARN and ERROR to log

    Write INFO, WARN and ERROR logs based on user-specified rates.

    Source for log formats: https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Error+Handling+and+Logging

    Args:
        log_dir = log directory
        wait_time = time between logs (seconds)
        per_warn = percent of logs that are WARN
        per_err = percent of logs that are ERROR

    Returns:
        None
    '''

    # INFO message without timestamp
    info_msg = " INFO [Processor] [kafka-network-thread-10251-1] [kafka-server] [] Closing socket connection to /172.17.198.21.\n"

    # WARN message without timestamp
    warn_msg = (" WARN kafka.client.ClientUtils$  - Fetching topic metadata with correlation id 0 for topics [Set(test-topic)] from broker [id:0,host:localhost,port:1025] failed\n"+
    "\tjava.net.ConnectException: Connection refused\n"+
    "\tat sun.nio.ch.Net.connect0(Native Method)\n"+
    "\tat sun.nio.ch.Net.connect(Net.java:465)\n"+
    "\tat sun.nio.ch.Net.connect(Net.java:457)\n"+
    "\tat sun.nio.ch.SocketChannelImpl.connect(SocketChannelImpl.java:639)\n"+
    "\tat kafka.network.BlockingChannel.connect(BlockingChannel.scala:57)\n"+
    "\tat kafka.producer.SyncProducer.connect(SyncProducer.scala:146)\n"+
    "\tat kafka.producer.SyncProducer.getOrMakeConnection(SyncProducer.scala:161)\n"+
    "\tat kafka.producer.SyncProducer.kafka$producer$SyncProducer$$doSend(SyncProducer.scala:68)\n"+
    "\tat kafka.producer.SyncProducer.send(SyncProducer.scala:112)\n"+
    "\tat kafka.client.ClientUtils$.fetchTopicMetadata(ClientUtils.scala:53)\n"+
    "\tat kafka.producer.BrokerPartitionInfo.updateInfo(BrokerPartitionInfo.scala:82)\n"+
    "\tat kafka.producer.async.DefaultEventHandler$$anonfun$handle$1.apply$mcV$sp(DefaultEventHandler.scala:69)\n"+
    "\tat kafka.utils.Utils$.swallow(Utils.scala:186)\n"+
    "\tat kafka.utils.Logging$class.swallowError(Logging.scala:105)\n"+
    "\tat kafka.utils.Utils$.swallowError(Utils.scala:45)\n"+
    "\tat kafka.producer.async.DefaultEventHandler.handle(DefaultEventHandler.scala:69)\n"+
    "\tat kafka.producer.Producer.send(Producer.scala:74)\n"+
    "\tat kafka.javaapi.producer.Producer.send(Producer.scala:32)\n")

    # ERROR message without timestamp
    err_msg = (" ERROR kafka.producer.SyncProducer  - Producer connection to localhost:1025 unsuccessful\n"+
    "\tjava.net.ConnectException: Connection refused\n"+
    "\tat sun.nio.ch.Net.connect0(Native Method)\n"+
    "\tat sun.nio.ch.Net.connect(Net.java:465)\n"+
    "\tat sun.nio.ch.Net.connect(Net.java:457)\n"+
    "\tat sun.nio.ch.SocketChannelImpl.connect(SocketChannelImpl.java:639)\n"+
    "\tat kafka.network.BlockingChannel.connect(BlockingChannel.scala:57)\n"+
    "\tat kafka.producer.SyncProducer.connect(SyncProducer.scala:146)\n"+
    "\tat kafka.producer.SyncProducer.getOrMakeConnection(SyncProducer.scala:161)\n"+
    "\tat kafka.producer.SyncProducer.kafka$producer$SyncProducer$$doSend(SyncProducer.scala:68)\n"+
    "\tat kafka.producer.SyncProducer.send(SyncProducer.scala:112)\n"+
    "\tat kafka.client.ClientUtils$.fetchTopicMetadata(ClientUtils.scala:53)\n"+
    "\tat kafka.producer.BrokerPartitionInfo.updateInfo(BrokerPartitionInfo.scala:82)\n"+
    "\tat kafka.producer.async.DefaultEventHandler$$anonfun$handle$1.apply$mcV$sp(DefaultEventHandler.scala:69)\n"+
    "\tat kafka.utils.Utils$.swallow(Utils.scala:186)\n"+
    "\tat kafka.utils.Logging$class.swallowError(Logging.scala:105)\n"+
    "\tat kafka.utils.Utils$.swallowError(Utils.scala:45)\n"+
    "\tat kafka.producer.async.DefaultEventHandler.handle(DefaultEventHandler.scala:69)\n"+
    "\tat kafka.producer.Producer.send(Producer.scala:74)\n"+
    "\tat kafka.javaapi.producer.Producer.send(Producer.scala:32)\n")

    # Create log directory if it does not exist
    if not os.path.isdir(log_dir):
    	os.mkdir(log_dir)

    # Path to logfile
    log_path = log_dir + '/logfile'

    # Start writing logs
    while True:

        # Write a log entry
        rand_int = randint(1, 100)
        log = open(log_path, 'a+')
        
        if rand_int <= per_warn:
            log.write(str(datetime.datetime.now()) + warn_msg)

        elif per_warn < rand_int < per_warn + per_err: 
            log.write(str(datetime.datetime.now()) + err_msg)

        else:
            log.write(str(datetime.datetime.now()) + info_msg)

        # Close logfile for next write
        log.close()

        # Wait the specified time before next log
        time.sleep(wait_time)


if __name__ == '__main__':

    # Log directory
    log_dir = 'logtest'

    # Wait time between logs (seconds)
    wait_time = int(os.environ['WAIT_TIME'])

    # Percent of logs that are WARN
    per_warn = int(os.environ['PER_WARN'])

    # Percent of logs that are ERROR
    per_err = int(os.environ['PER_ERR'])

    # Start logger
    logger(log_dir, wait_time, per_warn, per_err)
