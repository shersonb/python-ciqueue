import queue
from queue import Full, Empty

__all__ = ['Empty', 'Full', 'Closed', 'Interrupted', 'Queue', 'PriorityQueue', 'LifoQueue']


class Closed(Exception):
    pass


class Interrupted(Closed):
    pass


class CI(object):
    """
    Mixin class providing close and interrupt functionality.
    """

    def _init(self, maxsize):
        super()._init(maxsize)
        self._closed = False
        self._interrupted = False

    def _checkclosed(self):
        if self._closed:
            raise Closed()

    def _checkinterrupted(self):
        if self._interrupted:
            raise Interrupted()

    def _put(self, item):
        self._checkinterrupted()
        self._checkclosed()
        super()._put(item)

    def _get(self):
        self._checkinterrupted()
        return super()._get()

    def _qsize(self):
        self._checkinterrupted()
        print("O", self.not_full._is_owned())

        size = super()._qsize()

        if size == 0:
            self._checkclosed()

        return size

    def interrupt(self):
        '''
        Place Queue into interrupted state. Empties the queue and causes
        all threads to raise the Interrupted exception when get() and
        .put(item) are called.

        All calls to .get() and .put(item) after this method is called
        will also raise the Interrupted exception.
        '''
        with self.not_empty:
            self._interrupted = True
            self.not_empty.notifyAll()

        with self.not_full:
            while super()._qsize():
                super()._get()

            self.not_full.notifyAll()

    def close(self):
        '''
        Closes queue. Causes all threads to raise the Closed exception
        when get() is called on an empty queue and when when put() called.

        Threads that call .get() on, or are currently waiting to get an
        item from an empty queue when this method is called will raise
        the Closed exception.

        Threads that call .get() on a nonempty queue will continue to
        get items.

        Threads that call .put(item) or are currently waiting to put item
        into a full queue when this method is called will BLOCK until
        queue is not full, and then raise the Closed exception.

        Threads that call .put(item) on a queue that is not full will raise
        the Closed exception.
        '''
        with self.not_empty:
            self._closed = True
            self.not_empty.notifyAll()

        with self.not_full:
            self.not_full.notifyAll()


class Queue(CI, queue.Queue):
    pass


class PriorityQueue(CI, queue.PriorityQueue):
    pass


class LifoQueue(CI, queue.LifoQueue):
    pass
