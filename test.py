from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime
from time import sleep

def local_t(cntr):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(cntr,
                                                     datetime.now())

def calc_recieve_tstamp(recv_time_stamp, cntr):
    return max(recv_time_stamp, cntr) + 1

def event(pid, cntr):
    cntr[pid] = cntr[pid] + 1
    return cntr

def send_m(pipe, pid, cntr):
    cntr[pid] = cntr[pid] + 1
    pipe.send(('Empty shell', cntr))
    return cntr

def recieve_m(pipe, pid, cntr):
    cntr[pid] = cntr[pid] + 1
    message, timestamp = pipe.recv()
    cntr = calc_recieve_tstamp(timestamp, cntr)
    return cntr

def pr_one(pipe12):
    pid = 0
    cntr = [0, 0, 0]
    cntr = send_m(pipe12, pid, cntr)
    cntr = send_m(pipe12, pid, cntr)
    cntr  = event(pid, cntr)
    cntr = recieve_m(pipe12, pid, cntr)
    cntr  = event(pid, cntr)
    cntr  = event(pid, cntr)
    cntr = recieve_m(pipe12, pid, cntr)
    print ('Process A {}'.format(cntr))


def pr_two(pipe21, pipe23):
    pid = 1
    cntr = [0, 0, 0]
    cntr = recieve_m(pipe21, pid, cntr)
    cntr = recieve_m(pipe21, pid, cntr)
    cntr = send_m(pipe21, pid, cntr)
    cntr = recieve_m(pipe23, pid, cntr)
    cntr = event(pid, cntr)
    cntr = send_m(pipe21, pid, cntr)
    cntr = send_m(pipe23, pid, cntr)
    cntr = send_m(pipe23, pid, cntr)
    print ('Process B {}'.format(cntr))



def pr_three(pipe32):
    pid = 2
    cntr = [0, 0, 0]
    cntr = send_m(pipe32, pid, cntr)
    cntr = recieve_m(pipe32, pid, cntr)
    cntr = event(pid, cntr)
    cntr = recieve_m(pipe32, pid, cntr)
    print ('Process C {}'.format(cntr))



def calc_recieve_tstamp(recv_time_stamp, cntr):
    for id  in range(len(cntr)):
        cntr[id] = max(recv_time_stamp[id], cntr[id])
    return cntr


if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()
    pr1 = Process(target=pr_one,
                       args=(oneandtwo,))
    pr2 = Process(target=pr_two,
                       args=(twoandone, twoandthree))
    pr3 = Process(target=pr_three,
                       args=(threeandtwo,))
    pr1.start()
    pr2.start()
    pr3.start()
    pr1.join()
    pr2.join()
    pr3.join()