import sched
import time
from googledriveutils import write_to_reactordrive
s = sched.scheduler(time.time, time.sleep)


def main(sc):
    print 'Querying Reactor'
    write_to_reactordrive(1, 'R1data.csv')
    sc.enter(30, 1, main, (sc,))

s.enter(30, 1, main, (s,))
s.run()
