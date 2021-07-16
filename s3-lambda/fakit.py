import time
from random import choice
from csv import DictWriter
from multiprocessing import Process, JoinableQueue
from concurrent.futures import ThreadPoolExecutor, as_completed

from faker import Faker
from bson.objectid import ObjectId

Q = JoinableQueue(10000)


def gen_usr_set(fkt, Q, nuset=100):
    users = []
    for _i in range(nuset):
        gender = choice(['F', 'M'])
        users.append({
            'uid': str(ObjectId()),
            'gender': gender,
            'name': fkt.name_female() if gender == 'F' else fkt.name_male(),
            'address': address_cleanser(fkt.address()),
            'country': fkt.country(),
            'email': fkt.email(),
            'dob': fkt.date_of_birth(),
            'db_stamp': fkt.date_time_this_decade()
        })

    Q.put(users)


def address_cleanser(addr):
    if '\n' in addr:
        addr = addr.replace('\n', ' ')
    if '\r' in addr:
        addr = addr.replace('\r', ' ')

    return addr


def launchpad(count, Q):
    usr_sets = int(count/100)
    f = Faker()

    with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(gen_usr_set, f, Q,) for _ in range(usr_sets)
            ]

    for fut in as_completed(futures):
        r = fut.result()
        if r:
            print(r)


def stream_writer(Q):
    created = False
    print('Streaming...', end='', flush=True)
    with open('datum5.csv', 'w') as csvfile:
        while True:
            while not Q.empty():
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
            time.sleep(0.369)
            if Q.empty():
                time.sleep(1)
                if not Q.empty():
                    continue
                print('DONE', flush=True)
                break

t = time.time()
P1 = Process(target=stream_writer, args=(Q,))
P2 = Process(target=launchpad, args=(10000,Q))

P2.start()
time.sleep(1.6)
P1.start()

P2.join()
Q.join()
P1.join()

print('Program Finished in ', int(time.time() - t))
