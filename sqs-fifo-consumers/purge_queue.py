from essentials import sqs_client, sqs_url

client = sqs_client()
sqs_uri = sqs_url()

client.purge_queue(QueueUrl=sqs_uri)
