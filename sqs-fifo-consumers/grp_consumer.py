import sys
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from essentials import sqs_client, sqs_url

client = sqs_client()
sqs_uri = sqs_url()


def queue_poller(**kwargs):
    client = kwargs.get('client', None)
    sqs_uri = kwargs.get('sqs_uri', None)
    response = client.receive_message(
        QueueUrl=sqs_uri,
        MaxNumberOfMessages=10,
    )
    return response.get('Messages', [])


def batch_processor(client, queue_uri):
    while True:
        messages = queue_poller(client=client, sqs_uri=sqs_uri)
        if not messages:
            break
        for msg in messages:
            process_msg(client, msg, queue_uri)


def process_msg(client, msg, queue_uri):
    receipt_handle = msg['ReceiptHandle']
    time.sleep(0.001)
    client.delete_message(
        QueueUrl=queue_uri,
        ReceiptHandle=receipt_handle
    )
    opp_id = json.loads(msg['Body'])['opportunity_id']
    logging.info(f'Received and deleted message: {opp_id}')


def prime(**kwargs):
    threads = kwargs.get('threads', 8)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        pool = {
            executor.submit(
                batch_processor,
                kwargs['client'],
                kwargs['sqs_uri'],
            ): _ for _ in range(threads)
        }

    for future_ in as_completed(pool):
        logging.info(future_.result())


if __name__ == '__main__':
    t0 = time.time()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s: %(levelname)s: %(message)s'
    )

    prime(
        client=client,
        sqs_uri=sqs_uri,
        threads=10,
    )

    t1 = time.time()
    logging.info(f'Total Time Taken: {round(t1-16-t0, 1)}')
