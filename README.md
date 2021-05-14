# python-ciqueue
Closable, Interruptable Python queues

This module provides additional functionality to Python queues.

# Added methods

## .close() method

This method allows for a queue to be placed into a closed state. In this state,
no further items can be placed into the queue, while items still in the queue can
still be retrieved.

Threads waiting to **get** an item from an empty queue when .close() is called will
immediately raise the Closed exception.

Calls to .get() on an empty queue after .close() has been called will also raise
the Closed exception.

Calls to .get() on a nonempty queue will continue to get items.

Threads waiting to **put** an item into a full queue, however, will continue to
block until queue is no longer full (or .interrupt() is called), and then will
raise the Closed exception.

Calls to .put() on a full queue will also block until queue is no longer full or
is interrupted.

## .interrupt() method

This method interrupts the queue immediately, causing all threads waiting to **get**
or **put** to raise the Interrupted exception immediately.

Calls to .get() on an nonempty queue, or .put(item) on a non-full queue after
.interrupt() has been called will also immediately raise the Interrupted exception.

# Usage

The .close() and .interrupt() methods are provided by the mixin class CI. To use,
simply subclass a queue.Queue subclass as follows:

```python
from ciqueue import CI

class Queue(CI, queue.Queue):
    pass
```

Note: The mixin also provides ._put(item), ._get(), ._qsize(), and ._init(maxsize)
methods. In order implement these methods, a subclass must be created **before** mixing
in with the CI class.

```python
from ciqueue import CI

class CustomQueue(queue.Queue):
    def _init(self, maxsize):
        pass

    def _get(self):
        pass

    def _put(self, item):
        pass

    def _qsize(self):
        pass

class CustomQueue(CI, CustomQueue):
    pass
```
