#!/usr/bin/env python

import sys
import multiprocessing
from scapy.all import *

dst_IP=sys.argv[1]
num_processes=7

def worker(port1):
    while not port1.empty():
        src_port=RandShort()
        dst_port=port1.get()

        response=sr1(IP(dst=dst_IP)/TCP(sport=src_port,dport=int(dst_port),flags="S"), timeout=1, verbose=0)
        if str(type(response))=="<type 'NoneType'>":
            pass
        elif(response.haslayer(TCP)):
            if(response.getlayer(TCP).flags==0x12):
                send_reset=sr1(IP(dst=dst_IP)/TCP(sport=src_port,dport=int(dst_port),flags="AR"))
                print '\033[4m'+"\nPort "+str(dst_port)+'\033[0m'+'\033[92m'+" open\n"+'\033[0m'
            elif (response.getlayer(TCP).flags==0x14):
                pass
    return

def main():
    if len(sys.argv)==3:
        ports_replace=sys.argv[2].replace('-',' ').replace(':',' ').replace(',',' ')
        try:
            init_port=int(ports_replace.split(' ',1)[-2])
            fin_port=int(ports_replace.split(' ',1)[-1])
        except IndexError:
            print '\033[93m'+"\nUsage: scan_multithread.py <IPtoScan> <Initial port> <Final port>\n"+'\033[0m'
            exit()
    elif len(sys.argv)==4:
            init_port=int(sys.argv[2])
            fin_port=int(sys.argv[3])
    else:
        print '\033[93m'+"\nUsage: scan_multithread.py <IPtoScan> <Initial port> <Final port>\n"'\033[0m'
        exit()


    ports=[]
    q=multiprocessing.Queue()


    for puertos in range(init_port,fin_port+1):
        q.put(puertos)

    for process in range(num_processes):
        p=multiprocessing.Process(target=worker,args=(q,))
        ports.append(p)
        p.start()

    for p in ports:
        p.join()

if __name__=='__main__':
    main()
