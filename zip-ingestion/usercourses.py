import csv
import codecs
import random
import itertools
from datetime import datetime as dtm, timedelta as tdt

from bson.objectid import ObjectId

stamp = dtm.utcnow().replace(microsecond=0)


def yield_users(usrcsv):
    with open(usrcsv, 'r') as ufile:
        for row in csv.DictReader(ufile, delimiter='|'):
            yield row


def cache_courses():
    courses = []
    with open('courses.csv', 'r') as cfile:
        for row in csv.DictReader(cfile, delimiter='|'):
            courses.append(row)

    return courses


def prime():
    usercourses = []
    courses = cache_courses()
    stream = yield_users('users.csv')
    while True:
        try:
            ucs = []
            cycle_users= []
            cycle_courses = []
            for _ in range(36):
                cycle_courses += random.sample(courses, 5)
            nuset_users = list(itertools.islice(stream, 100))
            shortlisted_users = random.sample(nuset_users, 36)
            cycle_users = shortlisted_users.copy()
            for _ in range(9):
                cycle_users += random.sample(shortlisted_users, 16)

            for raw_doc in zip(cycle_courses, cycle_users):
                ucs.append(
                    create_usr_course(raw_doc)
                )
            usercourses = itertools.chain(ucs, usercourses)
        except Exception as err:
            break

    return write_to_csv(usercourses)


def create_usr_course(uczip, base=stamp):
    c, u = uczip
    r = random.choice(range(-36,36))
    ucstamp = base + tdt(days=r)
    return {
        'uccid': str(ObjectId()),
        'uid': u['uid'],
        'course_id': c['course_id'],
        'time_taken': int(c['duration']) + r,
        'icode': 'chunk-1',
        'db_stamp': ucstamp.isoformat()
    }


def write_to_csv(itero):
    itr_list = list(itero)
    with open('usercourses.csv', 'w') as ucfile:
        csv_writer = csv.DictWriter(
            ucfile,
            fieldnames=itr_list[0].keys(),
            delimiter='|'
        )
        csv_writer.writerow(dict((fld, fld) for fld in itr_list[0].keys()))
        csv_writer.writerows(itr_list)

    return True


if __name__ == '__main__':
    p = prime()
