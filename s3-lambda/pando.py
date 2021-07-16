import csv
from datetime import datetime as dtm


datum = [
    {
        'name': "nandu",
        'utnow': dtm.utcnow(),
    },
    {
        'name': 'bindu',
        'utnow': dtm.utcnow()
    }
]


def streamer(n, datum=datum):
    with open('dat.csv', 'w') as ofile:
        listwriter = csv.DictWriter(
            ofile,
            fieldnames=datum[0].keys()
        )
        listwriter.writerow(dict((f,f) for f in datum[0].keys()))
        for i in range(n):
            listwriter.writerows(datum)
