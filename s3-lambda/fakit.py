import time
from random import choice
from csv import DictWriter
from multiprocessing import Process, JoinableQueue
from concurrent.futures import ThreadPoolExecutor, as_completed

from faker import Faker
from bson.objectid import ObjectId

Q = JoinableQueue(1000)


def gen_usr_set(Q, nuset=10):
    fkr = Faker()
    users = []
    for _i in range(nuset):
        gender = choice(['F', 'M'])
        users.append({
            'uid': str(ObjectId()),
            'gender': gender,
            'name': fkr.name_female() if gender == 'F' else fkr.name_male(),
            'address': address_cleanser(fkr.address()),
            'country': fkr.country(),
            'email': fkr.email(),
            'dob': fkr.date_of_birth(),
            'db_stamp': fkr.date_time_this_decade()
        })

    Q.put(users)


def address_cleanser(addr):
    return addr.replace('\n', ' ').replace('\r', ' ')


def launchpad(records, chunk_size Q):
    usr_sets = int(records/chunk_size)
    f = Faker()

    with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(gen_usr_set, Q, chunk_size,) for _ in range(usr_sets)
            ]

    for fut in as_completed(futures):
        r = fut.result()
        if r:
            print(r)


def stream_writer(records, chunk_size, Q):
    total_batches = int(records/chunk_size)
    empty_queue_num = 0
    consecutive_chk = 0
    created = False
    print('Streaming...', flush=True)
    with open('datum5.csv', 'w') as csvfile:
        while P1.is_alive() or not Q.empty():
            empty_queue_num += 1
            consecutive_chk += 1
            while not Q.empty():
                batches += 1
                dat = Q.get()
                csv_writer = DictWriter(
                    csvfile,
                    fieldnames=dat[0].keys(),
                    delimiter='|',
                )
                if not created:
                    csv_writer.writerow(dict((fld,fld) for fld in dat[0].keys()))
                    created = True
                csv_writer.writerows(dat)
                Q.task_done()
                consecutive_chk = 0

            print(empty_queue_num, 'Q-Empty, Waiting for refill.', end='', flush=True)
            print(' Consecutive Checks:', consecutive_chk, end='', flush=True)
            print(' Successful Batches:', f'{batches}/{total_batches}', flush=True)
            time.sleep(1.88)


t = time.time()
records = 500_000_000
chunk_size = 1000
P1 = Process(target=launchpad, args=(records,chunk_size,Q))

P1.daemon = True
P1.start()
stream_writer(records, chunk_size, Q)
P1.join()
print("Launchpad completed")

Q.join()
print('Program Finished in ', int(time.time() - t))
