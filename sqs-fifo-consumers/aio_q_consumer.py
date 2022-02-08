import sys
import json
import time
import logging
import traceback
import asyncio as aio
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from essentials import sqs_client, sqs_url

sqs_uri = sqs_url()
client = sqs_client()
EXC = ThreadPoolExecutor(max_workers=16)
Q = aio.Queue(1_000)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: %(levelname)s: %(message)s'
)


async def queue_poller(Q=Q, exc=EXC, **kwargs):
    loop = kwargs.pop('loop', None)
    client = kwargs.get('client', None)
    sqs_uri = kwargs.get('sqs_uri', None)
    if not Q:
        sys.exit("Q not initialized")
    if not loop:
        sys.exit('Async Loop does not exists')

    while True:
        try:
            logging.info('Polling SQS...')
            response = await loop.run_in_executor(
                exc,
                partial(
                    client.receive_message,
                    QueueUrl=sqs_uri,
                    MaxNumberOfMessages=10,
                )
            )
            messages = response.get('Messages', [])
            if not messages:
                break
            await Q.put(messages)
            logging.info('Pushed messages to process')
            await aio.sleep(0.1)
        except Exception:
            logging.error(f'Polling SQS Failed: {traceback.format_exc()}')
            sys.exit()

    signal = 'SQS Completed'
    logging.warning(signal)
    return signal


async def process_msg(client, msgs, queue_uri, loop, exc=EXC):
    for msg in msgs:
        await aio.sleep(0.01)
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


async def process_msgs(Q=Q, **kwargs):
    P = kwargs.get('poller')
    loop = kwargs.pop('loop', None)
    client = kwargs.get('client', None)
    sqs_uri = kwargs.get('sqs_uri', None)
    if not loop:
        sys.exit('Async Loop does not exists')

    async def msg_getter():
        return await Q.get()

    while True:
        try:
            msgs = await aio.wait_for(msg_getter(), timeout=1)
            task = [process_msg(client, msgs, sqs_uri, loop)]
            await aio.gather(*task)
        except Exception:
            time.sleep(1)
            if P.done():
                logging.info('SQS Future Finished')
                break

    signal = "Completed EventLoop Q"
    logging.warning(signal)
    return signal


async def prime(**kwargs):
    client = kwargs.pop('client')
    sqs_uri = kwargs.pop('sqs_uri')
    loop = kwargs.pop('loop', None)
    if not loop:
        sys.exit('Async Loop does not exists')

    poller = loop.create_task(
        queue_poller(client=client, sqs_uri=sqs_uri, loop=loop)
    )
    processor = loop.create_task(
        process_msgs(client=client, sqs_uri=sqs_uri, loop=loop, poller=poller)
    )

    await aio.gather(*[poller, processor])


if __name__ == '__main__':
    t0 = time.time()
    loop = aio.get_event_loop()
    loop.set_default_executor(EXC)
    loop.run_until_complete(
        prime(
            client=client,
            sqs_uri=sqs_uri,
            loop=loop
        )
    )
    t1 = time.time()
    logging.info(f'Total Time Taken: {round(t1-16-t0, 1)}')
