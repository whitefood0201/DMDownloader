"""
Author: 燕十七
From: https://www.cnblogs.com/libitum/p/14848615.html

The module for asynchronous running tasks in Tk GUI.
"""
import tkinter as tk
import time as time
from concurrent import futures
from typing import Callable, Generic, List, TypeVar


_EVENT_PERIOD_MS = 100
_THREAD_POOL = futures.ThreadPoolExecutor(6, 'pool')

T = TypeVar('T')


class _Promise(Generic[T]):
    def __init__(self, future: futures.Future[T]) -> None:
        self._future = future
        self._on_success = None
        self._on_failure = None

    def then(self, on_success: Callable[[T], None]):
        """ Do something when task is finished. """
        self._on_success = on_success
        return self

    def catch(self, on_failure: Callable[[BaseException], None]):
        """ Do something when task is failed. """
        self._on_failure = on_failure
        return self


class AsyncEvent:
    """
    Used for asynchronous tasks in Tk GUI. It takes use of tk.after to check the
    event and do the callback in the GUI thread, so we can use it just like
    traditional "callback" way.

    The class is singleton, so it's shared in the process.

    """
    def __init__(self, master: tk.Misc) -> None:
        """ Initialize the singleton with Tk.
        Args:
            master: Same in Tk.
        """
        self._master: tk.Misc = master
        self._promise_list: List[_Promise] = []

    def submit(self, task: Callable[..., T], /, *args) -> _Promise[T]:
        """
        Adds an asynchronous task, and return a `Promise` for this task.
        We can add callback by the `Promise`.

        Args:
            task: A function which will be called asynchronously in a thread-pool.
            *args: The arguments for the function.
        Return: Promise object then you can add callback to it.
        """
        if not getattr(self, '_master', None):
            raise RuntimeError('Not initialized. Please call init() at first.')

        future = _THREAD_POOL.submit(task, *args)
        promise: _Promise[T] = _Promise(future)
        self._promise_list.append(promise)

        # If the len of event list is 1, means that it's not running.
        if len(self._promise_list) == 1:
            self._master.after(_EVENT_PERIOD_MS, self._handle_event)

        return promise

    def _handle_event(self):
        """ Works as event loop to do the callback. """
        for promise in self._promise_list:
            future = promise._future
            on_success = promise._on_success
            on_failure = promise._on_failure

            if future.done():
                if future.exception():
                    if on_failure:
                        on_failure(future.exception() or BaseException())
                    else:
                        # add log for the exception.
                        pass
                elif on_success:
                    on_success(future.result())
                self._promise_list.remove(promise)

        # Try to handle events in next cycle.
        if len(self._promise_list) > 0:
            self._master.after(_EVENT_PERIOD_MS, self._handle_event)
