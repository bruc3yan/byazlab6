# TODO: in progress
import threading

# Global lock
lock = threading.Lock()


class Locks(object):
    def __init__(self, name):
        self.name = name
        self.lock = None
        self.owner = None

    def create(self):
        self.lock = lock.acquire()

    def request(self):
        # returns true if lock has been acquired, false if the timeout has elapsed
        return self.lock

    def destroy(self):
        self.lock = lock.release()
