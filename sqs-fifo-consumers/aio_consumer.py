import sys
import json
import time
import logging
import asyncio as aio
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from essentials import sqs_client, sqs_url

sqs_uri = sqs_url()
client = sqs_client()
EXC = ThreadPoolExecutor(max_workers=16)


def queue_poller(**kwargs):
    client = kwargs.get('client', None)
    sqs_uri = kwargs.get('sqs_uri', None)
    response = client.receive_message(
        QueueUrl=sqs_uri,
        MaxNumberOfMessages=10,
    )
    return response.get('Messages', [])


async def process_msg(client, msg, queue_uri, loop, exc=EXC):
    await aio.sleep(0.001)
    receipt_handle = msg['ReceiptHandle']
    await loop.run_in_executor(
        exc,
        partial(
            client.delete_message,
            QueueUrl=queue_uri,
            ReceiptHandle=receipt_handle,
        )
    )
    opp_id = json.loads(msg['Body'])['opportunity_id']
    logging.info(f'Received and deleted message: {opp_id}')


async def process_msgs(**kwargs):
    messages = kwargs.pop('messages', [])
    loop = kwargs.pop('loop', None)
    if not loop:
        sys.exit('Async Loop does not exists')

    logging.info(f'Received {len(messages)} Messages')
    tasks = [process_msg(kwargs['client'], msg, kwargs['sqs_uri'], loop) for msg in messages]
    await aio.gather(*tasks)


if __name__ == '__main__':
    t0 = time.time()
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: %(levelname)s: %(message)s'
    )
    loop = aio.get_event_loop()
    loop.set_default_executor(EXC)
    while True:
        messages = queue_poller(client=client, sqs_uri=sqs_uri)
        if not messages:
            t1 = time.time()
            logging.info('No messages in Queue')
            logging.info(f'Total Time Taken: {round(t1-16-t0, 1)}')
            loop.close()
            sys.exit()

        loop.run_until_complete(
            process_msgs(
                messages=messages,
                client=client,
                sqs_uri=sqs_uri,
                loop=loop
            )
        )
