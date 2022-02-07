# Scripts to publish and consume messages from SQS FIFO

- Created a publisher script which creates and pushes messages to SQS.
- Created two consumers to compare how `ThreadPoolExecutor` and `EventLoop` perform. For large sample EventLoop was little better than ThreadPoolExecutor.

Conducted two samples tests:

**1M - 10% of actual target**
- EventLoop:
> 16116.3 seconds which is equivalent to 4.4 hours
> Estimation for 10M - 45 hours
- ThreadPoolExecutor:
> 16936.1 seconds which is equivalent to 4.7 hours
> Estimation for 10M - 47 hours

**100k - 1% of actual target**
- EventLoop:
> 1673.4 seconds which is equivalent to 46 minutes
> Estimation for 10M - 46 hours
- ThreadPoolExecutor:
> 1681.4 seconds which is equivalent to 46 minutes
> Estimation for 10M - 46 hours


For low number of messages any approach is working fine.
For FIFO queues, it is suggested to have different MessageGroupId which helps us to spawn concurrent processes to consumer messages faster and in time.
