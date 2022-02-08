import sys
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from bson import ObjectId

from essentials import msg_model, customer_msg_grps
from essentials import sqs_client, sqs_url

account_id = f'CoreStack Mock {time.ctime()}'


def create_actual_msg(acc=account_id):
    model = msg_model()
    oid = str(ObjectId())
    model['opportunity_accountid'] = acc
    model['opportunity_id'] = f'corestack-{oid}'
    model['opportunity_name'] = f'CoreStack Account {oid}'
    return model


def post_messages(msg_group, count=1000, sqs_uri=sqs_url()):
    client = sqs_client()
    for _ in range(count):
        msg = create_actual_msg()
        _r = client.send_message(
            QueueUrl=sqs_uri,
            MessageGroupId=msg_group,
            MessageBody=(json.dumps(msg)),
            MessageDeduplicationId=msg['opportunity_id']
        )

    return f'{count} messages posted to customer group {msg_group}'


def msg_poster(**kwargs):
    customers = kwargs.get('cgroups', 5)
    msg_per_customer = kwargs.get('msg_per_c', 100)
    customers = customer_msg_grps(customers)
    with ProcessPoolExecutor(max_workers=8) as executor:
        pool = {
            executor.submit(
                post_messages,
                customer,
                msg_per_customer
            ): customer for customer in customers
        }
    for future_ in as_completed(pool):
        print(future_.result())


if __name__ == '__main__':
    cgroups = 10
    msg_per_c = 50

    try:
        cgroups = int(sys.argv[1])
        msg_per_c = int(sys.argv[2])
    except Exception:
        pass

    bmg = msg_poster(cgroups=cgroups, msg_per_c=msg_per_c)
