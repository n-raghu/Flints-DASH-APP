from asyncio import as_completed
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from bson import ObjectId

from essentials import msg_model, msg_grp
from essentials import sqs_client, sqs_url

account_id = f'CoreStack Mock {time.ctime()}'


def create_actual_msg(acc=account_id):
    model = msg_model()
    oid = str(ObjectId())
    model['opportunity_accountid'] = acc
    model['opportunity_id'] = f'corestack-{oid}'
    model['opportunity_name'] = f'CoreStack Account {oid}'
    return model


def post_messages(count=1000, sqs_uri=sqs_url(), msg_group=msg_grp()):
    messages = []
    client = sqs_client()
    for _ in range(count):
        msg = create_actual_msg()
        response = client.send_message(
            QueueUrl=sqs_uri,
            MessageGroupId=msg_group,
            MessageBody=(json.dumps(msg)),
            MessageDeduplicationId=msg['opportunity_id']
        )
        messages.append({msg['opportunity_id']: response['MessageId']})

    return messages


def msg_poster(**kwargs):
    workers = kwargs.get('workers', 5)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        pool = {
            executor.submit(post_messages,): _ for _ in range(kwargs['batches'])
        }
    for future_ in as_completed(pool):
        print(f'Batch pushed {len(future_.result())} messages', flush=True)


if __name__ == '__main__':
    bmg = msg_poster(batches=1000, workers=16)
