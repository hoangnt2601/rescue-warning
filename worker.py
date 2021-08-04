import queue
import threading
from threading import Thread

class Worker:
    def __init__(self,task, number_worker,max_size_queue=0):
        self.task = task
        self.number_worker = number_worker
        self.max_size_queue = max_size_queue
        self.q = queue.Queue(maxsize=0)

        self.threads = []
        for i in range(self.number_worker):
            t = threading.Thread(target=self.__worker__)
            t.start()
            self.threads.append(t)

    def __worker__(self):
        while True:
            item = self.q.get()
            if item is None:
                break
            self.task(item)
            self.q.task_done()

    def add_job(self,item):
        self.q.put(item)

    def wait_and_stop(self):
        self.q.join()

        for i in range(self.number_worker):
            self.q.put(None)
        for t in self.threads:
            t.join()