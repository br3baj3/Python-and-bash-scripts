from  threading import Thread
from  threading import Lock
import Queue
import time
import ftplib

class List_pub(Thread):

        def __init__(self,queue,lock):
                Thread.__init__(self)
                self.queue=queue
                self.lock=lock

        def run(self):
                while True:
                        list=[]
                        address_ftp=self.queue.get()
                        print "Connecting to %s" %address_ftp
                        try:
                                ftp=ftplib.FTP(address_ftp)
                                ftp.login()
                                ftp.cwd('pub')
                                ftp.retrlines('LIST',list.append)
                        except ftplib.all_errors as e:
                                print "Fail to connect...\n"
                                print e
                        self.queue.task_done()
                        self.lock.acquire()
                        result=open('ftp_dir.txt', 'a')
                        result.write("\nFTP: %s\n\n" %address_ftp)
                        for content in list:
                                result.write(content+"\n")
                        result.close()
                        self.lock.release()
queue=Queue.Queue()
num_threads=5
lock=Lock()

for i in range(num_threads):
        worker=List_pub(queue,lock)
        worker.setDaemon(True)
        worker.start()

dir_result=open('ftp_dir.txt','w')
dir_result.close()

for line in open('lista_ftps.txt','r'):
        line=line.rstrip('\n')
        queue.put(line)


queue.join()
