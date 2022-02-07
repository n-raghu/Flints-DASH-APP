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


def process_msg(client, msg, queue_uri):
    receipt_handle = msg['ReceiptHandle']
    time.sleep(0.001)
    client.delete_message(
        QueueUrl=queue_uri,
        ReceiptHandle=receipt_handle
    )
    opp_id = json.loads(msg['Body'])['opportunity_id']
    logging.info(f'Received and deleted message: {opp_id}')


def process_msgs(**kwargs):
    threads = kwargs.get('threads', 8)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        pool = {
            executor.submit(
                process_msg,
                kwargs['client'],
                msg,
                kwargs['sqs_uri'],
            ): msg for msg in kwargs['messages']
        }

    for future_ in as_completed(pool):
        logging.info(future_.result())


if __name__ == '__main__':
    t0 = time.time()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s: %(levelname)s: %(message)s'
    )
    while True:
        messages = queue_poller(client=client, sqs_uri=sqs_uri)
        if not messages:
            t1 = time.time()
            logging.info('No messages in Queue')
            logging.info(f'Total Time Taken: {round(t1-16-t0, 1)}')
            sys.exit()

        process_msgs(
            messages=messages,
            client=client,
            sqs_uri=sqs_uri,
            threads=16
        )
